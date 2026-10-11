import 'earthquake_event.dart';

enum HistoryRegion { mizoram, northeastIndia, allIndia }

class EarthquakeFilter {
  const EarthquakeFilter({
    this.region = HistoryRegion.allIndia,
    this.startDate,
    this.endDate,
    this.minimumMagnitude,
    this.minimumDepthKm,
    this.maximumDepthKm,
  });

  final HistoryRegion region;
  final DateTime? startDate;
  final DateTime? endDate;
  final double? minimumMagnitude;
  final double? minimumDepthKm;
  final double? maximumDepthKm;

  EarthquakeFilter copyWith({
    HistoryRegion? region,
    DateTime? startDate,
    DateTime? endDate,
    double? minimumMagnitude,
    double? minimumDepthKm,
    double? maximumDepthKm,
    bool clearDates = false,
    bool clearMinimumMagnitude = false,
    bool clearMinimumDepth = false,
    bool clearMaximumDepth = false,
  }) {
    return EarthquakeFilter(
      region: region ?? this.region,
      startDate: clearDates ? null : startDate ?? this.startDate,
      endDate: clearDates ? null : endDate ?? this.endDate,
      minimumMagnitude: clearMinimumMagnitude
          ? null
          : minimumMagnitude ?? this.minimumMagnitude,
      minimumDepthKm: clearMinimumDepth
          ? null
          : minimumDepthKm ?? this.minimumDepthKm,
      maximumDepthKm: clearMaximumDepth
          ? null
          : maximumDepthKm ?? this.maximumDepthKm,
    );
  }

  bool matches(EarthquakeEvent event) {
    final localDate = event.occurredAt.toLocal();
    if (startDate != null && localDate.isBefore(_startOfDay(startDate!))) {
      return false;
    }
    if (endDate != null && localDate.isAfter(_endOfDay(endDate!))) {
      return false;
    }
    if (minimumMagnitude != null &&
        (event.magnitude == null || event.magnitude! < minimumMagnitude!)) {
      return false;
    }
    if (minimumDepthKm != null &&
        (event.depthKm == null || event.depthKm! < minimumDepthKm!)) {
      return false;
    }
    if (maximumDepthKm != null &&
        (event.depthKm == null || event.depthKm! > maximumDepthKm!)) {
      return false;
    }
    return _matchesRegion(event.location);
  }

  bool _matchesRegion(String location) {
    final normalized = location.toLowerCase();
    if (region == HistoryRegion.mizoram) return normalized.contains('mizoram');
    if (region == HistoryRegion.northeastIndia) {
      return const [
        'arunachal pradesh',
        'assam',
        'manipur',
        'meghalaya',
        'mizoram',
        'nagaland',
        'sikkim',
        'tripura',
      ].any(normalized.contains);
    }
    return _indiaLocationTokens.any(normalized.contains);
  }

  static const _indiaLocationTokens = [
    'india',
    'andaman',
    'andhra pradesh',
    'arunachal pradesh',
    'assam',
    'bihar',
    'chhattisgarh',
    'goa',
    'gujarat',
    'haryana',
    'himachal pradesh',
    'jammu',
    'jharkhand',
    'karnataka',
    'kerala',
    'ladakh',
    'lakshadweep',
    'madhya pradesh',
    'maharashtra',
    'manipur',
    'meghalaya',
    'mizoram',
    'nagaland',
    'odisha',
    'puducherry',
    'punjab',
    'rajasthan',
    'sikkim',
    'tamil nadu',
    'telangana',
    'tripura',
    'uttar pradesh',
    'uttarakhand',
    'west bengal',
  ];

  static DateTime _startOfDay(DateTime value) =>
      DateTime(value.year, value.month, value.day);

  static DateTime _endOfDay(DateTime value) =>
      DateTime(value.year, value.month, value.day, 23, 59, 59, 999);
}
