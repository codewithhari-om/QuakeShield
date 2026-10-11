import 'package:flutter/material.dart';

import '../../domain/earthquake_event.dart';

/// A dependency-free geographic plot for catalog coordinates.
/// It intentionally does not claim to be a navigational or live tile map.
class EarthquakeMap extends StatelessWidget {
  const EarthquakeMap({
    required this.events,
    required this.onEventSelected,
    super.key,
  });

  final List<EarthquakeEvent> events;
  final ValueChanged<EarthquakeEvent> onEventSelected;

  static const _minLatitude = 5.0;
  static const _maxLatitude = 38.0;
  static const _minLongitude = 65.0;
  static const _maxLongitude = 100.0;

  @override
  Widget build(BuildContext context) {
    final mappedEvents = events.where((event) => event.hasCoordinates).toList();
    if (mappedEvents.isEmpty) return const SizedBox.shrink();

    return Semantics(
      label: 'Interactive earthquake coordinate map',
      child: Container(
        height: 260,
        decoration: BoxDecoration(
          color: const Color(0xFF152733),
          borderRadius: BorderRadius.circular(16),
          border: Border.all(color: Colors.cyanAccent.withValues(alpha: 0.3)),
        ),
        child: LayoutBuilder(
          builder: (context, constraints) => Stack(
            children: [
              Positioned.fill(
                child: CustomPaint(painter: _CoordinateGridPainter()),
              ),
              ...mappedEvents.map(
                (event) => Positioned(
                  left: _x(event.longitude!, constraints.maxWidth) - 18,
                  top: _y(event.latitude!, constraints.maxHeight) - 18,
                  child: Semantics(
                    button: true,
                    label: 'Earthquake marker for ${event.location}',
                    child: IconButton(
                      icon: const Icon(
                        Icons.location_on,
                        color: Colors.redAccent,
                        size: 34,
                      ),
                      onPressed: () => onEventSelected(event),
                    ),
                  ),
                ),
              ),
              const Positioned(
                left: 12,
                bottom: 8,
                child: Text(
                  'Approximate coordinate map • tap a marker for details',
                  style: TextStyle(color: Colors.white70, fontSize: 10),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  double _x(double longitude, double width) {
    final clamped = longitude.clamp(_minLongitude, _maxLongitude).toDouble();
    return ((clamped - _minLongitude) / (_maxLongitude - _minLongitude)) *
        width;
  }

  double _y(double latitude, double height) {
    final clamped = latitude.clamp(_minLatitude, _maxLatitude).toDouble();
    return (1 - ((clamped - _minLatitude) / (_maxLatitude - _minLatitude))) *
        height;
  }
}

class _CoordinateGridPainter extends CustomPainter {
  @override
  void paint(Canvas canvas, Size size) {
    final grid = Paint()
      ..color = Colors.white.withValues(alpha: 0.10)
      ..strokeWidth = 1;
    for (var index = 1; index < 6; index++) {
      final fraction = index / 6;
      canvas.drawLine(
        Offset(size.width * fraction, 0),
        Offset(size.width * fraction, size.height),
        grid,
      );
      canvas.drawLine(
        Offset(0, size.height * fraction),
        Offset(size.width, size.height * fraction),
        grid,
      );
    }
    final outline = Paint()
      ..color = Colors.cyanAccent.withValues(alpha: 0.18)
      ..style = PaintingStyle.stroke
      ..strokeWidth = 2;
    final shape = Path()
      ..moveTo(size.width * .38, size.height * .10)
      ..lineTo(size.width * .63, size.height * .18)
      ..lineTo(size.width * .74, size.height * .42)
      ..lineTo(size.width * .59, size.height * .84)
      ..lineTo(size.width * .46, size.height * .94)
      ..lineTo(size.width * .34, size.height * .58)
      ..close();
    canvas.drawPath(shape, outline);
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => false;
}
