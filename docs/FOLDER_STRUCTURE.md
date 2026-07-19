# 🗂️ Struktur Folder — CampusHub

Struktur proyek Flask berikut mengikuti pola **Application Factory + Blueprint**, sesuai ketentuan UAS §2.3 (pemisahan routes/aplikasi utama, templates, static, dan modul koneksi basis data), sekaligus memudahkan pengembangan bertahap per aktor (Guest, Provider, Admin).

## Struktur Direktori

```
campushub/
├── app/
│   ├── __init__.py              # Application factory + registrasi blueprint
│   ├── config.py                # Konfigurasi (SECRET_KEY, DB URI, dsb.)
│   ├── extensions.py            # Inisialisasi db, login_manager, csrf
│   ├── models.py                # Model: Admin, Provider, Category, Service, Order
│   ├── forms.py                 # WTForms — validasi sisi server
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── public.py            # Beranda, cari/filter, detail, form pesan
│   │   ├── auth.py              # Login & register (Admin + Provider)
│   │   ├── provider.py          # Dashboard, CRUD jasa, kelola pesanan
│   │   └── admin.py             # Dashboard, verifikasi provider, kategori, statistik
│   │
│   ├── templates/
│   │   ├── base.html            # Layout utama (navbar, footer, block content)
│   │   ├── partials/
│   │   │   ├── navbar.html
│   │   │   └── footer.html
│   │   ├── public/
│   │   │   ├── home.html
│   │   │   ├── service_list.html
│   │   │   ├── service_detail.html
│   │   │   └── order_form.html
│   │   ├── auth/
│   │   │   ├── login.html
│   │   │   └── register.html
│   │   ├── provider/
│   │   │   ├── dashboard.html
│   │   │   ├── service_form.html
│   │   │   └── orders.html
│   │   └── admin/
│   │       ├── dashboard.html
│   │       ├── providers.html
│   │       ├── categories.html
│   │       └── services.html
│   │
│   └── static/
│       ├── css/
│       │   └── style.css        # Styling utama + signature 3D moment (lihat DESIGN.md)
│       ├── js/
│       │   ├── main.js
│       │   └── scroll-effects.js # IntersectionObserver untuk momen 3D di hero
│       └── img/
│
├── instance/
│   ├── campushub.db             # SQLite database (masuk .gitignore)
│   └── uploads/
│       └── ktm/                 # File KTM provider — di luar static/, tidak diserve publik
│
├── migrations/                  # Flask-Migrate (opsional, jika dipakai)
│
├── tests/
│   └── test_routes.py           # Pengujian dasar (mendukung BAB IV.4)
│
├── .env.example                 # Contoh variabel lingkungan
├── .gitignore
├── requirements.txt              # flask, flask-sqlalchemy, flask-login, flask-wtf, dst.
├── run.py                       # Entry point aplikasi
└── README.md                    # Instruksi instalasi & menjalankan aplikasi
```

## Penjelasan & Keterkaitan dengan Ketentuan UAS

| Path | Fungsi | Terkait |
|---|---|---|
| `run.py` | Entry point (`flask run` / `python run.py`) | — |
| `app/__init__.py` | Application factory, registrasi blueprint | Struktur Proyek §2.3 |
| `app/config.py` | Konfigurasi environment (dev/prod) | — |
| `app/models.py` | Definisi tabel & relasi (SQLAlchemy) | Fitur Wajib #2 (CRUD entitas terkait) |
| `app/forms.py` | Validasi input sisi server | Fitur Wajib #5 |
| `app/routes/auth.py` | Login & registrasi (termasuk terima upload KTM) session-based | Fitur Wajib #1, FR-05 |
| `app/routes/admin.py` | Dashboard, verifikasi provider (termasuk lihat KTM), kategori, statistik | Fitur Wajib #3, #4 |
| `app/routes/provider.py` | CRUD jasa & kelola pesanan | Fitur Wajib #2 |
| `app/routes/public.py` | Halaman sisi pengguna umum | Sisi Pengguna Umum |
| `app/templates/` | Tampilan per aktor | Perancangan Antarmuka (UI) §3.4 |
| `app/static/` | CSS/JS termasuk efek 3D/scroll | Lihat `DESIGN.md` |
| `instance/campushub.db` | Database SQLite | Basis Data §2.1 |
| `instance/uploads/ktm/` | File KTM yang diupload provider saat registrasi (bukan folder publik) | FR-05, Fitur Wajib #5 |
| `requirements.txt` | Daftar dependensi | Wajib disertakan §2.3 |
| `README.md` | Panduan instalasi | Wajib dilampirkan §4 |

