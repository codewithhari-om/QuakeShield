import { fetchAllSources } from '../adapters/index.js';
import { STATUS } from '../shared/config.js';
import {
  getSettings,
  getState,
  saveState,
  getNotifiedEventMap,
  pruneNotifiedEvents,
  setNotifiedEventMap,
  saveSettings
} from '../shared/storage.js';
import { deriveStatus, filterFreshEvents, mergeDuplicateEvents, scoreEventRelevance } from '../shared/events.js';
import { isStale } from '../shared/time.js';
import { notificationDescriptorForEvent, notificationTitleForEvent } from '../shared/presentation.js';

const POLL_ALARM = 'qs_poll_alarm';

chrome.runtime.onInstalled.addListener(async () => {
  const settings = await getSettings();
  await saveSettings(settings);
  await schedulePolling(settings.pollingIntervalSeconds);
  await refreshState('install');
});

chrome.runtime.onStartup.addListener(async () => {
  const settings = await getSettings();
  await schedulePolling(settings.pollingIntervalSeconds);
  await refreshState('startup');
});

chrome.alarms.onAlarm.addListener(async (alarm) => {
  if (alarm.name === POLL_ALARM) {
    await refreshState('alarm');
  }
});

chrome.storage.onChanged.addListener(async (changes, area) => {
  if (area !== 'local' || !changes.qs_settings) return;
  const settings = changes.qs_settings.newValue;
  await schedulePolling(settings.pollingIntervalSeconds);
  await refreshState('settings');
});

chrome.runtime.onMessage.addListener((message, _sender, sendResponse) => {
  (async () => {
    if (message?.type === 'QS_GET_STATE') {
      const state = await getState();
      sendResponse({ ok: true, state });
      return;
    }

    if (message?.type === 'QS_REFRESH') {
      const state = await refreshState('manual');
      sendResponse({ ok: true, state });
      return;
    }

    sendResponse({ ok: false, error: 'Unsupported message' });
  })().catch((error) => sendResponse({ ok: false, error: String(error?.message || error) }));
  return true;
});

chrome.notifications.onClicked.addListener(async (notificationId) => {
  const detailsUrl = chrome.runtime.getURL(`src/popup/event-details.html?eventId=${encodeURIComponent(notificationId)}`);
  await chrome.tabs.create({ url: detailsUrl });
});

async function schedulePolling(seconds) {
  const periodMinutes = Math.max(1, Number(seconds || 120) / 60);
  await chrome.alarms.clear(POLL_ALARM);
  await chrome.alarms.create(POLL_ALARM, { periodInMinutes: periodMinutes });
}

async function refreshState(trigger) {
  const settings = await getSettings();
  const now = Date.now();

  const fetched = await fetchAllSources(settings);
  const deduped = mergeDuplicateEvents(fetched.events);
  const freshEvents = filterFreshEvents(deduped, settings.maxEventAgeMinutes, now);

  const checks = new Map();
  for (const event of freshEvents) {
    checks.set(event.id, scoreEventRelevance(event, settings, settings.location));
  }

  const sourceHealth = markStaleSources(fetched.health, settings.staleAfterMinutes, now);
  const status = deriveStatus(freshEvents, checks, sourceHealth, settings);

  const relevantEvents = freshEvents
    .map((event) => ({ event, check: checks.get(event.id) }))
    .filter(({ check }) => check?.relevant)
    .sort((a, b) => new Date(b.event.occurredAt || 0).getTime() - new Date(a.event.occurredAt || 0).getTime());

  const top = relevantEvents[0] || null;
  const state = {
    trigger,
    status,
    generatedAt: new Date(now).toISOString(),
    lastSuccessfulUpdate: Object.values(sourceHealth)
      .map((source) => source.updatedAt)
      .filter(Boolean)
      .sort()
      .at(-1) || null,
    stale: !Object.values(sourceHealth).some((source) => source.connected && !source.stale),
    sources: sourceHealth,
    events: freshEvents,
    relevantEventIds: relevantEvents.map(({ event }) => event.id),
    focusedEvent: top
      ? {
          ...top.event,
          distanceKm: top.check?.distanceKm ?? null
        }
      : null
  };

  await saveState(state);
  await notifyForEvent(state, settings);
  await broadcastOverlayState(state, settings);
  return state;
}

