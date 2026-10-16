import { getSettings, saveSettings } from '../shared/storage.js';

const fields = {
  distanceThresholdKm: document.getElementById('distanceThresholdKm'),
  magnitudeThreshold: document.getElementById('magnitudeThreshold'),
  pollingIntervalSeconds: document.getElementById('pollingIntervalSeconds'),
  staleAfterMinutes: document.getElementById('staleAfterMinutes'),
  maxEventAgeMinutes: document.getElementById('maxEventAgeMinutes'),
  locationMode: document.getElementById('locationMode'),
  locationCity: document.getElementById('locationCity'),
  locationLatitude: document.getElementById('locationLatitude'),
  locationLongitude: document.getElementById('locationLongitude'),
  sourceQuakeShieldEnabled: document.getElementById('sourceQuakeShieldEnabled'),
  sourceQuakeShieldEventsUrl: document.getElementById('sourceQuakeShieldEventsUrl'),
  sourceQuakeShieldApiKey: document.getElementById('sourceQuakeShieldApiKey'),
  sourceOfficialEnabled: document.getElementById('sourceOfficialEnabled'),
  sourceOfficialFeedUrl: document.getElementById('sourceOfficialFeedUrl'),
  sourceMockEnabled: document.getElementById('sourceMockEnabled'),
  notificationsEnabled: document.getElementById('notificationsEnabled'),
  notificationsPlaySound: document.getElementById('notificationsPlaySound'),
  notificationsAllowPreliminary: document.getElementById('notificationsAllowPreliminary'),
  notificationsAllowReports: document.getElementById('notificationsAllowReports'),
  notificationsAllowEarlyWarnings: document.getElementById('notificationsAllowEarlyWarnings'),
  notificationsIncludeTestMode: document.getElementById('notificationsIncludeTestMode'),
  overlayEnabled: document.getElementById('overlayEnabled'),
  overlayAllowedSites: document.getElementById('overlayAllowedSites'),
  dashboardUrl: document.getElementById('dashboardUrl'),
  saveBtn: document.getElementById('saveBtn'),
  saveStatus: document.getElementById('saveStatus')
};

let settings = null;

function parseOptionalNumber(value) {
  if (value === '' || value === null || value === undefined) return null;
  const numeric = Number(value);
  return Number.isFinite(numeric) ? numeric : null;
}

function fillForm() {
  fields.distanceThresholdKm.value = settings.distanceThresholdKm;
  fields.magnitudeThreshold.value = settings.magnitudeThreshold;
  fields.pollingIntervalSeconds.value = settings.pollingIntervalSeconds;
  fields.staleAfterMinutes.value = settings.staleAfterMinutes;
  fields.maxEventAgeMinutes.value = settings.maxEventAgeMinutes;

  fields.locationMode.value = settings.location.mode;
  fields.locationCity.value = settings.location.city || '';
  fields.locationLatitude.value = settings.location.latitude ?? '';
  fields.locationLongitude.value = settings.location.longitude ?? '';

  fields.sourceQuakeShieldEnabled.checked = settings.sources.quakeShield.enabled;
  fields.sourceQuakeShieldEventsUrl.value = settings.sources.quakeShield.eventsUrl || '';
  fields.sourceQuakeShieldApiKey.value = settings.sources.quakeShield.apiKey || '';

  fields.sourceOfficialEnabled.checked = settings.sources.official.enabled;
  fields.sourceOfficialFeedUrl.value = settings.sources.official.feedUrl || '';

  fields.sourceMockEnabled.checked = settings.sources.mock.enabled;

  fields.notificationsEnabled.checked = settings.notifications.enabled;
  fields.notificationsPlaySound.checked = settings.notifications.playSound;
  fields.notificationsAllowPreliminary.checked = settings.notifications.allowPreliminary;
  fields.notificationsAllowReports.checked = settings.notifications.allowReports;
  fields.notificationsAllowEarlyWarnings.checked = settings.notifications.allowEarlyWarnings;
  fields.notificationsIncludeTestMode.checked = settings.notifications.includeTestMode;

  fields.overlayEnabled.checked = settings.overlay.enabled;
  fields.overlayAllowedSites.value = (settings.overlay.allowedSites || []).join('\n');
  fields.dashboardUrl.value = settings.links.dashboardUrl || '';
}

