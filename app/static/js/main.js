// Main JavaScript for CampusHub

document.addEventListener('DOMContentLoaded', () => {
    // Navbar toggle for mobile views
    const navToggle = document.getElementById('navToggle');
    const navLinks = document.getElementById('navLinks');

    if (navToggle && navLinks) {
        navToggle.addEventListener('click', () => {
            navLinks.classList.toggle('active');
        });
    }
});