function markStaleSources(sourceHealth, staleAfterMinutes, nowMs) {
  const result = {};
  for (const [name, status] of Object.entries(sourceHealth)) {
    const stale = status?.updatedAt ? isStale(status.updatedAt, staleAfterMinutes, nowMs) : !status?.connected;
    result[name] = {
      ...status,
      stale
    };
  }
  return result;
}

async function notifyForEvent(state, settings) {
  if (!settings.notifications.enabled || !state.focusedEvent) return;

  const event = state.focusedEvent;
  if (event.isTest && !settings.notifications.includeTestMode) return;

  const allowedType =
    (event.sourceType === 'PRELIMINARY_DETECTION' && settings.notifications.allowPreliminary) ||
    (event.sourceType === 'CONFIRMED_REPORT' && settings.notifications.allowReports) ||
    (event.sourceType === 'EARLY_WARNING' && settings.notifications.allowEarlyWarnings) ||
    event.sourceType === 'TEST';

  if (!allowedType) return;

  const notified = await getNotifiedEventMap();
  if (notified[event.id]) return;

  const permission = await chrome.notifications.getPermissionLevel();
  if (permission !== 'granted') return;

  const title = notificationTitleForEvent(event);
  const descriptor = notificationDescriptorForEvent(event);
  const magnitudeLabel = event.magnitude === null ? 'Magnitude unavailable' : `M${event.magnitude.toFixed(1)}`;
  const area = event.locationName || 'Unknown area';
  const source = event.source;
  const body = `${descriptor}\n${magnitudeLabel} • ${area}\nSource: ${source} • ${new Date(event.occurredAt || Date.now()).toLocaleString()}`;

  try {
    await chrome.notifications.create(event.id, {
      type: 'basic',
      iconUrl: 'assets/icon128.png',
      title,
      message: body,
      priority: 2,
      silent: !settings.notifications.playSound
    });
    notified[event.id] = Date.now();
    await pruneNotifiedEvents(Date.now() - 1000 * 60 * 60 * 24);
    await setNotifiedEventMap(notified);
  } catch (_error) {
    // Notifications may fail due to browser restrictions.
  }
}

function hostMatchesAllowlist(hostname, patterns) {
  if (!patterns.length) return false;
  return patterns.some((pattern) => {
    const trimmed = pattern.trim().toLowerCase();
    if (!trimmed) return false;
    if (trimmed.startsWith('*.')) {
      const suffix = trimmed.slice(2);
      return hostname === suffix || hostname.endsWith(`.${suffix}`);
    }
    return hostname === trimmed;
  });
}

async function broadcastOverlayState(state, settings) {
  if (!settings.overlay.enabled) return;

  const focusedEvent = state.focusedEvent;
  const shouldShow = [STATUS.alert, STATUS.watch, STATUS.test].includes(state.status) && !!focusedEvent;

  const tabs = await chrome.tabs.query({});
  for (const tab of tabs) {
    if (!tab.id || !tab.url) continue;

    let hostname;
    try {
      hostname = new URL(tab.url).hostname.toLowerCase();
    } catch {
      continue;
    }

    if (!hostMatchesAllowlist(hostname, settings.overlay.allowedSites)) continue;

    const payload = {
      type: 'QS_OVERLAY_UPDATE',
      shouldShow,
      event: focusedEvent,
      status: state.status,
      generatedAt: state.generatedAt,
      testMode: settings.sources.mock.enabled
    };

    try {
      await chrome.tabs.sendMessage(tab.id, payload);
    } catch {
      try {
        await chrome.scripting.insertCSS({ target: { tabId: tab.id }, files: ['src/content/overlay.css'] });
        await chrome.scripting.executeScript({ target: { tabId: tab.id }, files: ['src/content/overlay.js'] });
        await chrome.tabs.sendMessage(tab.id, payload);
      } catch {
        // Ignore pages where scripts cannot run.
      }
    }
  }
}
