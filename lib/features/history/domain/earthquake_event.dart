/// An earthquake record supplied by a catalog source.
///
/// Nullable fields are intentionally preserved as unavailable rather than
/// estimated by QuakeShield.
class EarthquakeEvent {
  const EarthquakeEvent({
    required this.occurredAt,
    required this.location,
    this.id,
    this.magnitude,
    this.depthKm,
    this.latitude,
    this.longitude,
    this.status,
    this.officialDetailUri,
  });

  final String? id;
  final DateTime occurredAt;
  final String location;
  final double? magnitude;
  final double? depthKm;
  final double? latitude;
  final double? longitude;
  final String? status;
  final Uri? officialDetailUri;

  bool get hasCoordinates => latitude != null && longitude != null;
}