## Rekomendasi `requirements.txt`

```
Flask
Flask-SQLAlchemy
Flask-Login
Flask-WTF
python-dotenv
```

*(tambahkan `Flask-Migrate` jika ingin mengelola migrasi skema database secara formal)*

## Upload KTM Provider

KTM cuma perlu dilihat Admin untuk verifikasi provider (FR-07) — bukan konten publik. Karena itu file-nya sengaja **tidak** ditaruh di `app/static/`: apa pun yang ada di situ otomatis bisa diakses lewat URL oleh siapa saja yang tahu nama filenya, meski tidak pernah di-link di halaman manapun.

Sebagai gantinya, KTM disimpan di `instance/uploads/ktm/` — folder ini tidak diserve otomatis oleh Flask, jadi cuma bisa diakses lewat route yang sengaja dibuat dan diproteksi `login_required` khusus Admin.

**Saat registrasi** (`app/routes/auth.py`):

```python
import os, uuid
from werkzeug.utils import secure_filename

ALLOWED_EXT = {'jpg', 'jpeg', 'png', 'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXT

# setelah validasi field form lainnya:
file = request.files.get('ktm')
ktm_filename = None
if file and file.filename:
    if not allowed_file(file.filename):
        flash('Format KTM harus JPG, PNG, atau PDF.', 'error')
        return redirect(url_for('auth.register_provider'))
    ext = secure_filename(file.filename).rsplit('.', 1)[1]
    ktm_filename = f"{uuid.uuid4().hex}.{ext}"
    upload_dir = os.path.join(current_app.instance_path, 'uploads', 'ktm')
    os.makedirs(upload_dir, exist_ok=True)
    file.save(os.path.join(upload_dir, ktm_filename))

new_provider = Provider(..., ktm_filename=ktm_filename)  # simpan nama file, bukan file-nya, ke DB
```

**Saat Admin verifikasi** (`app/routes/admin.py`):

```python
from flask import send_from_directory, current_app
from flask_login import login_required

@admin_bp.route('/admin/ktm/<path:filename>')
@login_required
def view_ktm(filename):
    upload_dir = os.path.join(current_app.instance_path, 'uploads', 'ktm')
    return send_from_directory(upload_dir, filename)
```

**Batas ukuran file** — tambahkan di `app/config.py` supaya Flask otomatis menolak file yang kelewat besar (validasi sisi server, Fitur Wajib #5):

```python
MAX_CONTENT_LENGTH = 2 * 1024 * 1024  # 2 MB
```

Untuk validasi sisi client, cukup tambahkan `accept=".jpg,.jpeg,.png,.pdf"` pada `<input type="file">` di `register.html` — bukan pengganti validasi server di atas, hanya mempercepat feedback ke pengguna.

## Catatan

- Folder `migrations/` dan `tests/` opsional namun disarankan — `tests/` mendukung dokumentasi pengujian black-box di BAB IV.4 laporan.
- `instance/` sebaiknya dimasukkan ke `.gitignore` agar database lokal tidak ikut ter-commit.
- Tidak ada dependensi JS pihak ketiga yang perlu ditambahkan — signature moment 3D di `DESIGN.md` memakai CSS + vanilla JS saja, jadi `requirements.txt` di atas sudah cukup.
