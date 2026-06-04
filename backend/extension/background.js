// Vortex Cookie Sync — background service worker

const DOMAINS = ['.youtube.com', '.google.com'];

function toCookieLine(c) {
  const domain = c.domain.startsWith('.') ? c.domain : '.' + c.domain;
  const sub    = c.domain.startsWith('.') ? 'TRUE' : 'FALSE';
  const expiry = Math.floor(c.expirationDate || 2147483647);
  const secure = c.secure ? 'TRUE' : 'FALSE';
  return [domain, sub, c.path, secure, expiry, c.name, c.value].join('\t');
}

async function getToken(serverUrl, password) {
  const { cachedToken, tokenExpiry } = await chrome.storage.local.get(['cachedToken', 'tokenExpiry']);
  if (cachedToken && tokenExpiry && Date.now() < tokenExpiry) return cachedToken;

  const res = await fetch(`${serverUrl}/api/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ password }),
  });
  const data = await res.json();
  if (!data.ok) throw new Error('Login failed — check your password');

  // Cache token for 23 hours
  await chrome.storage.local.set({
    cachedToken: data.token,
    tokenExpiry: Date.now() + 23 * 60 * 60 * 1000,
  });
  return data.token;
}

async function syncCookies() {
  const { serverUrl, password } = await chrome.storage.local.get(['serverUrl', 'password']);
  if (!serverUrl || !password) return;

  // Collect cookies from YouTube + Google
  const all = [];
  for (const domain of DOMAINS) {
    const cookies = await chrome.cookies.getAll({ domain });
    all.push(...cookies);
  }

  // Only sync if actually logged in (SID present)
  const loggedIn = all.some(c =>
    (c.name === 'SID' || c.name === '__Secure-1PSID' || c.name === 'SAPISID') &&
    c.value.length > 8
  );
  if (!loggedIn) {
    await chrome.storage.local.set({ lastError: 'Not signed in to YouTube — open youtube.com and sign in first' });
    return;
  }

  const lines = ['# Netscape HTTP Cookie File', '# Vortex Cookie Sync', ''];
  for (const c of all) lines.push(toCookieLine(c));
  const cookiesTxt = lines.join('\n');

  const token  = await getToken(serverUrl, password);
  const blob   = new Blob([cookiesTxt], { type: 'text/plain' });
  const form   = new FormData();
  form.append('file', blob, 'cookies.txt');

  const res = await fetch(`${serverUrl}/api/cookies/upload`, {
    method: 'POST',
    headers: { 'X-Auth-Token': token },
    body: form,
  });
  if (!res.ok) throw new Error(`Server error ${res.status}`);

  await chrome.storage.local.set({ lastSync: Date.now(), lastError: null });
}

async function trySyncCookies() {
  try {
    await syncCookies();
  } catch (e) {
    await chrome.storage.local.set({ lastError: e.message });
  }
}

// Sync every 6 hours
chrome.alarms.create('vortex_sync', { periodInMinutes: 360 });
chrome.alarms.onAlarm.addListener(alarm => {
  if (alarm.name === 'vortex_sync') trySyncCookies();
});

// Sync on install / extension update
chrome.runtime.onInstalled.addListener(() => trySyncCookies());

// Manual sync triggered from popup
chrome.runtime.onMessage.addListener((msg, _sender, reply) => {
  if (msg.action === 'sync') {
    trySyncCookies().then(() => reply({ ok: true }));
    return true;
  }
});
