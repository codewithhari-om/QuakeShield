import { EVENT_TYPES, STATUS } from './config.js';
import { haversineDistanceKm, hasCoordinates, eventMatchesArea } from './geo.js';
import { isStale } from './time.js';

function parseMagnitude(value) {
  if (value === null || value === undefined) return null;
  const numeric = Number(value);
  return Number.isFinite(numeric) ? numeric : null;
}

function pickType(eventType, fallback = EVENT_TYPES.confirmed) {
  const upper = String(eventType || '').toUpperCase();
  if (upper.includes('EARLY')) return EVENT_TYPES.earlyWarning;
  if (upper.includes('PRELIM')) return EVENT_TYPES.preliminary;
  if (upper.includes('TEST')) return EVENT_TYPES.test;
  return fallback;
}

export function normalizeEvent(source, rawEvent) {
  if (!rawEvent || typeof rawEvent !== 'object') return null;
  const id = String(rawEvent.id || rawEvent.eventId || rawEvent.code || '').trim();
  if (!id) return null;

  const latitude = Number(rawEvent.latitude ?? rawEvent.lat ?? rawEvent.location?.lat ?? rawEvent.coordinates?.lat);
  const longitude = Number(rawEvent.longitude ?? rawEvent.lon ?? rawEvent.lng ?? rawEvent.location?.lon ?? rawEvent.coordinates?.lon);
  const hasCoords = Number.isFinite(latitude) && Number.isFinite(longitude);

  const eventType = pickType(rawEvent.eventType || rawEvent.type || rawEvent.statusType);
  const isTest = Boolean(rawEvent.isTest || eventType === EVENT_TYPES.test || rawEvent.mode === 'TEST_MODE');

  return {
    id: `${source}:${id}`,
    canonicalId: id,
    source,
    sourceType: eventType,
    title: rawEvent.title || rawEvent.summary || rawEvent.place || 'Earthquake Event',
    locationName: rawEvent.locationName || rawEvent.place || rawEvent.location?.name || null,
    coordinates: hasCoords ? { lat: latitude, lon: longitude } : null,
    affectedAreas: Array.isArray(rawEvent.affectedAreas)
      ? rawEvent.affectedAreas.filter(Boolean)
      : (typeof rawEvent.affectedArea === 'string' ? [rawEvent.affectedArea] : []),
    magnitude: parseMagnitude(rawEvent.magnitude ?? rawEvent.mag),
    occurredAt: rawEvent.occurredAt || rawEvent.time || rawEvent.timestamp || null,
    updatedAt: rawEvent.updatedAt || rawEvent.lastUpdated || rawEvent.time || rawEvent.timestamp || null,
    warningLeadSeconds:
      Number.isFinite(Number(rawEvent.warningLeadSeconds)) ? Number(rawEvent.warningLeadSeconds) : null,
    url: rawEvent.url || rawEvent.detailsUrl || null,
    status: rawEvent.status || null,
    isTest,
    rawEvent
  };
}

export function mergeDuplicateEvents(events) {
  const bucket = new Map();
  for (const event of events) {
    if (!event) continue;
    const roundedMagnitude = event.magnitude === null ? 'na' : String(Math.round(event.magnitude * 10));
    const roundedLat = event.coordinates ? String(Math.round(event.coordinates.lat * 10)) : 'na';
    const roundedLon = event.coordinates ? String(Math.round(event.coordinates.lon * 10)) : 'na';
    const minute = event.occurredAt ? String(Math.floor(new Date(event.occurredAt).getTime() / 60000)) : 'na';
    const key = `${minute}:${roundedMagnitude}:${roundedLat}:${roundedLon}`;

    if (!bucket.has(key)) {
      bucket.set(key, { ...event, matchedSources: [event.source] });
      continue;
    }

    const current = bucket.get(key);
    const merged = {
      ...current,
      matchedSources: Array.from(new Set([...(current.matchedSources || []), event.source])),
      warningLeadSeconds: current.warningLeadSeconds ?? event.warningLeadSeconds,
      magnitude: current.magnitude ?? event.magnitude,
      locationName: current.locationName || event.locationName,
      affectedAreas: Array.from(new Set([...(current.affectedAreas || []), ...(event.affectedAreas || [])])),
      sourceType: current.sourceType === 'EARLY_WARNING' || event.sourceType !== 'EARLY_WARNING' ? current.sourceType : event.sourceType,
      isTest: current.isTest && event.isTest
    };
    bucket.set(key, merged);
  }

  return Array.from(bucket.values());
}

export function scoreEventRelevance(event, settings, location) {
  const thresholdKm = settings.distanceThresholdKm;
  const thresholdMag = settings.magnitudeThreshold;
  let distanceKm = null;
  let locationMatch = false;

  if (event.coordinates && hasCoordinates(location)) {
    distanceKm = haversineDistanceKm(location.latitude, location.longitude, event.coordinates.lat, event.coordinates.lon);
    locationMatch = distanceKm !== null && distanceKm <= thresholdKm;
  } else if (location?.city) {
    locationMatch = eventMatchesArea(event, location.city);
  }

  const magnitudePass = event.magnitude === null || event.magnitude >= thresholdMag;
  const sourceAgreement = (event.matchedSources || [event.source]).length >= settings.minimumSourceAgreement;
  const relevant = locationMatch && magnitudePass && sourceAgreement;

  return {
    relevant,
    distanceKm,
    magnitudePass,
    locationMatch,
    sourceAgreement
  };
}

export function deriveStatus(events, checks, sourceHealth, settings) {
  if (settings.sources.mock.enabled) {
    return STATUS.test;
  }

  const hasHealthySource = Object.values(sourceHealth || {}).some((s) => s.connected && !s.stale);
  if (!hasHealthySource) return STATUS.unknown;

  const relevantEvents = events.filter((event) => checks.get(event.id)?.relevant);
  if (!relevantEvents.length) return STATUS.allClear;

  const hasEarlyWarning = relevantEvents.some((event) => event.sourceType === EVENT_TYPES.earlyWarning);
  if (hasEarlyWarning) return STATUS.alert;

  const hasPreliminary = relevantEvents.some((event) => event.sourceType === EVENT_TYPES.preliminary);
  if (hasPreliminary) return STATUS.watch;

  return STATUS.watch;
}

export function filterFreshEvents(events, maxEventAgeMinutes, nowMs) {
  return events.filter((event) => !isStale(event.occurredAt, maxEventAgeMinutes, nowMs));
}
