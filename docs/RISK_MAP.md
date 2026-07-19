# 🔍 Risk Map & Gap Analysis — CampusHub

Review dilakukan dengan clone langsung repo [FikryYay4/CampusHub](https://github.com/FikryYay4/CampusHub) (commit `bc4679a`) dan membaca seluruh source code (routes, models, forms, storage, templates, config, tests) — bukan cuma nebak dari nama file. Dicocokkan juga ke `PRD.md`, `WORKFLOW.md`, `FOLDER_STRUCTURE.md`, `DESIGN.md`, dan soal UAS.

**Catatan jujur:** ini review level kode, bukan hasil klik-klik aplikasi yang jalan — jadi soal "kelihatan bagus/tidaknya" secara visual di browser, saya nggak bisa nilai dari sini. Yang bisa saya pastikan adalah apa yang benar-benar ada (atau nggak ada) di kode.

---

## ✅ Kekuatan (biar nggak cuma isinya kritik)

- **Ownership check konsisten** — `edit_service`, `delete_service`, `update_order` semua mengecek `provider_id == current_user.id` sebelum mengizinkan aksi. Banyak proyek mahasiswa lupa ini (celah IDOR); punya Ahmad sudah aman.
- **CSRF token lengkap** — dicek ke semua template yang punya `<form method="POST">`, semuanya sudah menyertakan `csrf_token`.
- **Validasi form solid** — regex nomor WhatsApp (`^08\d{8,13}$`), `FileAllowed` untuk tipe file, `EqualTo` untuk konfirmasi password, `NumberRange` untuk harga. Ini persis yang diminta Fitur Wajib #5.
- **Signature 3D moment terpasang sesuai spek** — `.service-fan` + `IntersectionObserver` di `scroll-effects.js` cocok dengan desain di `DESIGN.md`, termasu `prefers-reduced-motion` dihormati di CSS.
- **Test suite black-box beneran end-to-end** — `test_routes.py` mengetes alur registrasi → pending → approve → login → tambah jasa → guest pesan → accept → complete. Cakupannya bagus untuk ukuran proyek UAS.
- **Fallback gambar layanan rapi** — kalau `image_path` kosong, semua halaman publik menampilkan placeholder (🎓), bukan gambar rusak.
- **Kategori dilindungi dari orphan** — `delete_category` menolak hapus kategori yang masih dipakai jasa.
- **`docs/PRD.md` & `docs/FOLDER_STRUCTURE.md` sudah identik dengan versi terbaru** yang kita susun bareng — bagus untuk kelengkapan laporan UAS.

---

## 🗺️ Peta Risiko

*(Diagram di atas memplot posisi tiap temuan; tabel di bawah rinciannya. "Kemungkinan" = seberapa besar ini bakal ketahuan/kejadian sebelum atau saat dinilai — bukan probabilitas abstrak, karena sebagian besar ini fakta yang sudah ada di kode sekarang.)*

### 🔴 Kritis

| Risiko | Lokasi | Dampak | Kemungkinan | Mitigasi |
|---|---|---|---|---|
| Kredensial admin default (`admin`/`admin123`) di-*hardcode*, otomatis di-seed tiap start, **dan ditulis apa adanya di README.md publik** | `app/__init__.py` (`_seed`), `README.md` | Siapa pun bisa login sebagai Admin di aplikasi yang sudah live — approve/reject provider, hapus jasa/kategori, lihat semua data | Tinggi — sudah publik di GitHub sekarang juga | 1) Ganti password admin di deployment sungguhan, sekarang. 2) Hapus baris kredensial dari README. 3) Idealnya jangan auto-seed password tetap — generate password acak sekali saat pertama jalan, atau haruskan admin dibuat manual di production |

### 🟠 Tinggi

| Risiko | Lokasi | Dampak | Kemungkinan | Mitigasi |
|---|---|---|---|---|
| `storage.py` diam-diam fallback ke filesystem lokal kalau `SUPABASE_URL`/`SUPABASE_KEY` kosong atau gagal — dan `config.py` diam-diam fallback ke SQLite kalau `DATABASE_URL` kosong | `app/storage.py` (`_get_supabase`), `app/config.py` | Kalau env var di Vercel salah/lupa diisi, upload & data **tidak error jelas** — malah "jalan" dengan cara yang rusak di filesystem serverless yang tidak persisten. Inilah tepatnya skenario yang arsitektur Supabase kita rancang untuk dihindari | Sedang — tergantung ketelitian isi env var di Vercel dashboard | Tes deploy ke Vercel *sekarang*, bukan H-1. Cek log/behavior kalau salah satu env var kosong. Pertimbangkan bikin fallback ini melempar error jelas alih-alih diam-diam menyala |
| Route `/admin/ktm/<filename>` crash — `os.path.join(...)` dipanggil tapi **`import os` tidak ada** di `admin.py` | `app/routes/admin.py` baris 94 | `NameError` setiap kali Admin klik lihat KTM dalam mode fallback lokal | Sedang — hanya muncul saat fallback lokal aktif, tapi kalau aktif, pasti crash | Tambahkan `import os` di baris atas `admin.py` (perbaikan 1 baris) |

