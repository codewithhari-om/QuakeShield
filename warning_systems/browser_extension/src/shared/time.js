export function nowMs() {
  return Date.now();
}

export function toIso(ts) {
  if (!ts) return null;
  const date = typeof ts === 'number' ? new Date(ts) : new Date(String(ts));
  if (Number.isNaN(date.getTime())) return null;
  return date.toISOString();
}

export function minutesSince(iso, currentMs = nowMs()) {
  if (!iso) return Number.POSITIVE_INFINITY;
  const value = new Date(iso).getTime();
  if (Number.isNaN(value)) return Number.POSITIVE_INFINITY;
  return Math.max(0, (currentMs - value) / 60000);
}

export function isStale(iso, staleAfterMinutes, currentMs = nowMs()) {
  return minutesSince(iso, currentMs) > staleAfterMinutes;
}
