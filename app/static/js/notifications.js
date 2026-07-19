// Real-time notification polling for Provider orders

document.addEventListener('DOMContentLoaded', () => {
    const badge = document.getElementById('pesanan-baru-badge');
    if (!badge) return; // Only run if badge exists in DOM (Provider logged in)

    const POLL_MS = 30000; // 30 seconds

    async function refreshBadge() {
        try {
            const res = await fetch('/provider/api/pesanan-baru');
            if (res.ok) {
                const data = await res.json();
                const count = data.count;
                badge.textContent = count;
                if (count > 0) {
                    badge.classList.remove('d-none');
                } else {
                    badge.classList.add('d-none');
                }
            }
        } catch (err) {
            // Silently ignore network failures and retry on next interval
        }
    }

    // Initial load
    refreshBadge();

    // Polling interval
    setInterval(refreshBadge, POLL_MS);
});
