import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

import '../data/earthquake_catalog_repository.dart';
import '../data/ncs_catalog_repository.dart';
import '../domain/earthquake_event.dart';
import '../domain/earthquake_filter.dart';
import 'widgets/catalog_state_panel.dart';
import 'widgets/earthquake_map.dart';
import 'widgets/history_filters.dart';

class EarthquakeHistoryScreen extends StatefulWidget {
  const EarthquakeHistoryScreen({
    this.repository = const NcsOfficialPortalRepository(),
    this.showMap = true,
    super.key,
  });

  final EarthquakeCatalogRepository repository;
  final bool showMap;

  @override
  State<EarthquakeHistoryScreen> createState() =>
      _EarthquakeHistoryScreenState();
}

class _EarthquakeHistoryScreenState extends State<EarthquakeHistoryScreen> {
  CatalogResult? _result;
  EarthquakeFilter _filter = const EarthquakeFilter();
  bool _loading = true;

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    setState(() => _loading = true);
    try {
      final result = await widget.repository.fetchCatalog();
      if (mounted) setState(() => _result = result);
    } catch (_) {
      if (mounted) {
        setState(
          () => _result = CatalogFailure(
            message: 'The catalog could not be loaded. Please try again.',
            officialPortalUri: NcsOfficialPortalRepository.officialPortalUri,
          ),
        );
      }
    } finally {
      if (mounted) setState(() => _loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF101820),
      appBar: AppBar(
        backgroundColor: const Color(0xFF101820),
        title: const Text(
          'EARTHQUAKE HISTORY',
          style: TextStyle(fontWeight: FontWeight.bold, letterSpacing: 1),
        ),
        actions: [
          IconButton(
            tooltip: 'Refresh history',
            onPressed: _loading ? null : _load,
            icon: const Icon(Icons.refresh),
          ),
        ],
      ),
      body: RefreshIndicator(
        onRefresh: _load,
        child: ListView(
          padding: const EdgeInsets.all(16),
          children: [
            const Text(
              'RECORDED EARTHQUAKE HISTORY',
              style: TextStyle(
                color: Colors.cyanAccent,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 6),
            const Text(
              'Historical records are not predictions, live detections, or official warnings.',
              style: TextStyle(color: Colors.white70),
            ),
            const SizedBox(height: 12),
            HistoryFilters(
              filter: _filter,
              onChanged: (filter) => setState(() => _filter = filter),
            ),
            const SizedBox(height: 12),
            _buildContent(),
          ],
        ),
      ),
    );
  }

