export const DEFAULT_SETTINGS = {
  pollingIntervalSeconds: 120,
  staleAfterMinutes: 10,
  maxEventAgeMinutes: 120,
  distanceThresholdKm: 300,
  magnitudeThreshold: 3.5,
  minimumSourceAgreement: 1,
  location: {
    mode: 'none',
    city: '',
    latitude: null,
    longitude: null,
    permission: 'prompt'
  },
  notifications: {
    enabled: true,
    playSound: true,
    allowPreliminary: true,
    allowReports: true,
    allowEarlyWarnings: true,
    includeTestMode: false
  },
  overlay: {
    enabled: false,
    allowedSites: [],
    dismissForSession: true
  },
  sources: {
    quakeShield: {
      enabled: true,
      eventsUrl: '',
      apiKey: '',
      sourceLabel: 'QuakeShield Backend'
    },
    official: {
      enabled: true,
      feedUrl: 'https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson',
      sourceLabel: 'USGS Earthquake Feed',
      updateCadence: 'Approx. 1 min feed refresh',
      licensing: 'Public-domain U.S. government data (verify for deployment region)'
    },
    mock: {
      enabled: false
    }
  },
  links: {
    dashboardUrl: ''
  }
};

export const STORAGE_KEYS = {
  settings: 'qs_settings',
  state: 'qs_state',
  notifiedEvents: 'qs_notified_events'
};

export const STATUS = {
  allClear: 'ALL_CLEAR',
  watch: 'WATCH',
  alert: 'EARTHQUAKE_ALERT',
  unknown: 'DATA_UNAVAILABLE',
  test: 'TEST_MODE'
};

export const EVENT_TYPES = {
  confirmed: 'CONFIRMED_REPORT',
  preliminary: 'PRELIMINARY_DETECTION',
  earlyWarning: 'EARLY_WARNING',
  test: 'TEST'
};
