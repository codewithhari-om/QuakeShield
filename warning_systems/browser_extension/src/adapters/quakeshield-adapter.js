import { normalizeEvent } from '../shared/events.js';

function normalizeList(payload) {
  if (Array.isArray(payload)) return payload;
  if (Array.isArray(payload?.events)) return payload.events;
  if (Array.isArray(payload?.data?.events)) return payload.data.events;
  return [];
}

export async function fetchQuakeShieldEvents(settings) {
  const sourceSettings = settings.sources.quakeShield;
  if (!sourceSettings?.enabled) {
    return { events: [], health: { connected: false, stale: false, status: 'disabled' } };
  }

  if (!sourceSettings.eventsUrl) {
    return {
      events: [],
      health: {
        connected: false,
        stale: false,
        status: 'permission_required',
        reason: 'No backend endpoint configured.'
      }
    };
  }

  const headers = { Accept: 'application/json' };
  if (sourceSettings.apiKey) {
    headers.Authorization = 'Bearer ' + sourceSettings.apiKey;
  }

  const startedAt = Date.now();
  try {
    const response = await fetch(sourceSettings.eventsUrl, { headers });
    if (!response.ok) {
      return {
        events: [],
        health: {
          connected: false,
          stale: false,
          status: 'unavailable',
          reason: `HTTP ${response.status}`,
          latencyMs: Date.now() - startedAt
        }
      };
    }

    const payload = await response.json();
    const normalized = normalizeList(payload)
      .map((entry) => normalizeEvent('quakeshield', entry))
      .filter(Boolean);

    const latestUpdatedAt = normalized.reduce((latest, event) => {
      const ts = new Date(event.updatedAt || event.occurredAt || 0).getTime();
      return Number.isFinite(ts) && ts > latest ? ts : latest;
    }, 0);

    return {
      events: normalized,
      health: {
        connected: true,
        stale: false,
        status: 'connected',
        updatedAt: latestUpdatedAt ? new Date(latestUpdatedAt).toISOString() : null,
        latencyMs: Date.now() - startedAt
      }
    };
  } catch (error) {
    return {
      events: [],
      health: {
        connected: false,
        stale: false,
        status: 'unavailable',
        reason: String(error?.message || error),
        latencyMs: Date.now() - startedAt
      }
    };
  }
}
