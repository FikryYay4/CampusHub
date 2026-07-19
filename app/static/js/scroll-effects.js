// Scroll animations for signature moment card fan

document.addEventListener('DOMContentLoaded', () => {
    const fan = document.querySelector('.service-fan');
    if (!fan) return;

    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                fan.classList.add('is-open');
                observer.disconnect(); // Only animate once
            }
        });
    }, { threshold: 0.2 });

    observer.observe(fan);
});
