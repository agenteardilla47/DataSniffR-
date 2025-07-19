// Inject vibe classes based on simple keyword detection
const vibeMap = {
  joy: /jajaja/i,
  hum: /mmm+/i,
  paranoia: /lok kkkk/i,
};

function scanAndApply() {
  const body = document.body.innerText;
  Object.entries(vibeMap).forEach(([cls, regex]) => {
    if (regex.test(body)) {
      document.documentElement.classList.add(`vibe-${cls}`);
    }
  });
}

scanAndApply();
setInterval(scanAndApply, 5000);