# CampusHub — Platform Layanan Mahasiswa Berbasis Web

## Deskripsi
CampusHub adalah sistem informasi berbasis web yang mempertemukan mahasiswa yang membutuhkan jasa dengan mahasiswa penyedia jasa, dalam satu platform terpusat berbasis kampus.

## Tech Stack
- **Backend**: Python 3.11+, Flask, SQLAlchemy, Flask-Login, Flask-WTF
- **Database**: SQLite (lokal / testing) & PostgreSQL Supabase (production)
- **Storage**: Local filesystem (lokal / testing) & Supabase Storage (production)
- **Frontend**: HTML5, CSS3 (custom design system), Vanilla JavaScript
- **Charts**: Chart.js (CDN)

## Fitur
- **Guest**: Jelajah, cari, filter layanan, pesan tanpa login
- **Provider**: Registrasi, CRUD layanan, kelola pesanan
- **Admin**: Verifikasi provider, kelola kategori, kelola layanan (approve/reject/delete), dashboard statistik + grafik

## Instalasi & Menjalankan (Lokal)

```bash
# Clone repository
git clone https://github.com/FikryYay4/CampusHub.git
cd CampusHub

# Buat virtual environment
python -m venv venv
source venv/Scripts/activate  # Windows
# source venv/bin/activate    # Linux/Mac

# Install dependensi
pip install -r requirements.txt

# Setup Environment Variables
cp .env.example .env
# Edit .env dengan variabel Anda

# Jalankan aplikasi
python run.py
```

Buka http://127.0.0.1:5000 di browser.

## Deployment ke Vercel + Supabase

### 1. Setup Supabase
- Buat proyek di [supabase.com](https://supabase.com/).
- Buat 2 storage buckets: `ktm-provider` (Private) dan `service-images` (Public).
- Dapatkan `DATABASE_URL` (pooler port 6543) dan `DIRECT_URL` (port 5432).

### 2. Environment Variables di Vercel
Tambahkan variabel berikut di pengaturan proyek Vercel Anda:
- `SECRET_KEY`
- `DATABASE_URL`
- `SUPABASE_URL`
- `SUPABASE_KEY` (service_role key)
- `ADMIN_PASSWORD` (opsional, untuk mendefinisikan password admin default)

## Login Default
- **Admin**: username `admin`, password `admin123_SecureCampusHub` (atau sesuai `ADMIN_PASSWORD` di env)
- **Provider**: Daftar melalui halaman registrasi, tunggu approval admin

## Struktur Folder
```
campushub/
├── app/
│   ├── __init__.py          # Application factory
│   ├── config.py            # Konfigurasi
│   ├── extensions.py        # DB, Login, CSRF
│   ├── models.py            # Model database
│   ├── forms.py             # WTForms validasi
│   ├── storage.py           # Supabase Storage helper (KTM privat & Jasa publik)
│   ├── routes/              # Blueprint routes
│   ├── templates/           # Jinja2 templates
│   └── static/              # CSS, JS, images
├── instance/                # Lokal uploads
├── tests/                   # Pengujian
├── docs/                    # Dokumentasi & PRD
├── wsgi.py                  # Entry point (Vercel)
└── requirements.txt
```

## Lisensi
Proyek UAS Pengantar Pemrograman — 2026
