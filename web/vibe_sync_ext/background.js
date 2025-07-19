// WE-WE-WE VibeSync – background service worker
let port;

chrome.runtime.onInstalled.addListener(() => {
  console.log("[VibeSync] installed – MU→YO→O ready");
});

// relay mic FFT summary to active tab (placeholder)
chrome.runtime.onConnect.addListener((p) => {
  port = p;
});