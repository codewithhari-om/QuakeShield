import { STATUS } from '../shared/config.js';
import { getSettings, saveSettings } from '../shared/storage.js';
import { formatDate, formatSourceStatus, getStatusPresentation } from '../shared/presentation.js';

const ui = {
  openSettings: document.getElementById('openSettings'),
  openPreferences: document.getElementById('openPreferences'),
  useGeolocation: document.getElementById('useGeolocation'),
  clearLocation: document.getElementById('clearLocation'),
  manualForm: document.getElementById('manualLocationForm'),
  manualCity: document.getElementById('manualCity'),
  manualLat: document.getElementById('manualLat'),
  manualLon: document.getElementById('manualLon'),
  locationFormError: document.getElementById('locationFormError'),
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

function formatLocation(settingsLocation) {
  if (settingsLocation.mode === 'geolocation' && settingsLocation.city) {
    return `${settingsLocation.city} (browser location)`;
  }
  if (settingsLocation.mode === 'manual' && settingsLocation.city) {
    return `${settingsLocation.city} (manual)`;
  }
  return 'No location selected';
}

function hasLocationConfigured(location) {
  return Boolean(location?.city) || (typeof location?.latitude === 'number' && typeof location?.longitude === 'number');
}

function renderLocation() {
  const location = settings.location;
  ui.locationPermission.textContent = `Permission: ${location.permission}`;
  ui.locationValue.textContent = formatLocation(location);
  ui.toggleOverlay.textContent = settings.overlay.enabled ? 'Disable Overlay' : 'Enable Overlay';
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
      <span class="source-health">${formatSourceStatus(source)}</span>
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
    ui.warningLead.textContent = `${event.warningLeadSeconds}s (backend-provided estimate)`;
  } else {
    ui.warningLeadWrap.hidden = true;
    ui.warningLead.textContent = '--';
  }
}

function renderStatus(state) {
  const status = state?.status || STATUS.unknown;
  ui.statusCard.classList.remove('watch', 'alert', 'unknown', 'test');

  const presentation = getStatusPresentation(status, {
    hasLocation: hasLocationConfigured(settings.location)
  });

  if (presentation.tone !== 'ok') {
    ui.statusCard.classList.add(presentation.tone);
  }

  ui.statusBadge.textContent = presentation.label;
  ui.lastUpdate.textContent = `Last update: ${formatDate(state?.lastSuccessfulUpdate || state?.generatedAt)}`;
  ui.statusMessage.textContent = presentation.message;

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
  if (!navigator.geolocation) {
    ui.locationFormError.hidden = false;
    ui.locationFormError.textContent = 'Geolocation is not available in this environment.';
    return;
  }

  navigator.geolocation.getCurrentPosition(
    async (position) => {
      ui.locationFormError.hidden = true;
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
      ui.locationFormError.hidden = false;
      ui.locationFormError.textContent = 'Location permission denied. Use manual location entry instead.';
      renderLocation();
    },
    { enableHighAccuracy: false, timeout: 7000, maximumAge: 300000 }
  );
}

async function saveManualLocation(event) {
  event.preventDefault();
  const city = ui.manualCity.value.trim();
  const latRaw = ui.manualLat.value.trim();
  const lonRaw = ui.manualLon.value.trim();

  if (!city) {
    ui.locationFormError.hidden = false;
    ui.locationFormError.textContent = 'Please provide a city or area name.';
    return;
  }

  const lat = latRaw === '' ? null : Number(latRaw);
  const lon = lonRaw === '' ? null : Number(lonRaw);
  const bothEmpty = latRaw === '' && lonRaw === '';
  const bothProvided = Number.isFinite(lat) && Number.isFinite(lon);

  if (!bothEmpty && !bothProvided) {
    ui.locationFormError.hidden = false;
    ui.locationFormError.textContent = 'Latitude and longitude must both be valid numbers, or both left blank.';
    return;
  }

  ui.locationFormError.hidden = true;
  settings = await saveSettings({
    location: {
      mode: 'manual',
      city,
      latitude: bothProvided ? lat : null,
      longitude: bothProvided ? lon : null,
      permission: settings.location.permission || 'prompt'
    }
  });

  ui.manualForm.reset();
  renderLocation();
  await forceRefresh();
}

async function clearLocation() {
  ui.locationFormError.hidden = true;
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
  renderLocation();
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
  const eventId = currentState?.focusedEvent?.id;
  const detailsUrl = chrome.runtime.getURL(`src/popup/event-details.html${eventId ? `?eventId=${encodeURIComponent(eventId)}` : ''}`);
  chrome.tabs.create({ url: detailsUrl });
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