### 🔵 Sedang

| Risiko | Lokasi | Dampak | Kemungkinan | Mitigasi |
|---|---|---|---|---|
| Flash message ditiadakan di halaman publik (`docs/MEMORY.md`: "untuk menjaga kebersihan visual") | `app/routes/public.py` (tidak ada `flash()` sama sekali) | Fitur Wajib #6 UAS eksplisit menyebut *"flash message"* by name. Kegagalan submit order sebenarnya sudah tertolong oleh error inline WTForms (`service_detail.html`), tapi ini bukan mekanisme flash — kalau dosen membaca ketentuan secara harfiah, ini bisa jadi poin minus | Tinggi — kondisinya sudah begini | Tambahkan minimal 1 `flash()` di jalur publik (misal saat order berhasil dikirim) supaya "flash message" benar-benar ada, bukan cuma halaman sukses statis |
| Tidak ada alur approval untuk **jasa baru** oleh Admin — `Service.status` langsung `'active'` saat dibuat, tidak ada endpoint approve/reject jasa (beda dengan provider yang sudah ada) | `app/models.py`, `app/routes/provider.py`, `app/routes/admin.py` | Bertentangan dengan `WORKFLOW.md` §4 dan algoritma asli di `DESIGN.md` ("Menunggu Verifikasi Admin" → "Jasa Tampil"). Kalau diagram itu dipakai apa adanya di laporan, akan tidak cocok dengan aplikasi yang didemokan | Tinggi — ini sudah jadi perilaku aplikasi sekarang | Pilih salah satu: (a) update `WORKFLOW.md`/`DESIGN.md` supaya bilang "jasa tayang langsung, hanya provider yang diverifikasi" — simplifikasi yang sah dan tetap masuk akal, atau (b) tambah endpoint approve/reject jasa supaya cocok dokumen |
| `README.md` menyebut **Database: SQLite**, instruksi instalasi tidak menyinggung `.env`/Supabase/environment variables sama sekali | `README.md` | README adalah lampiran wajib UAS ("menjelaskan cara instalasi dan menjalankan aplikasi") — kalau diikuti persis, orang tidak akan tahu cara menyalakan versi Postgres/Supabase yang sebenarnya di-deploy | Tinggi — README pasti dibaca saat penilaian | Update README: sebut Postgres (Supabase), tambahkan langkah isi `.env` dari `.env.example`, sebut cara setup bucket Storage |
| `SQLALCHEMY_ENGINE_OPTIONS` di `config.py` cuma set `pool_pre_ping` & `pool_recycle` — `pool_size`/`max_overflow` belum diset eksplisit seperti yang dirancang di `FOLDER_STRUCTURE.md` | `app/config.py` | Default SQLAlchemy (pool_size 5, max_overflow 10) bisa lebih boros koneksi dari yang dibutuhkan di serverless, berisiko membebani pooler Supabase saat beberapa request masuk bersamaan | Rendah untuk demo biasa, naik kalau diakses banyak orang bersamaan (mis. pas sesi penilaian ramai) | Tambahkan `'pool_size': 1, 'max_overflow': 2` |
| Test suite **tidak pernah menguji jalur Supabase/Postgres asli** — fixture eksplisit mengosongkan `SUPABASE_URL`/`SUPABASE_KEY` dan pakai `sqlite:///:memory:` | `tests/test_routes.py` | Semua test hijau tidak membuktikan integrasi Supabase Storage/Postgres benar-benar berfungsi — false confidence | Sedang | Tidak wajib, tapi kalau sempat: 1 test terpisah yang jalan dengan Supabase asli (atau minimal test `storage.py` dengan mock) |

### ⚪ Rendah

