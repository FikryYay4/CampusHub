# 🗂️ Struktur Folder — CampusHub

Struktur proyek Flask berikut mengikuti pola **Application Factory + Blueprint**, disesuaikan untuk deploy di **Vercel** dengan database & storage di **Supabase (PostgreSQL)** — pilihan yang tetap sesuai ketentuan UAS §2.1 ("SQLite (minimal) atau MySQL/PostgreSQL"). Struktur ini juga memisahkan routes/aplikasi utama, templates, static, dan modul koneksi basis data sesuai §2.3.

## Struktur Direktori

```
campushub/
├── app/
│   ├── __init__.py              # Application factory + registrasi blueprint
│   ├── config.py                # Konfigurasi (SECRET_KEY, DATABASE_URL, SUPABASE_*, dsb.)
│   ├── extensions.py            # Inisialisasi db, login_manager, csrf
│   ├── models.py                # Model: Admin, Provider, Category, Service, Order
│   ├── forms.py                 # WTForms — validasi sisi server
│   ├── storage.py               # Helper Supabase Storage (KTM privat + gambar jasa publik)
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── public.py            # Beranda, cari/filter, detail, form pesan
│   │   ├── auth.py              # Login & register (+ upload KTM)
│   │   ├── provider.py          # Dashboard, CRUD jasa (+ gambar), pesanan, endpoint notifikasi
│   │   └── admin.py             # Dashboard, verifikasi provider (+ lihat KTM), kategori, statistik
│   │
│   ├── templates/
│   │   ├── base.html
│   │   ├── partials/
│   │   │   ├── navbar.html      # Badge notifikasi pesanan baru (Provider)
│   │   │   └── footer.html
│   │   ├── public/
│   │   │   ├── home.html
│   │   │   ├── service_list.html    # Menampilkan gambar jasa
│   │   │   ├── service_detail.html
│   │   │   └── order_form.html
│   │   ├── auth/
│   │   │   ├── login.html
│   │   │   └── register.html        # Input upload KTM
│   │   ├── provider/
│   │   │   ├── dashboard.html       # Badge jumlah pesanan baru
│   │   │   ├── service_form.html    # Input upload gambar jasa
│   │   │   └── orders.html
│   │   └── admin/
│   │       ├── dashboard.html
│   │       ├── providers.html       # Pratinjau KTM (signed URL)
│   │       ├── categories.html
│   │       └── services.html
│   │
│   └── static/
│       ├── css/
│       │   └── style.css        # Styling + signature 3D moment (lihat DESIGN.md)
│       ├── js/
│       │   ├── main.js
│       │   ├── scroll-effects.js   # IntersectionObserver momen 3D
│       │   └── notifications.js    # Polling badge pesanan baru
│       └── img/
│
├── migrations/                  # Flask-Migrate (Alembic) — dijalankan via DIRECT_URL
│
├── tests/
│   └── test_routes.py           # Pengujian dasar (mendukung BAB IV.4)
│
├── .env.example                 # DATABASE_URL, DIRECT_URL, SUPABASE_URL, SUPABASE_KEY, SECRET_KEY
├── .gitignore
├── requirements.txt
├── wsgi.py                      # Entry point — otomatis terbaca Vercel (Flask zero-config)
└── README.md                    # Instruksi instalasi & menjalankan aplikasi
```

## Penjelasan & Keterkaitan dengan Ketentuan UAS

| Path | Fungsi | Terkait |
|---|---|---|
| `wsgi.py` | Entry point; Vercel otomatis mendeteksi variabel `app` di sini (Flask zero-config, tanpa `vercel.json`) | Deployment |
| `app/__init__.py` | Application factory, registrasi blueprint | Struktur Proyek §2.3 |
| `app/config.py` | Konfigurasi + connection pooling ke Supabase | — |
| `app/models.py` | Definisi tabel & relasi (SQLAlchemy) | Fitur Wajib #2 |
| `app/forms.py` | Validasi input sisi server | Fitur Wajib #5 |
| `app/storage.py` | Upload/ambil file di Supabase Storage (KTM & gambar jasa) | FR-05, FR-16 |
| `app/routes/auth.py` | Login & registrasi (+ upload KTM) | Fitur Wajib #1, FR-05 |
| `app/routes/admin.py` | Dashboard, verifikasi provider (+ lihat KTM), kategori, statistik | Fitur Wajib #3, #4 |
| `app/routes/provider.py` | CRUD jasa (+ gambar), kelola pesanan, endpoint notifikasi | Fitur Wajib #2, FR-16, FR-17 |
| `app/routes/public.py` | Halaman sisi pengguna umum | Sisi Pengguna Umum |
| `app/templates/` | Tampilan per aktor | Perancangan Antarmuka (UI) §3.4 |
| `app/static/` | CSS/JS termasuk efek 3D & polling notifikasi | Lihat `DESIGN.md` |
| `requirements.txt` | Daftar dependensi | Wajib disertakan §2.3 |
| `README.md` | Panduan instalasi | Wajib dilampirkan §4 |

