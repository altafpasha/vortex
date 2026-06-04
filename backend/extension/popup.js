// popup.js
const $ = id => document.getElementById(id);

function setStatus(cls, msg) {
  const el = $('status');
  el.className = 'status ' + cls;
  el.textContent = msg;
}

async function init() {
  const { serverUrl, password, lastSync, lastError } =
    await chrome.storage.local.get(['serverUrl', 'password', 'lastSync', 'lastError']);

  if (serverUrl) $('serverUrl').value = serverUrl;
  if (password)  $('password').value  = password;

  if (lastError) {
    setStatus('err', '✗ ' + lastError);
  } else if (lastSync) {
    setStatus('ok', '✓ Last sync: ' + new Date(lastSync).toLocaleString());
  }
}

$('saveBtn').addEventListener('click', async () => {
  const serverUrl = $('serverUrl').value.trim().replace(/\/$/, '');
  const password  = $('password').value.trim();

  if (!serverUrl || !password) {
    setStatus('err', '✗ Fill in both fields');
    return;
  }

  await chrome.storage.local.set({ serverUrl, password, cachedToken: null, tokenExpiry: 0 });
  setStatus('info', '⟳ Syncing...');

  chrome.runtime.sendMessage({ action: 'sync' }, () => {
    chrome.storage.local.get(['lastSync', 'lastError'], ({ lastSync, lastError }) => {
      if (lastError) setStatus('err', '✗ ' + lastError);
      else setStatus('ok', '✓ Synced at ' + new Date(lastSync).toLocaleString());
    });
  });
});

init();
