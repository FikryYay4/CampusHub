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

    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                fan.classList.add('is-open');
                // Let the fan-out transition (900ms) settle before the cards start
                // taking turns sliding to the front, like riffling through a hand of cards.
                window.setTimeout(startCycle, 900);
                observer.disconnect(); // Fan-out itself only plays once
            }
        });
    }, { threshold: 0.2 });

    observer.observe(fan);
});
