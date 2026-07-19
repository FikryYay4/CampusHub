# 📋 Product Requirements Document (PRD)

## CampusHub — Platform Layanan Mahasiswa Berbasis Web

| | |
|---|---|
| **Mata Kuliah** | Pengantar Pemrograman — UAS Berbasis Project |
| **Versi Dokumen** | 1.0 |
| **Tanggal** | 19 Juli 2026 |
| **Status** | Draft — untuk dikonsultasikan ke dosen pengampu |

---

## 1. Ringkasan Produk

**CampusHub** adalah sistem informasi berbasis web yang mempertemukan mahasiswa yang membutuhkan jasa (jastip, editing, desain, programming, tutor, print/fotokopi, dsb.) dengan mahasiswa lain yang menyediakan jasa tersebut, dalam satu platform terpusat berbasis kampus.

Dibangun dengan **Python (Flask)** dan **SQLite**, sesuai ketentuan teknis UAS, dan mengangkat permasalahan nyata: **belum ada wadah terpusat bagi mahasiswa untuk saling menawarkan dan mencari jasa di lingkungan kampus** — saat ini masih tersebar di berbagai grup WhatsApp/story Instagram tanpa struktur yang jelas.

## 2. Latar Belakang Masalah

- Penawaran jasa antar-mahasiswa saat ini tersebar di berbagai *chat group* dan media sosial, sulit dicari dan dibandingkan.
- Tidak ada mekanisme verifikasi penyedia jasa, sehingga rawan jasa fiktif.
- Tidak ada rekap data terpusat mengenai jasa apa yang paling dicari di lingkungan kampus.

## 3. Tujuan

### 3.1 Tujuan Produk
1. Menyediakan satu platform terpusat untuk publikasi dan pencarian jasa antar-mahasiswa.
2. Memberi mekanisme verifikasi sederhana bagi penyedia jasa agar lebih terpercaya.
3. Memberi visibilitas data (statistik) kepada Admin mengenai aktivitas platform.

### 3.2 Tujuan Akademik (selaras Ketentuan UAS)
1. Menerapkan variabel, struktur kontrol, fungsi, struktur data, dan interaksi basis data lewat studi kasus nyata.
2. Memenuhi seluruh **Fitur Wajib** UAS (lihat §6).
3. Proyek dapat diselesaikan dalam kerangka waktu perkuliahan (estimasi §12).

## 4. Ruang Lingkup

### 4.1 Termasuk (In-Scope)
- Sisi Pengunjung/Guest (tanpa login): jelajah, cari, filter, lihat detail, pesan jasa.
- Sisi Penyedia Jasa/Provider (login): registrasi, kelola jasa (CRUD), kelola pesanan.
- Sisi Admin (login): verifikasi provider, kelola kategori, kelola/hapus jasa, dashboard statistik.
- Autentikasi berbasis session untuk Admin & Provider.
- Validasi form sisi client & server, flash message di setiap aksi.

### 4.2 Di Luar Cakupan (Out-of-Scope) — untuk versi UAS ini
- Pembayaran online / payment gateway (transaksi tetap manual via WhatsApp).
- Sistem rating & ulasan (lihat §13, pengembangan lanjutan).
- Live chat dalam aplikasi.
- Aplikasi mobile native.

## 5. Aktor & Pengguna

| Aktor | Login? | Hak Akses Utama |
|---|---|---|
| **Pengunjung (Guest)** | Tidak | Melihat, mencari, memfilter, melihat detail, dan memesan layanan |
| **Penyedia Jasa (Provider)** | Ya | Registrasi, kelola jasa (CRUD), lihat & proses pesanan, kelola profil |
| **Admin** | Ya | Verifikasi provider, kelola kategori & layanan, dashboard & statistik |

> Sistem ini memenuhi — bahkan melebihi — syarat minimal UAS berupa dua sisi pengguna fungsional (publik & admin), karena turut menghadirkan sisi ketiga (Provider) sebagai pengguna khusus dengan alur verifikasi sendiri.

## 6. Kebutuhan Fungsional