| Risiko | Lokasi | Dampak | Kemungkinan | Mitigasi |
|---|---|---|---|---|
| Transisi status order tidak divalidasi — `update_order` menerima `accept/reject/complete` apa adanya tanpa mengecek status saat ini, jadi urutan tidak sah (mis. `completed` → `accepted` lagi) secara teknis bisa terjadi lewat POST langsung | `app/routes/provider.py` (`update_order`) | Menyimpang dari state diagram di `WORKFLOW.md` §5, tapi butuh request yang sengaja dibuat untuk memicu | Rendah | Tambahkan pengecekan status saat ini sebelum mengizinkan transisi |
| Flash `"Message deleted!"` (Bahasa Inggris, generic) muncul saat Admin hapus jasa — beda sendiri dari semua flash message lain yang berbahasa Indonesia | `app/routes/admin.py` (`delete_service`, `delete_category`) | Kecil secara fungsi, tapi mencolok dan tidak konsisten saat demo/video | Tinggi — pasti kelihatan begitu tombol hapus dicoba | Ganti ke `"Layanan berhasil dihapus."` / `"Kategori berhasil dihapus."` |
| Palet warna & font meniru cukup persis identitas visual **Itemku** (marketplace nyata) — hex `#2C77D2`/`#1859AA`/`#FFC107` dan pasangan font sama persis seperti tercatat di `docs/MEMORY.md` | `app/static/css/style.css` | Bukan masalah hukum di level ini (warna/font sendirian sulit diklaim IP), tapi dari sisi orisinalitas akademik kurang ideal kalau dosen mengenali sumbernya | Rendah-Sedang, tergantung apakah dosen familiar dengan Itemku | Geser sedikit huenya / ganti pasangan font supaya tidak 1:1 |
| File duplikat `docs/DESIGN (1).md` tertinggal di samping `docs/DESIGN.md` | `docs/` | Kosmetik — bikin repo terlihat kurang rapi kalau di-browse | Rendah | Hapus file duplikatnya |
| `run.py` dan `wsgi.py` isinya identik persis | root | Redundan, tidak berbahaya | Rendah | Boleh dibiarkan, atau pertahankan `wsgi.py` saja dan update README supaya konsisten menyebut satu entry point |

---

## 🎨 Soal "apa yang kurang" — kesenjangan desain & dokumentasi

Beberapa hal yang bukan "bug" tapi lebih ke *belum selesai/belum konsisten* dibanding rencana awal:

1. **README paling jauh tertinggal dari implementasi sebenarnya** di antara semua dokumen — ini yang paling penting diperbaiki duluan karena README adalah salah satu dari 4 lampiran wajib UAS yang eksplisit dinilai.
2. **`WORKFLOW.md` dan kode sudah tidak 1:1** di bagian approval jasa — kalau laporan BAB III.2 memakai diagram `WORKFLOW.md` apa adanya, videonya perlu menjelaskan bagian ini konsisten dengan yang benar-benar didemokan, atau diagramnya disesuaikan dulu.
3. **Belum ada bukti aplikasi sudah benar-benar tersambung ke Supabase/Vercel yang sesungguhnya** — semua yang saya baca adalah kode yang *seharusnya* bekerja dengan Supabase, tapi test suite sengaja menghindari jalur itu. Sebelum submit, ini satu-satunya cara memastikan: deploy sungguhan ke Vercel, lalu coba semua fitur upload & lihat KTM di sana, bukan cuma di localhost.
4. **Identitas visual belum sepenuhnya "milik" CampusHub** — palet Itemku memang jadi titik awal yang wajar untuk moodboard, tapi untuk deliverable akhir ada baiknya digeser jadi khas sendiri.
5. **Momen 3D-nya sendiri sudah pas dan sesuai rencana** — ini bukan kekurangan, tapi saya sebut biar jelas: dari sisi "efek 3D di scroll" yang diminta di awal percakapan, itu bagian yang paling solid.

---

## ✅ Rekomendasi Prioritas (kalau waktu terbatas, urutkan begini)

1. **Ganti password admin di deployment nyata sekarang juga**, hapus dari README.
2. **Tambahkan `import os` di `app/routes/admin.py`.**
3. **Deploy ke Vercel + Supabase sungguhan dan uji semua fitur upload di sana** — jangan tunggu H-1, supaya sisa waktu masih cukup kalau env var-nya ternyata salah.
4. **Update `README.md`** supaya menyebut Postgres/Supabase dan langkah isi `.env`, bukan SQLite.
5. **Putuskan soal approval jasa**: selaraskan `WORKFLOW.md`/`DESIGN.md` dengan kode (dua-duanya sah, yang penting konsisten sebelum ditulis di laporan).
6. Kalau masih ada waktu: `"Message deleted!"` → Bahasa Indonesia, tambah `pool_size`/`max_overflow`, validasi transisi status order, hapus `docs/DESIGN (1).md`.