## Rekomendasi `requirements.txt`

```
Flask
Flask-SQLAlchemy
Flask-Login
Flask-WTF
Flask-Migrate
psycopg2-binary
supabase
python-dotenv
```

*(`psycopg2-binary` = driver Postgres untuk SQLAlchemy; `supabase` = client resmi untuk Storage)*

## Upload File: KTM Provider & Gambar Jasa

Dua jenis file, dua perlakuan berbeda — karena tujuannya beda:

| | KTM Provider | Gambar Jasa |
|---|---|---|
| Siapa yang boleh lihat | Admin saja (verifikasi) | Publik (katalog) |
| Bucket Supabase | `ktm-provider` — **Private** | `service-images` — **Public** |
| Cara akses | `create_signed_url()` — link sementara | `get_public_url()` — link permanen |
| Kolom di database | `Provider.ktm_path` | `Service.image_path` |

Kenapa disimpan di Supabase Storage, bukan folder lokal seperti sebelumnya? Karena filesystem Vercel Functions **tidak persisten** — setiap request bisa jalan di instance yang berbeda, jadi file yang disimpan lokal bisa hilang kapan saja. Supabase Storage jadi tempat penyimpanan file yang independen dari server aplikasi.

**`app/storage.py`** — satu helper untuk kedua kebutuhan:

```python
import os
import uuid
from supabase import create_client

# Dibuat sekali saat cold start, dipakai ulang selama instance masih "hangat"
_supabase = create_client(
    os.environ["SUPABASE_URL"],
    os.environ["SUPABASE_KEY"],  # service_role key — server-side saja, JANGAN pernah dikirim ke browser
)

KTM_BUCKET = "ktm-provider"            # private
SERVICE_IMG_BUCKET = "service-images"  # public

ALLOWED_KTM_EXT = {"jpg", "jpeg", "png", "pdf"}
ALLOWED_IMG_EXT = {"jpg", "jpeg", "png", "webp"}


def _unique_name(filename, allowed):
    ext = filename.rsplit(".", 1)[-1].lower()
    return f"{uuid.uuid4().hex}.{ext}" if ext in allowed else None


def upload_ktm(file_storage):
    """Upload ke bucket privat. Return path untuk kolom Provider.ktm_path, atau None kalau format ditolak."""
    name = _unique_name(file_storage.filename, ALLOWED_KTM_EXT)
    if not name:
        return None
    _supabase.storage.from_(KTM_BUCKET).upload(
        name, file_storage.read(), {"content-type": file_storage.mimetype}
    )
    return name


def get_ktm_url(ktm_path, expires_in=300):
    """Signed URL sementara (default 5 menit) — panggil HANYA di route yang @login_required Admin."""
    if not ktm_path:
        return None
    result = _supabase.storage.from_(KTM_BUCKET).create_signed_url(ktm_path, expires_in)
    return result["signedURL"]  # cek nama key persis di versi package yang terpasang (print(result) kalau beda)


def upload_service_image(file_storage):
    """Upload ke bucket publik. Return path untuk kolom Service.image_path, atau None kalau format ditolak."""
    name = _unique_name(file_storage.filename, ALLOWED_IMG_EXT)
    if not name:
        return None
    _supabase.storage.from_(SERVICE_IMG_BUCKET).upload(
        name, file_storage.read(), {"content-type": file_storage.mimetype}
    )
    return name


def get_service_image_url(image_path):
    """URL publik permanen — aman dipakai langsung di <img src>."""
    if not image_path:
        return None
    return _supabase.storage.from_(SERVICE_IMG_BUCKET).get_public_url(image_path)
```

**Saat registrasi Provider** (`app/routes/auth.py`):