| ID | Fitur | Deskripsi | Aktor | Prioritas | Ref. Fitur Wajib UAS |
|---|---|---|---|---|---|
| FR-01 | Lihat & cari layanan | Daftar layanan, pencarian, filter kategori | Guest | Must | Sisi pengguna umum |
| FR-02 | Detail layanan | Halaman detail satu layanan | Guest | Must | Sisi pengguna umum |
| FR-03 | Form pemesanan | Isi Nama, NIM, Kelas, No. WhatsApp, Catatan tanpa akun | Guest | Must | Sisi pengguna umum |
| FR-04 | Validasi input | Validasi client (JS) & server (Flask/WTForms) di semua form | Semua | Must | Fitur Wajib #5 |
| FR-05 | Registrasi Provider | Form pendaftaran + upload KTM opsional | Provider | Must | — |
| FR-06 | Login Admin & Provider | Login session-based, proteksi halaman dashboard | Provider, Admin | Must | Fitur Wajib #1 |
| FR-07 | Verifikasi Provider | Admin approve/reject pendaftaran provider baru | Admin | Must | — |
| FR-08 | CRUD Layanan | Tambah/ubah/hapus jasa milik sendiri | Provider | Must | Fitur Wajib #2 |
| FR-09 | Kelola Pesanan | Lihat pesanan masuk, ubah status Accept/Reject/Completed | Provider | Must | Fitur Wajib #2 |
| FR-10 | Dashboard Admin | Ringkasan jumlah provider, jasa, order, kategori terpopuler | Admin | Must | Fitur Wajib #3 |
| FR-11 | Laporan/grafik dinamis | Grafik order bulanan & kategori dari data live (bukan statis) | Admin | Must | Fitur Wajib #4 |
| FR-12 | Kelola Kategori | CRUD kategori layanan | Admin | Must | — |
| FR-13 | Hapus Layanan | Admin dapat menghapus layanan yang melanggar ketentuan | Admin | Should | — |
| FR-14 | Flash message & navigasi | Notifikasi berhasil/gagal + navigasi antar-halaman jelas | Semua | Must | Fitur Wajib #6 |
| FR-15 | Kontak WhatsApp | Provider menghubungi guest manual pasca-accept | Provider | Should | Catatan alur `DESIGN.md` |
| FR-16 | Upload gambar layanan | Provider unggah 1 foto per jasa (JPG/PNG/WEBP, maks 2MB) | Provider | Should | — |
| FR-17 | Notifikasi pesanan baru | Badge jumlah pesanan status Pending di dashboard Provider, diperbarui berkala (polling) | Provider | Should | — |

## 7. Kebutuhan Non-Fungsional

| Kategori | Ketentuan |
|---|---|
| Keamanan | Password di-hash (`werkzeug.security`); proteksi CSRF (Flask-WTF); `login_required` di semua route Provider/Admin; KTM di bucket privat Supabase Storage (signed URL, khusus Admin); gambar jasa di bucket publik (memang untuk ditampilkan ke semua orang); `service_role key` Supabase hanya hidup di server, tidak pernah di sisi browser |
| Usability | Navigasi maksimal 3 klik ke fitur utama; layout responsif (Bootstrap grid) |
| Performa | Query dashboard terindeks pada foreign key; hindari query N+1 |
| Portabilitas | PostgreSQL (Supabase) dipakai konsisten untuk development & production — opsi yang diperbolehkan di ketentuan UAS §2.1, sekaligus menghindari bug akibat perbedaan dialek SQL |
| Deployment | Hosting di Vercel (Flask zero-config); custom domain `.my.id` diarahkan lewat Vercel Dashboard |
| Ketersediaan | Project Supabase gratis auto-pause setelah 7 hari tanpa aktivitas — wajib di-resume manual atau di-ping berkala menjelang masa penilaian (lihat `FOLDER_STRUCTURE.md`) |
| Maintainability | Struktur folder modular (lihat `FOLDER_STRUCTURE.md`), `requirements.txt` lengkap |
| Aksesibilitas | Efek animasi/3D menghormati `prefers-reduced-motion` (lihat `DESIGN.md`) |

## 8. Model Data (Ringkasan)

