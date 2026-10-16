# QuakeShield Browser Extension (Manifest V3)

Location-based earthquake monitoring extension for QuakeShield research.

> **Safety notice:** This is a research prototype and must **not** replace official emergency alerts or local authority guidance.

## Scope and architecture

This extension is implemented in:

- `/home/runner/work/QuakeShield/QuakeShield/warning_systems/browser_extension/`

Core modules:

- `manifest.json`: Manifest V3 setup with service worker + options page.
- `src/background/service-worker.js`: polling, source fetch, normalization, dedup, stale-state handling, notifications, overlay messaging.
- `src/adapters/`: source adapters
  - `quakeshield-adapter.js` (configurable backend URL)
  - `usgs-adapter.js` (official earthquake report feed adapter)
  - `mock-adapter.js` (explicit **TEST MODE**)
- `src/shared/`: settings, storage, geo calculations, event normalization/filtering, UI/status presentation helpers.
- `src/popup/`: popup UI and `event-details` page.
- `src/settings/`: extension settings and consent/configuration controls.
- `src/content/`: website warning overlay script + style.
- `tests/*.test.js`: unit tests for normalization, dedup, filtering, stale-status logic, adapters, and UI state mapping.

## Current integration status

- The QuakeShield backend adapter is intentionally modular and configurable.
- **Live backend-triggered earthquake integration is not assumed complete** until backend endpoint + schema are finalized.
- TEST MODE should be used to verify full UX flow (popup, details page, notification wording, overlay behavior).

## Installation (unpacked)

1. Open Chrome and go to `chrome://extensions`.
2. Enable **Developer mode**.
3. Click **Load unpacked**.
4. Select `/home/runner/work/QuakeShield/QuakeShield/warning_systems/browser_extension`.

## Configuration

Use **Settings** from the popup.

- Configure QuakeShield backend events URL (full URL; no endpoint assumed by default).
- Optionally configure dashboard URL.
- Confirm threshold values (distance/magnitude/stale windows).
- Configure location manually or by explicit geolocation consent.
- Configure overlay allowed-site host list.
- Enable mock source for **TEST MODE** only.

See `.env.example` for configuration keys.

## Permissions

- `storage`: save user preferences and state.
- `alarms`: periodic polling.
- `notifications`: browser alert delivery.
- `geolocation`: optional browser location use only after user action.
- `tabs` + `scripting`: overlay injection on user-enabled sites.
- Host access for official source (`earthquake.usgs.gov`) and optional dynamic host permissions for configured backend origin.

## Event handling model

- Normalizes all source events into a common event format.
- Distinguishes event types:
  - `EARLY_WARNING`
  - `PRELIMINARY_DETECTION`
  - `CONFIRMED_REPORT`
  - `TEST`
- Deduplicates source-overlapping events by rounded time/magnitude/location signature.
- Avoids duplicate user notifications with local event-id memory.
- Never fabricates magnitudes, distances, warning lead times, or event timestamps.

## Data source behavior

- **QuakeShield backend:** configurable URL; disabled/permission-required state when URL is absent.
- **Official source adapter:** currently expects GeoJSON feed shape compatible with USGS summary feed.
- Catalogue/report entries are treated as reports/preliminary signals, not guaranteed advance warning.

## Reliability guards

- Handles network errors and unavailable sources.
- Marks source staleness with configurable stale threshold.
- Prevents stale/unavailable data from being shown as all clear.
- Filters stale events using configurable max age window.

## Testing

From extension directory:

```bash
cd /home/runner/work/QuakeShield/QuakeShield/warning_systems/browser_extension
npm test
```

Covers:

- event normalization
- deduplication
- location-based relevance
- stale-event filtering
- stale-source status behavior
- adapter error/response handling
- UI status and notification wording mappings

## Current backend API requirements not satisfied in this repository

No documented backend event API was found in repository backend/docs files during this task. To integrate fully, backend must provide:

1. A documented HTTPS event feed URL (or URLs) and auth method.
2. A versioned event schema including required fields:
   - unique event ID
   - event type/classification (`EARLY_WARNING`, `PRELIMINARY_DETECTION`, `CONFIRMED_REPORT`)
   - event and update timestamps (UTC)
   - magnitude (nullable)
   - location name and coordinates (nullable but recommended)
   - optional affected-area list
   - optional validated warning lead-time estimate (when defensible)
3. Source freshness metadata and expected update cadence.
4. Explicit test/simulation flag for non-real events.
5. Clear semantics that differentiate catalogued post-event reports vs operational early warnings.
6. Rate-limit and retry guidance for client polling.

## Limitations

- Browser extension cannot show overlays when browser is closed or extension execution is restricted.
- Browser notifications depend on permission and browser behavior.
- Official data-source licensing/availability should be re-verified for your deployment region before production use.