  Widget _buildContent() {
    if (_loading) {
      return const CatalogStatePanel(
        icon: Icons.hourglass_top,
        title: 'LOADING HISTORY',
        message: 'Checking the configured earthquake catalog source.',
      );
    }
    final result = _result;
    if (result is CatalogUnavailable) return _unavailable(result);
    if (result is CatalogFailure) return _failure(result);
    if (result is! CatalogSuccess) return const SizedBox.shrink();

    final filtered = result.events.where(_filter.matches).toList()
      ..sort((a, b) => b.occurredAt.compareTo(a.occurredAt));
    if (filtered.isEmpty) {
      return CatalogStatePanel(
        icon: Icons.search_off,
        title: 'NO MATCHING RECORDS',
        message: 'No source records match the active filters.',
        action: TextButton(
          onPressed: () => setState(() => _filter = const EarthquakeFilter()),
          child: const Text('Clear filters'),
        ),
      );
    }
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          '${filtered.length} RECORD${filtered.length == 1 ? '' : 'S'} • ${result.sourceLabel}',
          style: const TextStyle(color: Colors.white70, fontSize: 12),
        ),
        if (widget.showMap) ...[
          const SizedBox(height: 12),
          EarthquakeMap(events: filtered, onEventSelected: _showDetails),
        ],
        const SizedBox(height: 12),
        ...filtered.map(
          (event) => Padding(
            padding: const EdgeInsets.only(bottom: 10),
            child: _EventCard(event: event, onTap: () => _showDetails(event)),
          ),
        ),
      ],
    );
  }

  Widget _unavailable(CatalogUnavailable result) => CatalogStatePanel(
    icon: Icons.public_off,
    title: 'OFFICIAL PORTAL ONLY',
    message: result.reason,
    action: Column(
      children: [
        SelectableText(
          result.officialPortalUri.toString(),
          textAlign: TextAlign.center,
          style: const TextStyle(color: Colors.cyanAccent, fontSize: 12),
        ),
        ElevatedButton.icon(
          onPressed: () => _copyOfficialLink(result.officialPortalUri),
          icon: const Icon(Icons.copy_outlined),
          label: const Text('Copy official NCS portal link'),
        ),
      ],
    ),
  );

  Widget _failure(CatalogFailure result) => CatalogStatePanel(
    icon: Icons.error_outline,
    title: 'HISTORY UNAVAILABLE',
    message: result.message,
    action: Wrap(
      alignment: WrapAlignment.center,
      spacing: 8,
      children: [
        OutlinedButton(onPressed: _load, child: const Text('Retry')),
        TextButton(
          onPressed: () => _copyOfficialLink(result.officialPortalUri),
          child: const Text('Copy official portal link'),
        ),
      ],
    ),
  );

  Future<void> _copyOfficialLink(Uri uri) async {
    await Clipboard.setData(ClipboardData(text: uri.toString()));
    if (mounted) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Official NCS link copied.')),
      );
    }
  }

  void _showDetails(EarthquakeEvent event) {
    showModalBottomSheet<void>(
      context: context,
      backgroundColor: const Color(0xFF1D2A35),
      showDragHandle: true,
      builder: (context) => Padding(
        padding: const EdgeInsets.fromLTRB(22, 4, 22, 28),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              event.location,
              style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 19),
            ),
            const SizedBox(height: 14),
            _DetailRow(label: 'Magnitude', value: _number(event.magnitude)),
            _DetailRow(label: 'Occurred', value: _dateTime(event.occurredAt)),
            _DetailRow(
              label: 'Depth',
              value: event.depthKm == null
                  ? 'Not reported'
                  : '${event.depthKm} km',
            ),
            _DetailRow(
              label: 'Coordinates',
              value: event.hasCoordinates
                  ? '${event.latitude}, ${event.longitude}'
                  : 'Not reported',
            ),
            _DetailRow(label: 'Status', value: event.status ?? 'Not reported'),
            if (event.officialDetailUri != null) ...[
              const SizedBox(height: 8),
              TextButton.icon(
                onPressed: () => _copyOfficialLink(event.officialDetailUri!),
                icon: const Icon(Icons.copy_outlined),
                label: const Text('Copy official event detail link'),
              ),
            ],
          ],
        ),
      ),
    );
  }

  String _number(double? value) =>
      value == null ? 'Not reported' : value.toStringAsFixed(1);
  String _dateTime(DateTime value) =>
      '${value.year}-${value.month.toString().padLeft(2, '0')}-${value.day.toString().padLeft(2, '0')} ${value.hour.toString().padLeft(2, '0')}:${value.minute.toString().padLeft(2, '0')}';
}

class _EventCard extends StatelessWidget {
  const _EventCard({required this.event, required this.onTap});
  final EarthquakeEvent event;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    return Card(
      color: const Color(0xFF1D2A35),
      child: ListTile(
        onTap: onTap,
        leading: CircleAvatar(
          backgroundColor: Colors.redAccent,
          child: Text(event.magnitude?.toStringAsFixed(1) ?? '–'),
        ),
        title: Text(event.location),
        subtitle: Text(
          '${event.occurredAt.toLocal()}\nDepth: ${event.depthKm?.toString() ?? 'Not reported'} km',
        ),
        isThreeLine: true,
        trailing: event.hasCoordinates ? const Icon(Icons.map_outlined) : null,
      ),
    );
  }
}

class _DetailRow extends StatelessWidget {
  const _DetailRow({required this.label, required this.value});
  final String label;
  final String value;

  @override
  Widget build(BuildContext context) => Padding(
    padding: const EdgeInsets.symmetric(vertical: 3),
    child: Row(
      children: [
        SizedBox(
          width: 95,
          child: Text(label, style: const TextStyle(color: Colors.white60)),
        ),
        Expanded(child: Text(value)),
      ],
    ),
  );
}
