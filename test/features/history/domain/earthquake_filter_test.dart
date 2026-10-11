import 'package:flutter_test/flutter_test.dart';
import 'package:quakeshield_app/features/history/domain/earthquake_event.dart';
import 'package:quakeshield_app/features/history/domain/earthquake_filter.dart';

void main() {
  final mizoramEvent = EarthquakeEvent(
    occurredAt: DateTime(2026, 1, 10, 9),
    location: 'Test location, Mizoram, India',
    magnitude: 4.2,
    depthKm: 12,
    latitude: 23.2,
    longitude: 92.7,
  );

  test('Mizoram filter uses source location text and numeric filters', () {
    const filter = EarthquakeFilter(
      region: HistoryRegion.mizoram,
      minimumMagnitude: 4,
      minimumDepthKm: 10,
      maximumDepthKm: 20,
    );

    expect(filter.matches(mizoramEvent), isTrue);
    expect(
      filter.matches(
        EarthquakeEvent(
          occurredAt: DateTime(2026, 1, 10),
          location: 'Test location, Assam, India',
          magnitude: 4.5,
          depthKm: 12,
        ),
      ),
      isFalse,
    );
  });

  test(
    'events without required source values do not match numeric filters',
    () {
      const filter = EarthquakeFilter(minimumMagnitude: 3);
      final event = EarthquakeEvent(
        occurredAt: DateTime(2026, 1, 10),
        location: 'Test location, Mizoram, India',
      );

      expect(filter.matches(event), isFalse);
    },
  );
}
