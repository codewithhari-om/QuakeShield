import 'package:flutter/material.dart';

import '../../domain/earthquake_filter.dart';

class HistoryFilters extends StatelessWidget {
  const HistoryFilters({
    required this.filter,
    required this.onChanged,
    super.key,
  });

  final EarthquakeFilter filter;
  final ValueChanged<EarthquakeFilter> onChanged;

  @override
  Widget build(BuildContext context) {
    return Card(
      color: const Color(0xFF1D2A35),
      child: Padding(
        padding: const EdgeInsets.all(14),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'FILTERS',
              style: TextStyle(fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 10),
            Wrap(
              spacing: 8,
              children: HistoryRegion.values
                  .map(
                    (region) => ChoiceChip(
                      label: Text(_regionLabel(region)),
                      selected: filter.region == region,
                      onSelected: (_) =>
                          onChanged(filter.copyWith(region: region)),
                    ),
                  )
                  .toList(),
            ),
            const SizedBox(height: 8),
            OutlinedButton.icon(
              onPressed: () => _selectDateRange(context),
              icon: const Icon(Icons.date_range_outlined),
              label: Text(_dateLabel()),
            ),
            const SizedBox(height: 4),
            Row(
              children: [
                Expanded(
                  child: _NumberField(
                    label: 'Min magnitude',
                    initialValue: filter.minimumMagnitude,
                    onChanged: (value) => onChanged(
                      filter.copyWith(
                        minimumMagnitude: value,
                        clearMinimumMagnitude: value == null,
                      ),
                    ),
                  ),
                ),
                const SizedBox(width: 10),
                Expanded(
                  child: _NumberField(
                    label: 'Min depth km',
                    initialValue: filter.minimumDepthKm,
                    onChanged: (value) => onChanged(
                      filter.copyWith(
                        minimumDepthKm: value,
                        clearMinimumDepth: value == null,
                      ),
                    ),
                  ),
                ),
                const SizedBox(width: 10),
                Expanded(
                  child: _NumberField(
                    label: 'Max depth km',
                    initialValue: filter.maximumDepthKm,
                    onChanged: (value) => onChanged(
                      filter.copyWith(
                        maximumDepthKm: value,
                        clearMaximumDepth: value == null,
                      ),
                    ),
                  ),
                ),
              ],
            ),
            Align(
              alignment: Alignment.centerRight,
              child: TextButton(
                onPressed: () => onChanged(const EarthquakeFilter()),
                child: const Text('Clear filters'),
              ),
            ),
            const Text(
              'Regions use source location text. Missing numeric values do not '
              'match active numeric filters.',
              style: TextStyle(color: Colors.white60, fontSize: 11),
            ),
          ],
        ),
      ),
    );
  }

  Future<void> _selectDateRange(BuildContext context) async {
    final now = DateTime.now();
    final selected = await showDateRangePicker(
      context: context,
      firstDate: DateTime(1900),
      lastDate: DateTime(now.year + 1),
      initialDateRange: filter.startDate == null || filter.endDate == null
          ? null
          : DateTimeRange(start: filter.startDate!, end: filter.endDate!),
    );
    if (selected != null) {
      onChanged(
        filter.copyWith(startDate: selected.start, endDate: selected.end),
      );
    }
  }

  String _dateLabel() {
    if (filter.startDate == null || filter.endDate == null) return 'Any date';
    return '${_shortDate(filter.startDate!)} – ${_shortDate(filter.endDate!)}';
  }

  String _shortDate(DateTime value) =>
      '${value.year}-${value.month.toString().padLeft(2, '0')}-${value.day.toString().padLeft(2, '0')}';

  String _regionLabel(HistoryRegion region) => switch (region) {
    HistoryRegion.mizoram => 'Mizoram',
    HistoryRegion.northeastIndia => 'Northeast India',
    HistoryRegion.allIndia => 'All India',
  };
}

class _NumberField extends StatefulWidget {
  const _NumberField({
    required this.label,
    required this.initialValue,
    required this.onChanged,
  });

  final String label;
  final double? initialValue;
  final ValueChanged<double?> onChanged;

  @override
  State<_NumberField> createState() => _NumberFieldState();
}

class _NumberFieldState extends State<_NumberField> {
  late final TextEditingController _controller = TextEditingController(
    text: widget.initialValue?.toString() ?? '',
  );

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return TextField(
      controller: _controller,
      keyboardType: const TextInputType.numberWithOptions(decimal: true),
      decoration: InputDecoration(labelText: widget.label, isDense: true),
      onChanged: (text) => widget.onChanged(double.tryParse(text.trim())),
    );
  }
}
