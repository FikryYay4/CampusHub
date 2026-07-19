# CampusHub — Platform Layanan Mahasiswa Berbasis Web

## Deskripsi
CampusHub adalah sistem informasi berbasis web yang mempertemukan mahasiswa yang membutuhkan jasa dengan mahasiswa penyedia jasa, dalam satu platform terpusat berbasis kampus.

## Tech Stack
- **Backend**: Python 3, Flask, SQLAlchemy, Flask-Login, Flask-WTF
- **Database**: SQLite
- **Frontend**: HTML5, CSS3 (custom design system), Vanilla JavaScript
- **Charts**: Chart.js (CDN)

## Fitur
- **Guest**: Jelajah, cari, filter layanan, pesan tanpa login
- **Provider**: Registrasi, CRUD layanan, kelola pesanan
- **Admin**: Verifikasi provider, kelola kategori, dashboard statistik + grafik

## Instalasi & Menjalankan

```bash
# Clone repository
git clone https://github.com/FikryYay4/CampusHub.git
cd CampusHub

# Buat virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux/Mac

# Install dependensi
pip install -r requirements.txt

# Jalankan aplikasi
python run.py
```

Buka http://127.0.0.1:5000 di browser.

## Login Default
- **Admin**: username `admin`, password `admin123`
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
│   ├── routes/              # Blueprint routes
│   ├── templates/           # Jinja2 templates
│   └── static/              # CSS, JS, images
├── instance/                # SQLite DB + uploads
├── tests/                   # Pengujian
├── docs/                    # Dokumentasi
├── run.py                   # Entry point
└── requirements.txt
```

## Kategori Layanan
Jasa Editing · Jasa Desain · Jasa Programming · Tutor · Jastip Makanan · Jastip Minuman · Print/Fotokopi

## Lisensi
Proyek UAS Pengantar Pemrograman — 2026
