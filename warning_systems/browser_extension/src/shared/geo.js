const EARTH_RADIUS_KM = 6371;

function toRadians(value) {
  return (value * Math.PI) / 180;
}

export function haversineDistanceKm(lat1, lon1, lat2, lon2) {
  if ([lat1, lon1, lat2, lon2].some((v) => typeof v !== 'number' || Number.isNaN(v))) {
    return null;
  }
  const dLat = toRadians(lat2 - lat1);
  const dLon = toRadians(lon2 - lon1);
  const a =
    Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos(toRadians(lat1)) * Math.cos(toRadians(lat2)) * Math.sin(dLon / 2) * Math.sin(dLon / 2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  return EARTH_RADIUS_KM * c;
}

export function hasCoordinates(location) {
  return (
    location &&
    typeof location.latitude === 'number' &&
    typeof location.longitude === 'number' &&
    !Number.isNaN(location.latitude) &&
    !Number.isNaN(location.longitude)
  );
}

export function eventMatchesArea(event, city) {
  if (!city) return false;
  const needle = city.trim().toLowerCase();
  if (!needle) return false;
  const values = [event.locationName, ...(event.affectedAreas || [])].filter(Boolean).map((v) => v.toLowerCase());
  return values.some((v) => v.includes(needle));
}
