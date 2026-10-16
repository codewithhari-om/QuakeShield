import { formatDate } from '../shared/presentation.js';

const ui = {
  stateSummary: document.getElementById('stateSummary'),
  eventPanel: document.getElementById('eventPanel'),
  eventType: document.getElementById('eventType'),
  eventMagnitude: document.getElementById('eventMagnitude'),
  eventLocation: document.getElementById('eventLocation'),
  eventDistance: document.getElementById('eventDistance'),
  eventOccurred: document.getElementById('eventOccurred'),
  eventUpdated: document.getElementById('eventUpdated'),
  eventSource: document.getElementById('eventSource'),
  eventLead: document.getElementById('eventLead'),
  eventLimitNote: document.getElementById('eventLimitNote'),
  eventExternalLink: document.getElementById('eventExternalLink')
};

function selectEvent(state, eventId) {
  if (!state) return null;
  if (eventId) {
    const found = (state.events || []).find((event) => event.id === eventId);
    if (found) {
      const focusedDistance = state.focusedEvent?.id === found.id ? state.focusedEvent.distanceKm : null;
      return { ...found, distanceKm: focusedDistance };
    }
  }
  return state.focusedEvent || null;
}

function renderEvent(event, state) {
  if (!event) {
    ui.eventPanel.hidden = true;
    ui.stateSummary.textContent = 'No relevant event available in extension state.';
    return;
  }

  ui.eventPanel.hidden = false;
  ui.stateSummary.textContent = `Status: ${state?.status || 'UNKNOWN'} • Last successful update: ${formatDate(state?.lastSuccessfulUpdate || state?.generatedAt)}`;

  ui.eventType.textContent = event.sourceType || '--';
  ui.eventMagnitude.textContent = event.magnitude === null ? 'Unavailable' : `M${event.magnitude.toFixed(1)}`;
  ui.eventLocation.textContent = event.locationName || 'Unknown';
  ui.eventDistance.textContent = event.distanceKm === null ? 'Unavailable' : `${event.distanceKm.toFixed(1)} km`;
  ui.eventOccurred.textContent = formatDate(event.occurredAt);
  ui.eventUpdated.textContent = formatDate(event.updatedAt || event.occurredAt);
  ui.eventSource.textContent = `${event.source}${event.matchedSources?.length ? ` (${event.matchedSources.join(', ')})` : ''}`;
  ui.eventLead.textContent = Number.isFinite(event.warningLeadSeconds) && event.warningLeadSeconds > 0
    ? `${event.warningLeadSeconds}s (backend-provided estimate)`
    : 'Unavailable';

  ui.eventLimitNote.textContent = event.isTest
    ? 'TEST MODE event: this is simulated and not a real emergency.'
    : event.sourceType === 'EARLY_WARNING'
      ? 'Early warning shown only when source classification indicates a warning event.'
      : 'This event may be a report or preliminary detection and not guaranteed advance warning.';

  if (event.url) {
    ui.eventExternalLink.hidden = false;
    ui.eventExternalLink.href = event.url;
  } else {
    ui.eventExternalLink.hidden = true;
  }
}

async function init() {
  const response = await chrome.runtime.sendMessage({ type: 'QS_GET_STATE' });
  const state = response?.state || null;
  const params = new URLSearchParams(window.location.search);
  const eventId = params.get('eventId');
  const selected = selectEvent(state, eventId);
  renderEvent(selected, state);
}

init();
