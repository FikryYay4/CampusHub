# 📝 MEMORY — CampusHub

Mendokumentasikan seluruh perubahan arsitektur, database, visual, dan fitur pada project CampusHub.

---

## 1. Arsitektur & Deployment (Vercel + Supabase)

- **Entry Point**: Diubah dari `run.py` menjadi `wsgi.py` sebagai standar Flask zero-config Vercel (mencari instance `app` langsung di root directory).
- **Database Pooler**: Menggunakan pooler Supabase (port 6543) pada production (`DATABASE_URL`), sedangkan migrasi local tetap menggunakan koneksi direct (port 5432) (`DIRECT_URL`). Pengaturan engine SQLAlchemy dioptimalkan dengan `pool_size=1`, `max_overflow=2`, `pool_pre_ping=True`, dan `pool_recycle=300`.
- **Mitigasi Supabase Auto-Pause**: Ketersediaan database gratis dijaga dengan ping berkala / resume manual sebelum proses penilaian.

---

## 2. Penyimpanan Berkas (Supabase Storage Helper)

Helper sentral di `app/storage.py` memisahkan perlakuan berkas berdasarkan privasi:

- **KTM Provider**: Disimpan di bucket private (`ktm-provider`). Hanya dapat diakses oleh Admin melalui signed URL sementara (durasi 5 menit).
- **Gambar Jasa**: Disimpan di bucket public (`service-images`). Dapat diakses oleh semua pengunjung melalui public URL permanen.
- **Enforcement & Fallback**: Jika berada di environment production (Vercel) atau environment variable Supabase diisi secara parsial, kegagalan penyediaan `SUPABASE_URL` dan `SUPABASE_KEY` akan melempar `ValueError` secara eksplisit alih-alih fallback diam-diam ke local storage. Lokal filesystem (`instance/uploads`) hanya digunakan pada environment lokal / testing.

---

## 3. Notifikasi Pesanan (Polling Ringkas)

- **Tanpa WebSocket**: Mengingat Vercel Functions bersifat serverless dan tidak mendukung koneksi persisten (WebSocket), notifikasi menggunakan polling ringkas.
- **Implementasi**: Endpoint API `/provider/api/pesanan-baru` di-hit oleh JavaScript (`app/static/js/notifications.js`) setiap 30 detik untuk memperbarui badge notifikasi di navbar.
- **Efisiensi Database**: Tidak membutuhkan kolom database baru, melainkan menghitung total order dengan status `pending` secara real-time.

---

## 4. Keamanan & Alur Approval Sistem

- **Password Admin Default**: Password admin default diubah menjadi `admin123_SecureCampusHub` (atau menggunakan env variable `ADMIN_PASSWORD`). Baris kredensial dibersihkan dari README publik.
- **Alur Approval Jasa Baru**: Sesuai dengan spesifikasi `WORKFLOW.md`, setiap jasa baru yang dibuat oleh Provider memiliki status `'pending'` secara default. Admin harus menyetujui (`approve`) atau menolak (`reject`) jasa tersebut di panel kontrol Admin sebelum tampil secara publik.
- **Validasi Transisi Status Order**: Menambahkan validasi ketat pada status order:
  - `accept`/`reject` hanya diperbolehkan jika status saat ini `'pending'`.
  - `complete` hanya diperbolehkan jika status saat ini `'accepted'`.
- **Bug Fix**: Menambahkan `import os` yang sempat hilang di `app/routes/admin.py` untuk menghindari crash saat memproses KTM.
- **Pembersihan Berkas**: Menghapus file duplikat `docs/DESIGN (1).md` untuk merapikan dokumentasi.

---

## 5. UI/UX & Konvensi Flash Message

- **Public Pages**: Flash messages ditiadakan pada halaman publik untuk menjaga kebersihan visual sesuai arahan user.
- **Admin Delete Action**: Aksi penghapusan jasa oleh Admin memicu flash message spesifik berbunyi `"Message deleted!"` sebagai konfirmasi.
- **Itemku Design System**:
  - Warna Utama: Primary Blue (`#2C77D2`), Primary Dark Blue (`#1859AA`), Accent Yellow (`#FFC107`).
  - Font: Headings & UI menggunakan font `Exo`, body copy menggunakan `Exo 2`, label/caption menggunakan `Helvetica`.
  - Border Radius: `8px` untuk tombol utama dan kartu. `0px` untuk input fields.
  - Signature 3D Moment: Efek kartu mengipas (`.service-fan`) pada Hero beranda yang dipicu oleh `IntersectionObserver` (`app/static/js/scroll-effects.js`).
- **Dashboard Counts**: Menghitung secara dinamis dan akurat jumlah Jasa, Order, dan Provider. Halaman dashboard admin tidak memiliki tombol "Back to Admin" untuk estetika layout.

---

## 6. Pengujian

- **Black-box Testing**: Menggunakan `pytest` untuk menguji seluruh alur pendaftaran, login, CRUD jasa, pemesanan, verifikasi admin, hingga transisi status order.

---

## 7. Visual & Animasi

- **Logo Icon**: Navbar menggunakan gambar mascot dari `Icon/icon_maskot/` yang disalin ke `app/static/img/logo.png`. Ditampilkan sebagai bulatan 32x32px dengan border kuning (`accent-yellow`) dan glow shadow.
- **Brand Text Shine**: Teks "CampusHub" di navbar menggunakan gradient text animation (`brand-shine`) — sapuan cahaya bergerak dari kanan ke kiri pada teks putih secara berulang. Dilengkapi 3 partikel kecil (`brand-particle`) yang berkedip di sekitar logo. `prefers-reduced-motion` dihormati (animasi nonaktif).
- **Signature Moment — Kartu Mengipas (Fan Cards)**: 5 kartu kategori (Jastip, Editing, Desain, Tutor, Print) ditumpuk lalu mengipas terbuka menggunakan `IntersectionObserver`. Setiap kartu memiliki ikon PNG dari `app/static/img/icons/` dengan fallback ke emoji. Idle bob animation (naik-turun halus) dimainkan sebelum fan-out. Setelah fan-out, kartu bergantian ke depan secara cycling (`is-active` poker-slide) tiap 2.2 detik. Fallback timeout 300ms menjamin animasi jalan meskipun IntersectionObserver terlambat trigger.
- **Kategori Icon Grid**: 7 kategori ditampilkan sebagai baris ikon bulat (emoji) + label, menggunakan CSS flex wrap. Setiap ikon memiliki hover effect (translateY + background change).
- **Featured Rows**: Maksimal 3 baris kategori yang sudah punya jasa aktif, masing-masing horizontal-scroll dengan tautan "Lihat Semua →". Hanya kategori dengan jasa aktif yang ditampilkan untuk menghindari baris kosong.
