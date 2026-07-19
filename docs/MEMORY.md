# 📝 MEMORY — CampusHub

Mendokumentasikan seluruh perubahan arsitektur, database, visual, dan fitur pada project CampusHub.

---

## 1. Arsitektur & Deployment (Vercel + Supabase)

- **Entry Point**: Diubah dari `run.py` menjadi `wsgi.py` sebagai standar Flask zero-config Vercel (mencari instance `app` langsung di root directory).
- **Database Pooler**: Menggunakan pooler Supabase (port 6543) pada production (`DATABASE_URL`), sedangkan migrasi local tetap menggunakan koneksi direct (port 5432) (`DIRECT_URL`). Pengaturan engine SQLAlchemy dioptimalkan dengan `pool_pre_ping=True` dan `pool_recycle=300`.
- **Mitigasi Supabase Auto-Pause**: Ketersediaan database gratis dijaga dengan ping berkala / resume manual sebelum proses penilaian.

---

## 2. Penyimpanan Berkas (Supabase Storage Helper)

Helper sentral di `app/storage.py` memisahkan perlakuan berkas berdasarkan privasi:

- **KTM Provider**: Disimpan di bucket private (`ktm-provider`). Hanya dapat diakses oleh Admin melalui signed URL sementara (durasi 5 menit).
- **Gambar Jasa**: Disimpan di bucket public (`service-images`). Dapat diakses oleh semua pengunjung melalui public URL permanen.
- **Fallback**: Jika variabel `SUPABASE_URL` dan `SUPABASE_KEY` kosong, penyimpanan otomatis dialihkan ke local filesystem (`instance/uploads`).

---

## 3. Notifikasi Pesanan (Polling Ringkas)

- **Tanpa WebSocket**: Mengingat Vercel Functions bersifat serverless dan tidak mendukung koneksi persisten (WebSocket), notifikasi menggunakan polling ringkas.
- **Implementasi**: Endpoint API `/provider/api/pesanan-baru` di-hit oleh JavaScript (`app/static/js/notifications.js`) setiap 30 detik untuk memperbarui badge notifikasi di navbar.
- **Efisiensi Database**: Tidak membutuhkan kolom database baru, melainkan menghitung total order dengan status `pending` secara real-time.

---

## 4. UI/UX & Konvensi Flash Message

- **Public & Admin Pages**: Flash messages ditiadakan pada halaman publik untuk menjaga kebersihan visual.
- **Admin Delete Action**: Aksi penghapusan jasa oleh Admin memicu flash message spesifik berbunyi `"Message deleted!"` sebagai konfirmasi.
- **Itemku Design System**:
  - Warna Utama: Primary Blue (`#2C77D2`), Primary Dark Blue (`#1859AA`), Accent Yellow (`#FFC107`).
  - Font: Headings & UI menggunakan font `Exo`, body copy menggunakan `Exo 2`, label/caption menggunakan `Helvetica`.
  - Border Radius: `8px` untuk tombol utama dan kartu. `0px` untuk input fields.
  - Signature 3D Moment: Efek kartu mengipas (`.service-fan`) pada Hero beranda yang dipicu oleh `IntersectionObserver` (`app/static/js/scroll-effects.js`).
- **Dashboard Counts**: Menghitung secara dinamis dan akurat jumlah Jasa, Order, dan Provider. Halaman dashboard admin tidak memiliki tombol "Back to Admin" untuk estetika layout.

---

## 5. Pengujian & Keamanan

- **Black-box Testing**: Menggunakan `pytest` untuk menguji seluruh alur pendaftaran, login, CRUD jasa, pemesanan, verifikasi admin, hingga transisi status order.
- **Keamanan Kredensial**: Password di-hash menggunakan `werkzeug.security` (`generate_password_hash` dan `check_password_hash`). Seluruh route Provider & Admin diproteksi menggunakan `@login_required` dan role check. CSRF protection diaktifkan global menggunakan Flask-WTF.
