Menurut saya, konsep yang sudah kita bentuk sekarang sudah cukup matang. Agar implementasinya mudah, saya menyarankan **tidak menggunakan istilah "Skill Marketplace"**, tetapi gunakan konsep **Marketplace Layanan Mahasiswa**.

Misalnya nama aplikasinya:

> **CampusHub**
> *Platform Layanan Mahasiswa Berbasis Web*

Di dalamnya bisa ada:

* Jasa Editing
* Jasa Desain
* Jasa Programming
* Tutor
* Jastip Makanan
* Jastip Minuman
* Print/Fotokopi
* dan lain-lain.

---

# 👥 Aktor Sistem

## 1. Pengunjung (Guest/Public)

Tidak perlu login.

Hak akses:

* Melihat daftar layanan
* Mencari layanan
* Filter kategori
* Melihat detail layanan
* Memesan layanan

---

## 2. Penyedia Jasa (Provider)

Login.

Hak akses:

* Registrasi akun
* Login
* Mengelola jasa
* Melihat pesanan
* Mengubah status pesanan
* Mengelola profil

---

## 3. Admin

Login.

Hak akses:

* Verifikasi provider
* Mengelola kategori
* Mengelola provider
* Menghapus layanan
* Dashboard
* Statistik

---

# Alur Logika Sistem

```text
                           START
                              │
                              ▼
                    Halaman Beranda
                              │
      ┌───────────────────────┼────────────────────────┐
      ▼                       ▼                        ▼
 Pengunjung             Penyedia Jasa               Admin
      │                       │                        │
      │                  Login/Register            Login
      │                       │                        │
      ▼                       ▼                        ▼
Lihat Daftar Jasa       Dashboard Provider      Dashboard Admin
      │                       │                        │
      ▼                       ▼                        ▼
Cari / Filter          Kelola Jasa           Kelola Provider
      │                       │                        │
      ▼                       ▼                        ▼
Detail Jasa          Tambah/Edit/Hapus       Kelola Kategori
      │                       │                        │
      ▼                       ▼                        ▼
Isi Form Pesanan      Lihat Pesanan          Lihat Statistik
      │                       │
      ▼                       ▼
Data Masuk Database    Terima / Tolak
      │                       │
      └──────────────► Update Status ◄──────────────┐
                              │
                              ▼
                           Selesai
```

---

# Algoritma Pengunjung

```
START

↓

Buka Website

↓

Lihat Daftar Layanan

↓

Cari Layanan

↓

Klik Detail

↓

Isi

Nama

NIM

Kelas

Nomor WhatsApp

Catatan

↓

Klik Pesan

↓

Validasi

↓

Data Disimpan

↓

Status

Menunggu Konfirmasi

↓

END
```

---

# Algoritma Penyedia Jasa

```
START

↓

Login

↓

Valid?

↓

Tidak

↓

Kembali Login

↓

Ya

↓

Dashboard

↓

Pilih Menu

Tambah Jasa

↓

Isi Data

Judul

Kategori

Harga

Deskripsi

↓

Simpan

↓

Menunggu Verifikasi Admin

↓

Jika Disetujui

↓

Jasa Tampil

↓

END
```

---

# Algoritma Pemesanan

```
START

↓

Guest memilih jasa

↓

Isi Form

↓

Klik Pesan

↓

Database

↓

Order Baru

↓

Masuk ke Dashboard Provider

↓

Provider Login

↓

Lihat Pesanan

↓

Accept / Reject

↓

Status Berubah

↓

Guest dihubungi melalui WhatsApp

↓

Pesanan Selesai

↓

END
```

> **Catatan:** Karena Guest tidak memiliki akun, notifikasi cukup melalui nomor WhatsApp yang diisikan saat memesan.

---

# Algoritma Admin

```
START

↓

Login

↓

Dashboard

↓

Pilih Menu

↓

Provider

↓

Verifikasi Akun

↓

Approve

↓

Provider Aktif

↓

Kelola Kategori

↓

Kelola Layanan

↓

Lihat Dashboard

↓

END
```

---

# Flow Penyedia Baru

