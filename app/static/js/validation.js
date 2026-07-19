// Client-side form validation for CampusHub order form

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('orderForm');
    if (!form) return;

    const nameInput = document.getElementById('nama_pemesan');
    const nimInput = document.getElementById('nim');
    const kelasInput = document.getElementById('kelas');
    const waInput = document.getElementById('no_whatsapp');

    function showError(input, msg) {
        // Remove existing error if any
        let errorSpan = input.parentNode.querySelector('.field-error');
        if (!errorSpan) {
            errorSpan = document.createElement('span');
            errorSpan.className = 'field-error';
            input.parentNode.appendChild(errorSpan);
        }
        errorSpan.textContent = msg;
        input.classList.add('input-error');
    }

    function clearError(input) {
        const errorSpan = input.parentNode.querySelector('.field-error');
        if (errorSpan) {
            errorSpan.remove();
        }
        input.classList.remove('input-error');
    }

    form.addEventListener('submit', (e) => {
        let hasError = false;

        // Name Validation
        if (!nameInput.value.trim()) {
            showError(nameInput, 'Nama lengkap wajib diisi.');
            hasError = true;
        } else {
            clearError(nameInput);
        }

        // NIM Validation
        if (!nimInput.value.trim()) {
            showError(nimInput, 'NIM wajib diisi.');
            hasError = true;
        } else {
            clearError(nimInput);
        }

        // Kelas Validation
        if (!kelasInput.value.trim()) {
            showError(kelasInput, 'Kelas wajib diisi.');
            hasError = true;
        } else {
            clearError(kelasInput);
        }

        // WhatsApp Validation
        const waValue = waInput.value.trim();
        const waPattern = /^08\d{8,13}$/;
        if (!waValue) {
            showError(waInput, 'Nomor WhatsApp wajib diisi.');
            hasError = true;
        } else if (!waPattern.test(waValue)) {
            showError(waInput, 'Format WhatsApp salah. Contoh: 08xxxxxxxxxx (10-15 digit)');
            hasError = true;
        } else {
            clearError(waInput);
        }

        if (hasError) {
            e.preventDefault();
        }
    });

    // Realtime clear on input
    [nameInput, nimInput, kelasInput, waInput].forEach(input => {
        if (input) {
            input.addEventListener('input', () => clearError(input));
        }
    });
});
