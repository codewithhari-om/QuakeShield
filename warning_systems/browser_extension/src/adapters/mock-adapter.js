import { normalizeEvent } from '../shared/events.js';

export async function fetchMockEvents(settings) {
  if (!settings.sources.mock.enabled) {
    return { events: [], health: { connected: false, stale: false, status: 'disabled' } };
  }

  const mockEvent = normalizeEvent('mock', {
    id: `test-${new Date().toISOString().slice(0, 13)}`,
    eventType: 'TEST',
    title: 'TEST MODE: Simulated Seismic Alert',
    locationName: settings.location.city || 'Configured Location',
    occurredAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
    magnitude: 5.2,
    affectedAreas: [settings.location.city || 'Configured Location'],
    warningLeadSeconds: 18,
    isTest: true,
    status: 'test_mode'
  });

  return {
    events: [mockEvent].filter(Boolean),
    health: {
      connected: true,
      stale: false,
      status: 'connected',
      updatedAt: new Date().toISOString(),
      reason: 'TEST MODE only'
    }
  };
}
