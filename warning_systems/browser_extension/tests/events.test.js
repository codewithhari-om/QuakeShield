import test from 'node:test';
import assert from 'node:assert/strict';

import { deepMerge } from '../src/shared/storage.js';
import { normalizeEvent, mergeDuplicateEvents, scoreEventRelevance, filterFreshEvents, deriveStatus } from '../src/shared/events.js';
import { DEFAULT_SETTINGS, STATUS } from '../src/shared/config.js';

const baseSettings = {
  ...DEFAULT_SETTINGS,
  distanceThresholdKm: 200,
  magnitudeThreshold: 4,
  location: {
    mode: 'manual',
    city: 'Tokyo',
    latitude: 35.6764,
    longitude: 139.6500,
    permission: 'granted'
  }
};

test('deepMerge preserves defaults and applies updates', () => {
  const merged = deepMerge(DEFAULT_SETTINGS, { notifications: { enabled: false } });
  assert.equal(merged.notifications.enabled, false);
  assert.equal(merged.notifications.allowReports, true);
});

test('normalizeEvent maps mixed schemas', () => {
  const event = normalizeEvent('quakeshield', {
    id: 'abc-1',
    eventType: 'EARLY_WARNING',
    location: { lat: 35, lon: 140, name: 'Near Tokyo' },
    magnitude: 5.8,
    occurredAt: '2026-01-01T00:00:00Z'
  });

  assert.equal(event.id, 'quakeshield:abc-1');
  assert.equal(event.sourceType, 'EARLY_WARNING');
  assert.equal(event.coordinates.lat, 35);
});

test('mergeDuplicateEvents combines same event from two sources', () => {
  const events = [
    normalizeEvent('quakeshield', {
      id: 'one',
      magnitude: 5,
      latitude: 34,
      longitude: 139,
      occurredAt: '2026-01-01T00:00:10Z'
    }),
    normalizeEvent('official', {
      id: 'two',
      magnitude: 5.01,
      latitude: 34.02,
      longitude: 139.03,
      occurredAt: '2026-01-01T00:00:30Z'
    })
  ];

  const merged = mergeDuplicateEvents(events);
  assert.equal(merged.length, 1);
  assert.deepEqual(merged[0].matchedSources.sort(), ['official', 'quakeshield']);
});

test('scoreEventRelevance evaluates location and magnitude thresholds', () => {
  const event = normalizeEvent('official', {
    id: 'nearby',
    magnitude: 4.8,
    latitude: 35.7,
    longitude: 139.7,
    occurredAt: '2026-01-01T00:00:00Z'
  });

  const score = scoreEventRelevance(event, baseSettings, baseSettings.location);
  assert.equal(score.relevant, true);
  assert.equal(score.locationMatch, true);
  assert.equal(score.magnitudePass, true);
});

test('filterFreshEvents removes stale entries', () => {
  const now = Date.parse('2026-01-01T02:00:00Z');
  const fresh = normalizeEvent('official', {
    id: 'fresh',
    magnitude: 5,
    occurredAt: '2026-01-01T01:50:00Z'
  });
  const stale = normalizeEvent('official', {
    id: 'stale',
    magnitude: 5,
    occurredAt: '2025-12-31T22:00:00Z'
  });

  const filtered = filterFreshEvents([fresh, stale], 120, now);
  assert.equal(filtered.length, 1);
  assert.equal(filtered[0].canonicalId, 'fresh');
});

test('deriveStatus does not return all clear when all sources are stale', () => {
  const checks = new Map();
  const status = deriveStatus(
    [],
    checks,
    {
      quakeShield: { connected: false, stale: true },
      official: { connected: true, stale: true }
    },
    deepMerge(baseSettings, { sources: { mock: { enabled: false } } })
  );

  assert.equal(status, STATUS.unknown);
});
