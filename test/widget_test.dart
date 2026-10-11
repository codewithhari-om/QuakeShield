import 'package:flutter_test/flutter_test.dart';

import 'package:quakeshield_app/main.dart';

void main() {
  testWidgets('QuakeShield starts on the monitor and opens history', (
    WidgetTester tester,
  ) async {
    await tester.pumpWidget(const QuakeShieldApp());

    expect(find.text('EARTHQUAKE MONITOR'), findsOneWidget);
    expect(find.text('TEST SIMULATED ALERT'), findsOneWidget);

    await tester.tap(find.text('History'));
    await tester.pump(const Duration(milliseconds: 100));

    expect(find.text('EARTHQUAKE HISTORY'), findsOneWidget);
    expect(find.text('OFFICIAL PORTAL ONLY'), findsOneWidget);
  });
}