function validateUrlField(label, value, requiredWhenEnabled = false) {
  if (!value) {
    if (requiredWhenEnabled) {
      throw new Error(`${label} is required when this source is enabled.`);
    }
    return;
  }

  let parsed;
  try {
    parsed = new URL(value);
  } catch {
    throw new Error(`${label} must be a valid URL.`);
  }

  if (!['http:', 'https:'].includes(parsed.protocol)) {
    throw new Error(`${label} must use http or https.`);
  }
}

async function requestOptionalOriginsIfNeeded(nextSettings) {
  const backendUrl = nextSettings.sources.quakeShield.eventsUrl;
  if (!backendUrl) return;

  const parsed = new URL(backendUrl);
  const origin = `${parsed.protocol}//${parsed.host}/*`;

  const currentOrigins = await chrome.permissions.getAll();
  if (currentOrigins.origins?.includes(origin)) return;

  const granted = await chrome.permissions.request({ origins: [origin] });
  if (!granted) {
    throw new Error('Backend host permission was not granted. Requests to backend may fail until granted.');
  }
}

async function save() {
  try {
    const nextSettings = {
      distanceThresholdKm: Math.max(1, Number(fields.distanceThresholdKm.value || 300)),
      magnitudeThreshold: Math.max(0, Number(fields.magnitudeThreshold.value || 0)),
      pollingIntervalSeconds: Math.max(30, Number(fields.pollingIntervalSeconds.value || 120)),
      staleAfterMinutes: Math.max(1, Number(fields.staleAfterMinutes.value || 10)),
      maxEventAgeMinutes: Math.max(1, Number(fields.maxEventAgeMinutes.value || 120)),
      location: {
        mode: fields.locationMode.value,
        city: fields.locationCity.value.trim(),
        latitude: parseOptionalNumber(fields.locationLatitude.value),
        longitude: parseOptionalNumber(fields.locationLongitude.value),
        permission: settings.location.permission || 'prompt'
      },
      sources: {
        quakeShield: {
          ...settings.sources.quakeShield,
          enabled: fields.sourceQuakeShieldEnabled.checked,
          eventsUrl: fields.sourceQuakeShieldEventsUrl.value.trim(),
          apiKey: fields.sourceQuakeShieldApiKey.value.trim()
        },
        official: {
          ...settings.sources.official,
          enabled: fields.sourceOfficialEnabled.checked,
          feedUrl: fields.sourceOfficialFeedUrl.value.trim()
        },
        mock: {
          enabled: fields.sourceMockEnabled.checked
        }
      },
      notifications: {
        enabled: fields.notificationsEnabled.checked,
        playSound: fields.notificationsPlaySound.checked,
        allowPreliminary: fields.notificationsAllowPreliminary.checked,
        allowReports: fields.notificationsAllowReports.checked,
        allowEarlyWarnings: fields.notificationsAllowEarlyWarnings.checked,
        includeTestMode: fields.notificationsIncludeTestMode.checked
      },
      overlay: {
        enabled: fields.overlayEnabled.checked,
        allowedSites: fields.overlayAllowedSites.value
          .split('\n')
          .map((line) => line.trim().toLowerCase())
          .filter(Boolean)
      },
      links: {
        dashboardUrl: fields.dashboardUrl.value.trim()
      }
    };

    const hasPartialCoordinates =
      (nextSettings.location.latitude !== null && nextSettings.location.longitude === null) ||
      (nextSettings.location.latitude === null && nextSettings.location.longitude !== null);

    if (hasPartialCoordinates) {
      throw new Error('Latitude and longitude must both be set or both be empty.');
    }

    validateUrlField('QuakeShield events URL', nextSettings.sources.quakeShield.eventsUrl, nextSettings.sources.quakeShield.enabled);
    validateUrlField('Official feed URL', nextSettings.sources.official.feedUrl, nextSettings.sources.official.enabled);
    validateUrlField('Dashboard URL', nextSettings.links.dashboardUrl, false);

    await requestOptionalOriginsIfNeeded(nextSettings);
    settings = await saveSettings(nextSettings);
    fields.saveStatus.style.color = '#22c55e';
    fields.saveStatus.textContent = `Saved ${new Date().toLocaleTimeString()}`;
  } catch (error) {
    fields.saveStatus.style.color = '#fca5a5';
    fields.saveStatus.textContent = String(error?.message || error);
  }
}

async function init() {
  settings = await getSettings();
  fillForm();
  fields.saveBtn.addEventListener('click', save);
}

init();