```python
from app.storage import upload_ktm

file = request.files.get('ktm')
ktm_path = upload_ktm(file) if file and file.filename else None
if file and file.filename and not ktm_path:
    flash('Format KTM harus JPG, PNG, atau PDF.', 'error')
    return redirect(url_for('auth.register_provider'))

new_provider = Provider(..., ktm_path=ktm_path)
```

**Saat Provider tambah/edit jasa** (`app/routes/provider.py`):

```python
from app.storage import upload_service_image

file = request.files.get('gambar')
image_path = upload_service_image(file) if file and file.filename else None
if file and file.filename and not image_path:
    flash('Format gambar harus JPG, PNG, atau WEBP.', 'error')
    return redirect(url_for('provider.tambah_jasa'))

new_service = Service(..., image_path=image_path)
```

**Saat menampilkan katalog** (`app/routes/public.py`) — dihitung di route, bukan di template, biar tetap eksplisit:

```python
from app.storage import get_service_image_url

@public_bp.route('/layanan')
def service_list():
    services = Service.query.filter_by(status='approved').all()
    for s in services:
        s.image_url = get_service_image_url(s.image_path)  # atribut sementara, bukan kolom DB
    return render_template('public/service_list.html', services=services)
```

**Saat Admin verifikasi** (`app/routes/admin.py`):

```python
from app.storage import get_ktm_url

@admin_bp.route('/admin/providers/<int:provider_id>')
@login_required
def detail_provider(provider_id):
    provider = Provider.query.get_or_404(provider_id)
    ktm_url = get_ktm_url(provider.ktm_path)
    return render_template('admin/providers.html', provider=provider, ktm_url=ktm_url)
```

Batas ukuran file (berlaku untuk KTM maupun gambar jasa) ditambahkan di `app/config.py` — lihat bagian Deploy di bawah.

## Notifikasi Pesanan Baru (Provider)

**Kenapa bukan WebSocket?** Flask-SocketIO butuh koneksi yang tetap terbuka lama, dan itu tidak cocok dengan Vercel Functions yang sifatnya request/response singkat (serverless, bukan proses yang nyala terus). Solusi yang tetap sederhana dan kompatibel: **hitung ulang status Pending, lalu polling ringan dari browser.**

Tidak perlu kolom baru di database — status `Pending` yang sudah ada di `Order` (lihat `WORKFLOW.md` §5) dipakai langsung sebagai penanda "belum ditindaklanjuti".

**Endpoint hitung + halaman dashboard** (`app/routes/provider.py`):

```python
def _hitung_pesanan_baru():
    return Order.query.join(Service).filter(
        Service.provider_id == current_user.id,
        Order.status == 'Pending'
    ).count()


@provider_bp.route('/provider/dashboard')
@login_required
def dashboard():
    return render_template('provider/dashboard.html', pesanan_baru=_hitung_pesanan_baru())


@provider_bp.route('/provider/api/pesanan-baru')
@login_required
def pesanan_baru_count():
    """Endpoint kecil untuk di-polling JS setiap beberapa detik."""
    return {'count': _hitung_pesanan_baru()}
```

**Polling JS** (`app/static/js/notifications.js`):

```js
(() => {
  const badge = document.querySelector('#pesanan-baru-badge');
  if (!badge) return; // cuma aktif di halaman yang punya badge ini

  const POLL_MS = 30000; // 30 detik — cukup terasa "hidup" tanpa membebani server

  async function refreshBadge() {
    try {
      const res = await fetch('/provider/api/pesanan-baru');
      const { count } = await res.json();
      badge.textContent = count;
      badge.classList.toggle('d-none', count === 0);
    } catch (e) {
      // diamkan; coba lagi di polling berikutnya
    }
  }

  refreshBadge();
  setInterval(refreshBadge, POLL_MS);
})();
```

**Markup badge** (`app/templates/partials/navbar.html`):

```html
<a href="{{ url_for('provider.orders') }}" class="nav-link">
  Pesanan
  <span id="pesanan-baru-badge" class="badge bg-danger {{ 'd-none' if pesanan_baru == 0 else '' }}">
    {{ pesanan_baru }}
  </span>
</a>
```

Kalau nanti mau upgrade ke notifikasi instan tanpa jeda polling, Supabase punya fitur **Realtime** yang bisa didengarkan langsung dari browser setiap ada baris baru masuk ke tabel `orders` — tanpa Flask jadi perantara sama sekali. Untuk kebutuhan UAS, polling 30 detik di atas sudah cukup dan jauh lebih sederhana untuk diimplementasikan dan dijelaskan di video demo.

