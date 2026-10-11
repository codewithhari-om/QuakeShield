import '../domain/earthquake_event.dart';

abstract interface class EarthquakeCatalogRepository {
  Future<CatalogResult> fetchCatalog();
}

sealed class CatalogResult {
  const CatalogResult();
}

class CatalogSuccess extends CatalogResult {
  const CatalogSuccess({
    required this.events,
    required this.fetchedAt,
    required this.sourceLabel,
  });

  final List<EarthquakeEvent> events;
  final DateTime fetchedAt;
  final String sourceLabel;
}

class CatalogUnavailable extends CatalogResult {
  const CatalogUnavailable({
    required this.officialPortalUri,
    required this.reason,
  });

  final Uri officialPortalUri;
  final String reason;
}

class CatalogFailure extends CatalogResult {
  const CatalogFailure({
    required this.message,
    required this.officialPortalUri,
  });

  final String message;
  final Uri officialPortalUri;
}
