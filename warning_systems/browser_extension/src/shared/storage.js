import { DEFAULT_SETTINGS, STORAGE_KEYS } from './config.js';

function deepMerge(base, update) {
  if (Array.isArray(base) || Array.isArray(update)) {
    return update ?? base;
  }
  if (typeof base !== 'object' || base === null || typeof update !== 'object' || update === null) {
    return update ?? base;
  }
  const merged = { ...base };
  for (const key of Object.keys(update)) {
    merged[key] = key in base ? deepMerge(base[key], update[key]) : update[key];
  }
  return merged;
}

export async function getSettings() {
  const stored = await chrome.storage.local.get(STORAGE_KEYS.settings);
  return deepMerge(DEFAULT_SETTINGS, stored[STORAGE_KEYS.settings] || {});
}

export async function saveSettings(nextSettings) {
  const current = await getSettings();
  const merged = deepMerge(current, nextSettings || {});
  await chrome.storage.local.set({ [STORAGE_KEYS.settings]: merged });
  return merged;
}

export async function getState() {
  const stored = await chrome.storage.local.get(STORAGE_KEYS.state);
  return stored[STORAGE_KEYS.state] || null;
}

export async function saveState(state) {
  await chrome.storage.local.set({ [STORAGE_KEYS.state]: state });
}

export async function getNotifiedEventMap() {
  const stored = await chrome.storage.local.get(STORAGE_KEYS.notifiedEvents);
  return stored[STORAGE_KEYS.notifiedEvents] || {};
}

export async function setNotifiedEventMap(map) {
  await chrome.storage.local.set({ [STORAGE_KEYS.notifiedEvents]: map });
}

export async function pruneNotifiedEvents(cutoffTimestampMs) {
  const current = await getNotifiedEventMap();
  const next = {};
  for (const [eventId, ts] of Object.entries(current)) {
    if (ts >= cutoffTimestampMs) {
      next[eventId] = ts;
    }
  }
  await setNotifiedEventMap(next);
  return next;
}

export { deepMerge };