## Deploy ke Vercel + Supabase

### 1. Setup Supabase
- Buat project baru di [supabase.com](https://supabase.com/dashboard).
- **Project Settings → Database → Connect**: salin connection string mode **Transaction** (port 6543) untuk `DATABASE_URL`, dan mode **Session**/direct (port 5432) untuk `DIRECT_URL` (dipakai migrasi saja).
- **Storage**: buat 2 bucket — `ktm-provider` (**Private**) dan `service-images` (**Public**). Opsional: set `file_size_limit` & `allowed_mime_types` di pengaturan bucket sebagai validasi tambahan sisi server.
- **Project Settings → API**: salin `SUPABASE_URL` dan **service_role key** (bukan `anon key` — service_role diperlukan supaya server bisa upload ke bucket privat tanpa terhalang Row Level Security). Kunci ini rahasia, jangan pernah dipakai di kode sisi browser.

### 2. Koneksi database untuk serverless (`app/config.py`)

```python
import os

SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]  # pooler, port 6543
SQLALCHEMY_ENGINE_OPTIONS = {
    "pool_size": 1,
    "max_overflow": 2,
    "pool_pre_ping": True,   # buang koneksi basi sebelum dipakai
    "pool_recycle": 300,
}
MAX_CONTENT_LENGTH = 2 * 1024 * 1024  # batas upload 2 MB (KTM & gambar jasa)
```

Tiap request Vercel bisa jalan di instance terpisah, jadi pool koneksi sengaja dijaga kecil — biar Supabase Pooler (Supavisor) yang menangani multiplexing-nya. Migrasi (`flask db upgrade`) tetap dijalankan dari komputer lokal memakai `DIRECT_URL`, bukan dari Vercel.

### 3. Entry point (`wsgi.py`)

Vercel kini mendukung Flask tanpa konfigurasi tambahan (tanpa `vercel.json`/folder `api/`) — cukup sediakan variabel bernama `app` di salah satu file berikut, diletakkan di root: `app.py`, `index.py`, `server.py`, `main.py`, `wsgi.py`, atau `asgi.py`. Karena folder aplikasi kita sudah bernama `app/` (package), dipakai `wsgi.py` supaya tidak bentrok nama dengan `app.py`:

```python
# wsgi.py
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
```

### 4. Environment variables di Vercel

Set lewat **Vercel Dashboard → Project → Settings → Environment Variables** — jangan pernah commit `.env` ke Git:

| Key | Isi |
|---|---|
| `SECRET_KEY` | string acak panjang |
| `DATABASE_URL` | connection string pooler Supabase, port 6543 |
| `SUPABASE_URL` | `https://<project-ref>.supabase.co` |
| `SUPABASE_KEY` | service_role key |

### 5. Custom domain `.my.id`

Vercel mendukung custom domain di semua plan termasuk Hobby/gratis — tambahkan lewat **Project → Settings → Domains**, lalu arahkan DNS domain `.my.id` sesuai instruksi yang muncul di sana.

### ⚠️ Supabase Free Tier — Auto-Pause

Project Supabase gratis **otomatis pause setelah 7 hari tanpa aktivitas**; aplikasi yang connect ke database yang ter-pause akan gagal — bukan karena bug di kode. Ini penting karena UAS mensyaratkan aplikasi bisa diakses **selama masa penilaian**.

Mitigasi:
- Paling simpel: buka dashboard Supabase dan klik **Resume** manual H-1 sebelum dinilai.
- Kalau mau lebih aman tanpa harus ingat-ingat: buat 1 GitHub Action/Vercel Cron sederhana yang meng-hit endpoint apa pun di aplikasi (misalnya `/`) sekali sehari — request itu otomatis menjaga project tetap aktif.

## Catatan

- Folder `migrations/` dan `tests/` opsional namun disarankan — `tests/` mendukung dokumentasi pengujian black-box di BAB IV.4 laporan.
- `.env` **wajib** masuk `.gitignore` — isinya password database dan service_role key, bukan sekadar konfigurasi biasa.
- `service_role key` hanya boleh dipakai di kode sisi server (`app/storage.py`, environment variable Vercel) — tidak pernah di JavaScript sisi browser atau di-hardcode di repository.