```
Daftar Provider

↓

Isi Biodata

↓

Upload KTM (Opsional)

↓

Status

Pending

↓

Admin Verifikasi

↓

Disetujui

↓

Provider Bisa Login

↓

Mulai Menawarkan Jasa
```

---

# Flow Dashboard Admin

```
Dashboard

↓

Hitung

↓

Jumlah Provider

↓

Jumlah Jasa

↓

Jumlah Order

↓

Kategori Terpopuler

↓

Provider Teraktif

↓

Grafik Order Bulanan

↓

Grafik Kategori
```

---

# Struktur Database

```
Admin
│
├── Provider
│      │
│      ├── Service
│      │       │
│      │       └── Order
│      │
│      └── Category
```

---

# Alur Bisnis Lengkap

```text
Provider Daftar
        │
        ▼
Admin Verifikasi
        │
        ▼
Provider Login
        │
        ▼
Tambah Layanan
        │
        ▼
Guest Melihat Layanan
        │
        ▼
Guest Memesan
        │
        ▼
Order Masuk
        │
        ▼
Provider Konfirmasi
        │
        ▼
Status Order
Pending
 │
 ├───────────────┐
 ▼               ▼
Accepted      Rejected
 │
 ▼
Completed
```

---

# Status Order

Saya menyarankan hanya menggunakan 4 status agar sederhana:

```text
Pending
↓
Accepted
↓
Completed
```

atau

```text
Pending
↓
Rejected
```

Dengan alur ini, sistem tetap sederhana namun sudah mencakup seluruh proses bisnis dari penyedia mendaftar hingga pesanan selesai.

## Penyesuaian agar sesuai UAS

Dari sisi dokumen UAS, kamu tetap memenuhi syarat adanya dua sisi pengguna secara fungsional:

* **Pengunjung (Publik)**: mengakses layanan tanpa login, mencari jasa, dan membuat pesanan.
* **Admin**: login untuk mengelola sistem melalui dashboard.
* **Penyedia Jasa**: merupakan pengguna khusus yang harus terverifikasi agar dapat menawarkan layanan dan mengelola pesanan.

Model ini realistis untuk lingkungan kampus karena pembeli tidak dipaksa membuat akun, sementara penyedia jasa tetap memiliki akun agar sistem dapat mengelola layanan dan pesanan dengan baik. Ini juga menjaga implementasi tetap sederhana dan cocok diselesaikan dalam waktu sekitar tiga hari.

---

# 🎨 Efek Visual: Animasi 3D & Scroll Interaction

Satu hal yang perlu dihindari: pasang dua-tiga library animasi lalu tempel efek fade/tilt di semua elemen. Itu justru bikin halaman terasa seperti template generik. Pendekatan yang lebih kuat: **satu momen 3D yang jadi "tanda tangan" halaman**, dijalankan dengan baik — sisanya dibuat tenang.

## Sudut Pandang

CampusHub intinya adalah *banyak jenis layanan mahasiswa, terkumpul di satu wadah*. Representasi visual paling jujur untuk ide itu bukan kartu yang tilt mengikuti kursor, tapi **kartu-kartu layanan yang mulanya menumpuk lalu mengipas terbuka** — seperti kartu remi dikocok lalu dibentangkan satu per satu. Momen ini ditaruh di hero (halaman beranda); elemen-elemen lain (list layanan, dashboard) sengaja dibuat senyap supaya momen ini yang diingat.

## Prinsip

1. **Satu momen terorkestrasi, bukan efek yang dicecer** ke setiap kartu/section.
2. **`transform` + `opacity` saja** (GPU-friendly) — hindari animasikan `top/left/width/height`.
3. **`prefers-reduced-motion` dihormati** — animasi nonaktif otomatis untuk pengguna yang sensitif gerakan.
4. **Elemen di luar signature moment dibuat tenang** — cukup sedikit terangkat saat hover, tanpa tilt-ikuti-kursor atau glare di mana-mana.

## Signature Moment — "Kartu Layanan Mengipas" (Hero, Halaman Beranda)

