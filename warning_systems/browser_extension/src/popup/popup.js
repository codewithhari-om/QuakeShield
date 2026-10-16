import { STATUS } from '../shared/config.js';
import { getSettings, saveSettings } from '../shared/storage.js';

const ui = {
  openSettings: document.getElementById('openSettings'),
  openPreferences: document.getElementById('openPreferences'),
  useGeolocation: document.getElementById('useGeolocation'),
  clearLocation: document.getElementById('clearLocation'),
  manualForm: document.getElementById('manualLocationForm'),
  manualCity: document.getElementById('manualCity'),
  manualLat: document.getElementById('manualLat'),
  manualLon: document.getElementById('manualLon'),
  changeLocation: document.getElementById('changeLocation'),
  refreshState: document.getElementById('refreshState'),
  viewDetails: document.getElementById('viewDetails'),
  openDashboard: document.getElementById('openDashboard'),
  toggleOverlay: document.getElementById('toggleOverlay'),
  locationPermission: document.getElementById('locationPermission'),
  locationValue: document.getElementById('locationValue'),
  statusCard: document.getElementById('statusCard'),
  statusBadge: document.getElementById('statusBadge'),
  statusMessage: document.getElementById('statusMessage'),
  lastUpdate: document.getElementById('lastUpdate'),
  eventCard: document.getElementById('eventCard'),
  eventMag: document.getElementById('eventMag'),
  eventLoc: document.getElementById('eventLoc'),
  eventDistance: document.getElementById('eventDistance'),
  eventType: document.getElementById('eventType'),
  eventTime: document.getElementById('eventTime'),
  eventSource: document.getElementById('eventSource'),
  warningLeadWrap: document.getElementById('warningLeadWrap'),
  warningLead: document.getElementById('warningLead'),
  sourceList: document.getElementById('sourceList')
};

let currentState = null;
let settings = null;

function labelFromStatus(status) {
  switch (status) {
    case STATUS.allClear:
      return 'ALL CLEAR';
    case STATUS.watch:
      return 'WATCH';
    case STATUS.alert:
      return 'EARTHQUAKE ALERT';
    case STATUS.test:
      return 'TEST MODE';
    default:
      return 'DATA UNAVAILABLE';
  }
}

function statusClass(status) {
  switch (status) {
    case STATUS.allClear:
      return 'ok';
    case STATUS.watch:
      return 'watch';
    case STATUS.alert:
      return 'alert';
    case STATUS.test:
      return 'test';
    default:
      return 'unknown';
  }
}

function formatDate(value) {
  if (!value) return '--';
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return '--';
  return date.toLocaleString();
}

function renderLocation() {
  const location = settings.location;
  ui.locationPermission.textContent = `Permission: ${location.permission}`;
  if (location.mode === 'geolocation' && location.city) {
    ui.locationValue.textContent = `${location.city} (browser location)`;
  } else if (location.mode === 'manual' && location.city) {
    ui.locationValue.textContent = `${location.city} (manual)`;
  } else {
    ui.locationValue.textContent = 'No location selected';
  }
}

function renderSources(sources = {}) {
  ui.sourceList.innerHTML = '';
  const ordered = [
    ['quakeShield', 'QuakeShield backend'],
    ['official', 'Official source'],
    ['mock', 'Mock TEST source']
  ];

  for (const [key, label] of ordered) {
    const source = sources[key] || {};
    const li = document.createElement('li');
    li.className = 'source-row';
    li.innerHTML = `
      <span>${label}</span>
      <span>${source.status || 'unknown'}${source.stale ? ' (stale)' : ''}</span>
    `;
    ui.sourceList.appendChild(li);
  }
}

function renderEvent(event, status) {
  if (!event) {
    ui.eventCard.hidden = true;
    return;
  }

  ui.eventCard.hidden = false;
  ui.eventMag.textContent = event.magnitude === null ? 'Unavailable' : `M${event.magnitude.toFixed(1)}`;
  ui.eventLoc.textContent = event.locationName || 'Unknown';
  ui.eventDistance.textContent = event.distanceKm === null ? 'Unavailable' : `${event.distanceKm.toFixed(1)} km`;
  ui.eventType.textContent = event.sourceType;
  ui.eventTime.textContent = formatDate(event.occurredAt);
  ui.eventSource.textContent = `${event.source}${event.matchedSources?.length ? ` (${event.matchedSources.join(', ')})` : ''}`;

  if (status === STATUS.alert && Number.isFinite(event.warningLeadSeconds) && event.warningLeadSeconds > 0) {
    ui.warningLeadWrap.hidden = false;
    ui.warningLead.textContent = `${event.warningLeadSeconds}s (from backend)`;
  } else {
    ui.warningLeadWrap.hidden = true;
    ui.warningLead.textContent = '--';
  }
}

