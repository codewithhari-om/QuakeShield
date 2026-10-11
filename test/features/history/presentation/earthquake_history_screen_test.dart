import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:quakeshield_app/features/history/data/earthquake_catalog_repository.dart';
import 'package:quakeshield_app/features/history/domain/earthquake_event.dart';
import 'package:quakeshield_app/features/history/presentation/earthquake_history_screen.dart';

void main() {
  testWidgets('shows source records supplied by the repository', (
    tester,
  ) async {
    await tester.pumpWidget(
      MaterialApp(
        home: EarthquakeHistoryScreen(
          showMap: false,
          repository: _SuccessRepository(),
        ),
      ),
    );
    await tester.pumpAndSettle();

    expect(find.text('Test event, Mizoram, India'), findsOneWidget);
    expect(find.textContaining('1 RECORD'), findsOneWidget);
  });

  testWidgets('shows an empty state after filters remove all source records', (
    tester,
  ) async {
    await tester.pumpWidget(
      MaterialApp(
        home: EarthquakeHistoryScreen(
          showMap: false,
          repository: _SuccessRepository(),
        ),
      ),
    );
    await tester.pumpAndSettle();

    await tester.enterText(find.byType(TextField).first, '9');
    await tester.pump();
    expect(find.text('NO MATCHING RECORDS'), findsOneWidget);
  });
}

class _SuccessRepository implements EarthquakeCatalogRepository {
  @override
  Future<CatalogResult> fetchCatalog() async => CatalogSuccess(
    sourceLabel: 'Test source only',
    fetchedAt: DateTime(2026, 1, 1),
    events: [
      EarthquakeEvent(
        occurredAt: DateTime(2026, 1, 1),
        location: 'Test event, Mizoram, India',
        magnitude: 4.2,
        depthKm: 10,
        latitude: 23.2,
        longitude: 92.7,
      ),
    ],
  );
}
