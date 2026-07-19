# Perubahan: Efek Brand, Kartu Mengipas, & Kategori ala Gambar 3

5 file berubah, tinggal timpa ke path yang sama di repo:

```
app/routes/public.py
app/templates/partials/navbar.html
app/templates/public/home.html
app/static/css/style.css
app/static/js/scroll-effects.js
```

Sudah dites: `pytest` (7/7 lulus) + render manual dengan data asli (kategori, provider, jasa) — semua elemen baru muncul di HTML dengan benar.

## 1. Tulisan "CampusHub" — kilau + partikel

`navbar.html` & `style.css`. Teksnya sekarang punya sapuan cahaya (`brand-shine`) yang lewat sekali tiap ~4 detik — bukan kedip on/off kasar, supaya tetap terlihat premium bukan rusak — ditambah 3 partikel kecil (`brand-particle`) yang berkelip di sekitar logo. `prefers-reduced-motion` tetap dihormati.

## 2. Kartu mengipas — ikon, gerak idle, & bergantian ke depan

`home.html`, `style.css`, `scroll-effects.js`. Tiga perubahan:
- **Ikon**: tiap kartu sekarang punya slot `<img>` yang mengarah ke `app/static/img/icons/{jastip,editing,desain,tutor,print}.png`. **Folder ini belum ada di repo — upload 5 PNG kamu ke situ.** Kalau file belum ada/gagal dimuat, otomatis jatuh ke emoji lama (tidak akan tampil gambar rusak).
- **Gerak dari awal**: tumpukan kartu sekarang punya animasi "bernapas" halus (naik-turun kecil, delay bertahap tiap kartu) bahkan sebelum kartu mengipas terbuka.
- **Bergantian ke depan**: ~0.9 detik setelah kartu selesai mengipas, satu kartu pada satu waktu membesar & maju ke depan (`is-active`), lalu gantian ke kartu sebelahnya tiap 2.2 detik — efek geser seperti membuka kartu remi satu-satu. Kalau `prefers-reduced-motion` aktif, pergantian ini dimatikan (kartu tetap diam di posisi mengipas).

## 3. Kategori layanan ala Gambar 3

`public.py` & `home.html` & `style.css`. Bagian "Kategori Layanan" yang tadinya grid kotak polos, sekarang:
- Baris ikon bulat + label (7 kategori, ikon masih emoji — gampang diganti PNG nanti dengan pola yang sama seperti kartu mengipas kalau mau).
- Di bawahnya, sampai 3 baris kategori yang scroll horizontal (cuma kategori yang **sudah punya jasa aktif** yang muncul, biar nggak ada baris kosong), masing-masing dengan tautan "Lihat Semua →".
- "Layanan Terbaru" di paling bawah tetap ada seperti semula.

## Satu temuan bonus (di luar yang diminta)

Waktu saya tes render, ketemu: `pool_size`/`max_overflow` yang ditambahkan di commit kemarin ke `config.py` ternyata **bikin app crash kalau `DATABASE_URL` kosong dan jatuh ke SQLite** — parameter itu tidak valid untuk pooling default SQLite. Ini murni soal jalur fallback lokal (bukan soal koneksi Supabase asli, yang mana masih aman), tapi sekalian menegaskan lagi kenapa penting benar-benar pastikan `DATABASE_URL` ke Supabase ke-set waktu deploy ke Vercel — bukan cuma soal upload yang bisa diam-diam salah, ternyata start aplikasinya sendiri bisa gagal total.
