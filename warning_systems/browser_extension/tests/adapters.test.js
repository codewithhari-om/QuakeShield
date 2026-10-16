import test from 'node:test';
import assert from 'node:assert/strict';

import { DEFAULT_SETTINGS } from '../src/shared/config.js';
import { deepMerge } from '../src/shared/storage.js';
import { fetchOfficialEvents } from '../src/adapters/usgs-adapter.js';
import { fetchQuakeShieldEvents } from '../src/adapters/quakeshield-adapter.js';

function withMockFetch(mockImpl, fn) {
  const originalFetch = globalThis.fetch;
  globalThis.fetch = mockImpl;
  return Promise.resolve()
    .then(fn)
    .finally(() => {
      globalThis.fetch = originalFetch;
    });
}

test('quakeshield adapter returns permission_required without endpoint', async () => {
  const settings = deepMerge(DEFAULT_SETTINGS, {
    sources: {
      quakeShield: { enabled: true, eventsUrl: '' }
    }
  });

  const result = await fetchQuakeShieldEvents(settings);
  assert.equal(result.health.status, 'permission_required');
  assert.equal(result.events.length, 0);
});

test('quakeshield adapter handles network errors', async () => {
  const settings = deepMerge(DEFAULT_SETTINGS, {
    sources: {
      quakeShield: { enabled: true, eventsUrl: 'https://backend.example/events' }
    }
  });

  await withMockFetch(
    async () => {
      throw new Error('network down');
    },
    async () => {
      const result = await fetchQuakeShieldEvents(settings);
      assert.equal(result.health.status, 'unavailable');
      assert.equal(result.events.length, 0);
    }
  );
});

test('official adapter maps geojson features', async () => {
  const settings = deepMerge(DEFAULT_SETTINGS, {
    sources: {
      official: {
        enabled: true,
        feedUrl: 'https://earthquake.example/feed'
      }
    }
  });

  const payload = {
    metadata: { generated: 1700000000000 },
    features: [
      {
        id: 'us7000abcd',
        properties: {
          code: 'abcd',
          status: 'reviewed',
          title: 'M 4.6 - offshore',
          place: 'Offshore Test Area',
          mag: 4.6,
          time: 1700000000000,
          updated: 1700000002000,
          url: 'https://example.org/event/us7000abcd'
        },
        geometry: {
          coordinates: [138.3, 35.2, 10]
        }
      }
    ]
  };

  await withMockFetch(
    async () => ({ ok: true, json: async () => payload }),
    async () => {
      const result = await fetchOfficialEvents(settings);
      assert.equal(result.health.status, 'connected');
      assert.equal(result.events.length, 1);
      assert.equal(result.events[0].sourceType, 'CONFIRMED_REPORT');
    }
  );
});
