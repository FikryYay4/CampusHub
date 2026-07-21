import os
from flask import Flask, send_from_directory
from werkzeug.exceptions import HTTPException
from app.config import Config
from app.extensions import db, login_manager, csrf
from app.models import Admin, Provider


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Use /tmp for writable directories on Vercel
    upload_path = os.environ.get('UPLOAD_FOLDER', os.path.join('/tmp', 'uploads'))
    os.makedirs(upload_path, exist_ok=True)
    app.config['UPLOAD_FOLDER'] = upload_path

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        if not user_id:
            return None
        try:
            role, uid = user_id.split('-', 1)
            uid = int(uid)
            if role == 'admin':
                return Admin.query.get(uid)
            elif role == 'provider':
                return Provider.query.get(uid)
        except Exception:
            return None
        return None

    # Log all unhandled errors to Vercel runtime logs
    @app.errorhandler(Exception)
    def handle_error(e):
        if isinstance(e, HTTPException):
            return e
        import traceback
        tb = traceback.format_exc()
        print("TRACE:" + tb.replace("\n", "\\n"))
        return "Internal Server Error", 500

    # Serve static uploads route when local storage is used
    @app.route('/uploads/<path:filename>')
    def static_uploads(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    from app.routes.public import public_bp
    from app.routes.auth import auth_bp
    from app.routes.provider import provider_bp
    from app.routes.admin import admin_bp

    app.register_blueprint(public_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(provider_bp)
    app.register_blueprint(admin_bp)

    # Inject pesanan_baru for provider navbar
    @app.context_processor
    def inject_pesanan_baru():
        from flask_login import current_user
        from app.models import Order, Service
        pesanan_baru = 0
        if current_user.is_authenticated and current_user.role == 'provider':
            pesanan_baru = Order.query.join(Service).filter(
                Service.provider_id == current_user.id,
                Order.status == 'pending'
            ).count()
        return {'pesanan_baru': pesanan_baru}

    # Ensure Supabase storage buckets (non-fatal)
    _ensure_storage_buckets(app)

    # Initialize database — tables may already exist, so failure is non-fatal
    with app.app_context():
        try:
            db.create_all()
            _seed(app)
        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"DB init failed (non-fatal): {e}")

    return app


def _ensure_storage_buckets(app):
    """Create Supabase storage buckets if missing. Uses raw REST API."""
    url = app.config.get('SUPABASE_URL', '')
    svc_key = os.environ.get('SUPABASE_SERVICE_KEY', '')
    if not (url and svc_key):
        print("SKIP bucket creation: SUPABASE_SERVICE_KEY not set")
        return
    try:
        import httpx
        from app.storage import KTM_BUCKET, SERVICE_IMG_BUCKET
        headers = {"authorization": f"Bearer {svc_key}", "apikey": svc_key}
        api = f"{url}/storage/v1/bucket"
        existing = [b["name"] for b in httpx.get(api, headers=headers).json()]
        for bucket, public in [(KTM_BUCKET, False), (SERVICE_IMG_BUCKET, True)]:
            if bucket not in existing:
                r = httpx.post(api, headers=headers, json={"name": bucket, "public": public})
                r.raise_for_status()
                print(f"Created bucket: {bucket}")
    except Exception as e:
        print(f"Bucket creation skipped (non-fatal): {e}")


def _seed(app):
    from app.models import Category
    # Seed default admin if none
    if not Admin.query.first():
        admin = Admin(username='admin')
        admin.set_password(os.environ.get('ADMIN_PASSWORD', 'admin123_SecureCampusHub'))
        db.session.add(admin)

    # Seed default categories
    seeds = [
        ('Jasa Editing', 'jasa-editing'),
        ('Jasa Desain', 'jasa-desain'),
        ('Jasa Programming', 'jasa-programming'),
        ('Tutor', 'tutor'),
        ('Jastip Makanan', 'jastip-makanan'),
        ('Jastip Minuman', 'jastip-minuman'),
        ('Print/Fotokopi', 'print-fotokopi'),
    ]
    for nama, slug in seeds:
        if not Category.query.filter_by(slug=slug).first():
            db.session.add(Category(nama_kategori=nama, slug=slug))

    db.session.commit()
