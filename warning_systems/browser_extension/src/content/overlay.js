const ROOT_ID = 'qs-overlay-root';

function ensureRoot() {
  let root = document.getElementById(ROOT_ID);
  if (root) return root;

  root = document.createElement('aside');
  root.id = ROOT_ID;
  root.setAttribute('role', 'status');
  root.setAttribute('aria-live', 'assertive');
  root.hidden = true;
  document.documentElement.appendChild(root);
  return root;
}

function hideOverlay() {
  const root = ensureRoot();
  root.hidden = true;
}

function renderOverlay(payload) {
  const root = ensureRoot();
  if (!payload?.shouldShow || !payload.event) {
    hideOverlay();
    return;
  }

  const event = payload.event;
  const magnitude = event.magnitude === null ? 'Magnitude unavailable' : `M${Number(event.magnitude).toFixed(1)}`;

  root.innerHTML = `
    <section class="qs-overlay-panel status-${payload.status}">
      <header class="qs-overlay-header">
        <div class="qs-overlay-title">QuakeShield ${payload.testMode ? 'TEST MODE' : 'Alert'}</div>
        <button class="qs-overlay-dismiss" aria-label="Dismiss warning overlay">×</button>
      </header>
      <div class="qs-overlay-summary">${magnitude} • ${event.locationName || 'Unknown location'}</div>
      <div class="qs-overlay-meta">Source: ${event.source} • ${new Date(event.occurredAt || Date.now()).toLocaleString()}</div>
      <div class="qs-overlay-warning">Research prototype. Follow official emergency alerts and local authorities.</div>
    </section>
  `;

  root.querySelector('.qs-overlay-dismiss')?.addEventListener('click', () => {
    root.hidden = true;
  });

  root.hidden = false;
}

chrome.runtime.onMessage.addListener((message) => {
  if (message?.type !== 'QS_OVERLAY_UPDATE') return;
  renderOverlay(message);
});
