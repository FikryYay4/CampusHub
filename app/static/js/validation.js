// validation.js — Client-side form validation for order form
document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('orderForm');
    if (!form) return;

    form.addEventListener('submit', (e) => {
        let valid = true;
        const fields = ['nama_pemesan', 'nim', 'kelas', 'no_whatsapp'];

        // Clear old errors
        form.querySelectorAll('.js-error').forEach(el => el.remove());

        fields.forEach(name => {
            const input = form.querySelector(`[name="${name}"]`);
            if (!input) return;
            const val = input.value.trim();

            if (!val) {
                showError(input, 'Field ini wajib diisi.');
                valid = false;
            }
        });

        // WhatsApp format
        const wa = form.querySelector('[name="no_whatsapp"]');
        if (wa && wa.value.trim() && !/^08\d{8,13}$/.test(wa.value.trim())) {
            showError(wa, 'Format: 08xxxxxxxxxx');
            valid = false;
        }

        if (!valid) e.preventDefault();
    });

    function showError(input, msg) {
        const err = document.createElement('span');
        err.className = 'field-error js-error';
        err.textContent = msg;
        input.parentNode.appendChild(err);
        input.style.borderColor = '#E42B2B';
        input.addEventListener('input', () => {
            input.style.borderColor = '';
            const existing = input.parentNode.querySelector('.js-error');
            if (existing) existing.remove();
        }, { once: true });
    }
});
