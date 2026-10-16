import { fetchQuakeShieldEvents } from './quakeshield-adapter.js';
import { fetchOfficialEvents } from './usgs-adapter.js';
import { fetchMockEvents } from './mock-adapter.js';

export async function fetchAllSources(settings) {
  const [quakeShield, official, mock] = await Promise.all([
    fetchQuakeShieldEvents(settings),
    fetchOfficialEvents(settings),
    fetchMockEvents(settings)
  ]);

  return {
    events: [...quakeShield.events, ...official.events, ...mock.events],
    health: {
      quakeShield: quakeShield.health,
      official: official.health,
      mock: mock.health
    }
  };
}
