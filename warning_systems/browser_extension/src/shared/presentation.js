import { STATUS, EVENT_TYPES } from './config.js';

export function getStatusPresentation(status, context = {}) {
  const hasLocation = Boolean(context.hasLocation);

  if (status === STATUS.allClear && !hasLocation) {
    return {
      label: 'STATUS UNKNOWN',
      tone: 'unknown',
      message: 'Set a location to evaluate whether events are relevant to your area.'
    };
  }

  switch (status) {
    case STATUS.allClear:
      return {
        label: 'ALL CLEAR',
        tone: 'ok',
        message: 'No relevant active alert is currently known.'
      };
    case STATUS.watch:
      return {
        label: 'WATCH',
        tone: 'watch',
        message: 'Potential relevant event detected. Monitor updates closely.'
      };
    case STATUS.alert:
      return {
        label: 'EARTHQUAKE ALERT',
        tone: 'alert',
        message: 'Validated alert criteria met for your configured area.'
      };
    case STATUS.test:
      return {
        label: 'TEST MODE',
        tone: 'test',
        message: 'TEST MODE is active. Alerts are simulated only.'
      };
    default:
      return {
        label: 'DATA UNAVAILABLE',
        tone: 'unknown',
        message: 'Latest status cannot be verified. Data may be stale or unavailable.'
      };
  }
}

export function formatDate(value) {
  if (!value) return '--';
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return '--';
  return date.toLocaleString();
}

export function formatSourceStatus(source) {
  if (!source) return 'Unknown';
  if (source.status === 'permission_required') return 'Permission Required';
  if (source.status === 'disabled') return 'Disabled';
  if (!source.connected || source.status === 'unavailable') return 'Unavailable';
  if (source.stale) return 'Delayed';
  return 'Connected';
}

export function notificationTitleForEvent(event) {
  if (!event || event.isTest || event.sourceType === EVENT_TYPES.test) return 'QuakeShield TEST MODE Alert';
  if (event.sourceType === EVENT_TYPES.earlyWarning) return 'QuakeShield EARLY WARNING';
  if (event.sourceType === EVENT_TYPES.preliminary) return 'QuakeShield Preliminary Detection';
  return 'QuakeShield Earthquake Report';
}

export function notificationDescriptorForEvent(event) {
  if (!event || event.isTest || event.sourceType === EVENT_TYPES.test) {
    return 'Simulated test alert';
  }
  if (event.sourceType === EVENT_TYPES.earlyWarning) {
    return 'Validated warning signal';
  }
  if (event.sourceType === EVENT_TYPES.preliminary) {
    return 'Preliminary automated detection';
  }
  return 'Confirmed earthquake report';
}
