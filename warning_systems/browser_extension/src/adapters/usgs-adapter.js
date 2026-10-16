import { normalizeEvent } from '../shared/events.js';

function mapFeature(feature) {
  const properties = feature?.properties || {};
  const coords = feature?.geometry?.coordinates || [];
  const statusType = properties.status === 'automatic' ? 'PRELIMINARY_DETECTION' : 'CONFIRMED_REPORT';
  return {
    id: feature.id || properties.code || properties.ids,
    eventType: statusType,
    title: properties.title,
    place: properties.place,
    magnitude: properties.mag,
    time: properties.time,
    updatedAt: properties.updated,
    status: properties.status,
    latitude: coords[1],
    longitude: coords[0],
    url: properties.url,
    affectedAreas: properties.place ? [properties.place] : []
  };
}

export async function fetchOfficialEvents(settings) {
  const sourceSettings = settings.sources.official;
  if (!sourceSettings?.enabled) {
    return { events: [], health: { connected: false, stale: false, status: 'disabled' } };
  }

  const feedUrl = sourceSettings.feedUrl;
  if (!feedUrl) {
    return {
      events: [],
      health: { connected: false, stale: false, status: 'permission_required', reason: 'No official feed URL configured.' }
    };
  }

  const startedAt = Date.now();
  try {
    const response = await fetch(feedUrl, { headers: { Accept: 'application/json' } });
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
    const normalized = (payload?.features || [])
      .map((feature) => normalizeEvent('official', mapFeature(feature)))
      .filter(Boolean);

    return {
      events: normalized,
      health: {
        connected: true,
        stale: false,
        status: 'connected',
        updatedAt: payload?.metadata?.generated ? new Date(payload.metadata.generated).toISOString() : null,
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
