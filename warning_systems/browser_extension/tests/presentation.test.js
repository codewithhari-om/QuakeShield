import test from 'node:test';
import assert from 'node:assert/strict';

import { STATUS, EVENT_TYPES } from '../src/shared/config.js';
import {
  formatSourceStatus,
  getStatusPresentation,
  notificationDescriptorForEvent,
  notificationTitleForEvent
} from '../src/shared/presentation.js';

test('status presentation does not show all-clear when location missing', () => {
  const view = getStatusPresentation(STATUS.allClear, { hasLocation: false });
  assert.equal(view.label, 'STATUS UNKNOWN');
  assert.equal(view.tone, 'unknown');
});

test('status presentation shows all-clear with configured location', () => {
  const view = getStatusPresentation(STATUS.allClear, { hasLocation: true });
  assert.equal(view.label, 'ALL CLEAR');
  assert.equal(view.tone, 'ok');
});

test('source status formatter maps stale/unavailable states', () => {
  assert.equal(formatSourceStatus({ connected: true, stale: false, status: 'connected' }), 'Connected');
  assert.equal(formatSourceStatus({ connected: true, stale: true, status: 'connected' }), 'Delayed');
  assert.equal(formatSourceStatus({ connected: false, stale: true, status: 'unavailable' }), 'Unavailable');
  assert.equal(formatSourceStatus({ connected: false, stale: false, status: 'permission_required' }), 'Permission Required');
});

test('notification wording distinguishes event categories', () => {
  const early = { sourceType: EVENT_TYPES.earlyWarning, isTest: false };
  const prelim = { sourceType: EVENT_TYPES.preliminary, isTest: false };
  const report = { sourceType: EVENT_TYPES.confirmed, isTest: false };
  const mock = { sourceType: EVENT_TYPES.test, isTest: true };

  assert.equal(notificationTitleForEvent(early), 'QuakeShield EARLY WARNING');
  assert.equal(notificationTitleForEvent(prelim), 'QuakeShield Preliminary Detection');
  assert.equal(notificationTitleForEvent(report), 'QuakeShield Earthquake Report');
  assert.equal(notificationTitleForEvent(mock), 'QuakeShield TEST MODE Alert');

  assert.equal(notificationDescriptorForEvent(early), 'Validated warning signal');
  assert.equal(notificationDescriptorForEvent(prelim), 'Preliminary automated detection');
  assert.equal(notificationDescriptorForEvent(report), 'Confirmed earthquake report');
  assert.equal(notificationDescriptorForEvent(mock), 'Simulated test alert');
});
