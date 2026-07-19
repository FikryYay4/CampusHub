// scroll-effects.js — Signature Moment: fan card animation
document.addEventListener('DOMContentLoaded', () => {
    const fan = document.querySelector('.service-fan');
    if (!fan) return;

    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                fan.classList.add('is-open');
                observer.disconnect();
            }
        });
    }, { threshold: 0.4 });

    observer.observe(fan);
});