Lima kartu kategori (Jastip, Editing, Desain, Tutor, Print) ditumpuk di satu titik pivot (bawah-tengah), lalu berputar membuka seperti kipas — dipicu lewat `IntersectionObserver`, yang otomatis menangani dua kasus sekaligus: langsung terpicu kalau elemen sudah terlihat saat halaman dimuat (posisi hero), atau terpicu saat baru discroll ke viewport (kalau elemen ini dipakai lagi di bagian lain halaman).

```html
<div class="service-fan">
  <div class="fan-card">Jastip</div>
  <div class="fan-card">Editing</div>
  <div class="fan-card">Desain</div>
  <div class="fan-card">Tutor</div>
  <div class="fan-card">Print</div>
</div>
```

```css
.service-fan {
  perspective: 1000px;
  position: relative;
  width: 300px;
  height: 240px;
  margin: 0 auto;
}

.fan-card {
  position: absolute;
  bottom: 0;
  left: 50%;
  width: 130px;
  height: 190px;
  margin-left: -65px;
  border-radius: 14px;
  transform-origin: bottom center;
  transform: rotateZ(0deg) rotateY(0deg);
  transition: transform 900ms cubic-bezier(0.22, 1, 0.36, 1);
  box-shadow: 0 14px 30px rgba(0, 0, 0, .18);
}

.fan-card:nth-child(1) { transition-delay: 0ms;    z-index: 1; }
.fan-card:nth-child(2) { transition-delay: 80ms;   z-index: 2; }
.fan-card:nth-child(3) { transition-delay: 160ms;  z-index: 3; }
.fan-card:nth-child(4) { transition-delay: 240ms;  z-index: 2; }
.fan-card:nth-child(5) { transition-delay: 320ms;  z-index: 1; }

.service-fan.is-open .fan-card:nth-child(1) { transform: rotateZ(-28deg) rotateY(20deg); }
.service-fan.is-open .fan-card:nth-child(2) { transform: rotateZ(-14deg) rotateY(10deg); }
.service-fan.is-open .fan-card:nth-child(3) { transform: rotateZ(0deg)   rotateY(0deg); }
.service-fan.is-open .fan-card:nth-child(4) { transform: rotateZ(14deg)  rotateY(-10deg); }
.service-fan.is-open .fan-card:nth-child(5) { transform: rotateZ(28deg)  rotateY(-20deg); }

@media (prefers-reduced-motion: reduce) {
  .fan-card { transition: none; }
}
```

```js
// app/static/js/scroll-effects.js
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
```

## Elemen Lain — Sengaja Dibuat Tenang

| Bagian | Perlakuan |
|---|---|
| Kartu layanan (list/katalog) | `translateY(-4px)` + shadow lembut saat hover. Tidak ada tilt-ikuti-kursor atau glare. |
| Dashboard Admin/Provider | Angka & grafik tampil langsung, paling banter *fade-in* sekali saat halaman dimuat — tanpa animasi count-up. |
| Transisi antar-section | Tidak perlu efek khusus; cukup spacing dan tipografi yang rapi untuk memisahkan section. |

Menahan diri di bagian ini justru yang membuat momen kartu mengipas di hero terasa berarti — kalau semua elemen bergerak, tidak ada yang terasa istimewa.

## Implementasi

- CSS di atas masuk ke `app/static/css/style.css`.
- JS di atas masuk ke `app/static/js/scroll-effects.js` (lihat `FOLDER_STRUCTURE.md`).
- Markup kartu ditaruh di `templates/public/home.html`, pada section hero.
- Murni CSS + JS ringan sisi klien — tidak menyentuh backend Flask, skema database, atau `requirements.txt`.

## Catatan

- Kalau nanti masuk ke tahap menentukan palet warna & tipografi CampusHub, coba hindari kombinasi "default AI" yang sering muncul: krem + serif + aksen terracotta, atau gelap + aksen neon tunggal. Pilih warna yang terasa spesifik untuk CampusHub, bukan template.
- Kalau linimasa mepet, versi paling minimal tetap masih layak: hanya *fade-in* judul hero saat load, tanpa kartu mengipas. Tapi efek kartu mengipas ini realistis dikerjakan dalam waktu kurang dari satu jam begitu markup-nya siap — dampaknya jauh lebih terasa dibanding waktu yang dihabiskan.