function renderStatus(state) {
  const status = state?.status || STATUS.unknown;
  ui.statusCard.classList.remove('watch', 'alert', 'unknown', 'test');
  const css = statusClass(status);
  if (css !== 'ok') {
    ui.statusCard.classList.add(css);
  }

  ui.statusBadge.textContent = labelFromStatus(status);
  ui.lastUpdate.textContent = `Last update: ${formatDate(state?.lastSuccessfulUpdate || state?.generatedAt)}`;

  if (status === STATUS.allClear) {
    ui.statusMessage.textContent = 'No relevant active alert is currently known.';
  } else if (status === STATUS.watch) {
    ui.statusMessage.textContent = 'Potential relevant event detected. Monitor updates closely.';
  } else if (status === STATUS.alert) {
    ui.statusMessage.textContent = 'Validated alert criteria met for your configured area.';
  } else if (status === STATUS.test) {
    ui.statusMessage.textContent = 'TEST MODE is active. Alerts are simulated only.';
  } else {
    ui.statusMessage.textContent = 'Latest status cannot be verified. Data may be stale or unavailable.';
  }

  renderEvent(state?.focusedEvent || null, status);
  renderSources(state?.sources || {});
}

async function refreshState() {
  const response = await chrome.runtime.sendMessage({ type: 'QS_GET_STATE' });
  currentState = response?.state || null;
  renderStatus(currentState);
}

async function forceRefresh() {
  const response = await chrome.runtime.sendMessage({ type: 'QS_REFRESH' });
  currentState = response?.state || null;
  renderStatus(currentState);
}

async function requestGeolocation() {
  if (!navigator.geolocation) return;

  navigator.geolocation.getCurrentPosition(
    async (position) => {
      const next = {
        location: {
          ...settings.location,
          mode: 'geolocation',
          permission: 'granted',
          city: settings.location.city || 'Current location',
          latitude: Number(position.coords.latitude.toFixed(5)),
          longitude: Number(position.coords.longitude.toFixed(5))
        }
      };
      settings = await saveSettings(next);
      renderLocation();
      await forceRefresh();
    },
    async () => {
      settings = await saveSettings({ location: { ...settings.location, permission: 'denied' } });
      renderLocation();
    },
    { enableHighAccuracy: false, timeout: 7000, maximumAge: 300000 }
  );
}

async function saveManualLocation(event) {
  event.preventDefault();
  const city = ui.manualCity.value.trim();
  if (!city) return;

  const lat = Number(ui.manualLat.value);
  const lon = Number(ui.manualLon.value);
  const hasCoords = Number.isFinite(lat) && Number.isFinite(lon);

  settings = await saveSettings({
    location: {
      mode: 'manual',
      city,
      latitude: hasCoords ? lat : null,
      longitude: hasCoords ? lon : null,
      permission: settings.location.permission || 'prompt'
    }
  });

  ui.manualForm.reset();
  renderLocation();
  await forceRefresh();
}

async function clearLocation() {
  settings = await saveSettings({
    location: {
      mode: 'none',
      city: '',
      latitude: null,
      longitude: null,
      permission: settings.location.permission || 'prompt'
    }
  });
  renderLocation();
  await forceRefresh();
}

async function toggleOverlay() {
  const enabled = !settings.overlay.enabled;
  settings = await saveSettings({ overlay: { ...settings.overlay, enabled } });
  await forceRefresh();
}

function openSettings() {
  chrome.runtime.openOptionsPage();
}

function openDashboard() {
  const url = settings.links.dashboardUrl;
  if (!url) {
    chrome.runtime.openOptionsPage();
    return;
  }
  chrome.tabs.create({ url });
}

function openEventDetails() {
  if (currentState?.focusedEvent?.url) {
    chrome.tabs.create({ url: currentState.focusedEvent.url });
  }
}

async function init() {
  settings = await getSettings();
  renderLocation();
  await refreshState();

  ui.openSettings.addEventListener('click', openSettings);
  ui.openPreferences.addEventListener('click', openSettings);
  ui.changeLocation.addEventListener('click', openSettings);
  ui.useGeolocation.addEventListener('click', requestGeolocation);
  ui.clearLocation.addEventListener('click', clearLocation);
  ui.manualForm.addEventListener('submit', saveManualLocation);
  ui.refreshState.addEventListener('click', forceRefresh);
  ui.viewDetails.addEventListener('click', openEventDetails);
  ui.openDashboard.addEventListener('click', openDashboard);
  ui.toggleOverlay.addEventListener('click', toggleOverlay);
}

init();
