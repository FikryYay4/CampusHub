// Scroll animations for signature moment card fan

document.addEventListener('DOMContentLoaded', () => {
    const fan = document.querySelector('.service-fan');
    if (!fan) return;

    const cards = Array.from(fan.querySelectorAll('.fan-card'));
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const CYCLE_MS = 2200;
    let activeIndex = Math.floor(cards.length / 2); // start on the center card
    let cycleTimer = null;

    function setActive(index) {
        cards.forEach((card, i) => card.classList.toggle('is-active', i === index));
    }

    function startCycle() {
        if (prefersReducedMotion || cycleTimer || cards.length === 0) return;
        setActive(activeIndex);
        cycleTimer = setInterval(() => {
            activeIndex = (activeIndex + 1) % cards.length;
            setActive(activeIndex);
        }, CYCLE_MS);
    }

    // Force fan open after load delay — hero is usually above fold,
    // but IntersectionObserver can miss it on fast loads
    window.setTimeout(() => {
        if (!fan.classList.contains('is-open')) {
            fan.classList.add('is-open');
            window.setTimeout(startCycle, 900);
        }
    }, 300);

    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                if (!fan.classList.contains('is-open')) {
                    fan.classList.add('is-open');
                    window.setTimeout(startCycle, 900);
                }
                observer.disconnect();
            }
        });
    }, { threshold: 0.05 });

    observer.observe(fan);
});
