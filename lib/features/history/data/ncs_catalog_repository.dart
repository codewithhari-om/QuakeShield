import 'earthquake_catalog_repository.dart';

/// Safe production behavior until NCS publishes or authorizes an automated
/// catalog interface suitable for this prototype.
class NcsOfficialPortalRepository implements EarthquakeCatalogRepository {
  static final Uri officialPortalUri = Uri.parse(
    'https://riseq.seismo.gov.in/riseq/earthquake/',
  );

  const NcsOfficialPortalRepository();

  @override
  Future<CatalogResult> fetchCatalog() async {
    return CatalogUnavailable(
      officialPortalUri: officialPortalUri,
      reason:
          'No documented automated NCS catalog source has been verified for '
          'this prototype. QuakeShield does not scrape the official website.',
    );
  }
}
