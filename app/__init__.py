import os
from flask import Flask
from app.config import Config
from app.extensions import db, login_manager, csrf
from app.models import Admin, Provider


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    os.makedirs(app.instance_path, exist_ok=True)
    os.makedirs(os.path.join(app.instance_path, 'uploads', 'ktm'), exist_ok=True)

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        if user_id.startswith('admin-'):
            return Admin.query.get(int(user_id.split('-')[1]))
        elif user_id.startswith('provider-'):
            return Provider.query.get(int(user_id.split('-')[1]))
        return None

    from app.routes.public import public_bp
    from app.routes.auth import auth_bp
    from app.routes.provider import provider_bp
    from app.routes.admin import admin_bp

    app.register_blueprint(public_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(provider_bp)
    app.register_blueprint(admin_bp)

    with app.app_context():
        db.create_all()
        _seed(app)

    return app


def _seed(app):
    """Seed admin + categories on first run."""
    from app.models import Category
    if not Admin.query.first():
        admin = Admin(username='admin')
        admin.set_password('admin123')
        db.session.add(admin)

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