| Entitas | Atribut Kunci | Relasi |
|---|---|---|
| **Admin** | id, username, password_hash | Mengelola Provider & Category (otorisasi/role, bukan FK langsung) |
| **Provider** | id, nama, email, password_hash, no_whatsapp, ktm_path (opsional), status (pending/aktif/ditolak) | 1—N ke Service |
| **Category** | id, nama_kategori, slug | 1—N ke Service |
| **Service** | id, provider_id (FK), category_id (FK), judul, harga, deskripsi, image_path (opsional), status, created_at | 1—N ke Order |
| **Order** | id, service_id (FK), nama_pemesan, nim, kelas, no_whatsapp, catatan, status, created_at | — |

> Catatan: pada sketsa awal `DESIGN.md`, Category digambar bersarang di bawah Provider. Untuk relasi basis data yang lebih baku, Category diperlakukan sebagai tabel master bersama (dikelola Admin) yang direferensikan Service — bukan milik masing-masing provider.
>
> `ktm_path` dan `image_path` menyimpan **path file di Supabase Storage**, bukan file-nya langsung (bukan kolom BLOB). Detail upload & retrieval ada di `FOLDER_STRUCTURE.md`.

## 9. Kategori Layanan Awal (Seed Data)

Jasa Editing · Jasa Desain · Jasa Programming · Tutor · Jastip Makanan · Jastip Minuman · Print/Fotokopi

*(dapat ditambah Admin kapan saja lewat fitur Kelola Kategori)*

## 10. Kriteria Keberhasilan

- [ ] Seluruh 6 Fitur Wajib UAS terimplementasi dan lolos pengujian black-box (ref. template BAB IV.4).
- [ ] CRUD berjalan pada ≥ 2 entitas yang saling berkaitan (Service ↔ Order terpenuhi).
- [ ] Dashboard menampilkan data agregat real-time dari database, bukan angka statis.
- [ ] Aplikasi ter-deploy dan dapat diakses publik di domain `.my.id`.
- [ ] Repository GitHub publik/privat (akses dosen) + `README.md` instalasi lengkap.
- [ ] Video YouTube mencakup alur logika, struktur basis data, kode penting, dan demo seluruh fitur.
- [ ] Laporan mengikuti sistematika template UAS (BAB I–V + Lampiran).

## 11. Asumsi & Batasan

- Topik "CampusHub — Marketplace Layanan Mahasiswa" telah/akan dikonsultasikan dan disetujui dosen pengampu sebelum development dimulai (wajib per ketentuan UAS §2.3).
- Topik bersifat unik di kelas — perlu dipastikan tidak ada mahasiswa lain mengambil topik identik.
- Proyek dikerjakan individu.
- Estimasi coding inti ±3 hari efektif; total timeline termasuk testing, deployment, video, dan laporan ±5–7 hari (lihat §12).
- Tidak ada payment gateway; seluruh transaksi tetap difasilitasi manual via WhatsApp.

## 12. Estimasi Tahapan Pengerjaan

| Tahap | Fokus | Estimasi |
|---|---|---|
| 1 | Setup project, model DB, migrasi, seed kategori | 0.5 hari |
| 2 | Autentikasi Admin & Provider + proteksi route | 0.5 hari |
| 3 | CRUD Layanan (Provider) + halaman publik (Guest) | 1 hari |
| 4 | Alur pemesanan (Guest) + kelola pesanan (Provider) | 0.5 hari |
| 5 | Dashboard Admin + grafik statistik | 0.5 hari |
| 6 | Styling (Bootstrap) + efek 3D/scroll (lihat `DESIGN.md`) | 0.5–1 hari |
| 7 | Testing black-box, perbaikan bug | 0.5 hari |
| 8 | Deployment ke domain `.my.id`, README, video, laporan | 1–1.5 hari |

## 13. Pengembangan Lanjutan (Future Enhancements)

- Sistem rating & ulasan provider.
- Integrasi pembayaran (Midtrans/Xendit) untuk skala lebih luas.
- Notifikasi in-app/email, mengurangi ketergantungan penuh pada WhatsApp manual.
- Chat dalam aplikasi antara guest dan provider.

## 14. Dokumen Terkait

- `WORKFLOW.md` — diagram alur sistem (flowchart, state diagram, sequence diagram).
- `FOLDER_STRUCTURE.md` — struktur folder proyek Flask.
- `DESIGN.md` — konsep awal + spesifikasi efek visual 3D/scroll.