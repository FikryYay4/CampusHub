from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app.extensions import db


class Admin(UserMixin, db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, pw):
        self.password_hash = generate_password_hash(pw)

    def check_password(self, pw):
        return check_password_hash(self.password_hash, pw)

    @property
    def role(self):
        return 'admin'

    def get_id(self):
        return f'admin-{self.id}'


class Provider(UserMixin, db.Model):
    __tablename__ = 'provider'
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    no_whatsapp = db.Column(db.String(20), nullable=False)
    ktm_path = db.Column(db.String(256), nullable=True)  # Supabase Storage path or local filename
    status = db.Column(db.String(20), default='pending')  # pending / aktif / ditolak
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    services = db.relationship('Service', backref='provider', lazy=True, cascade='all, delete-orphan')

    def set_password(self, pw):
        self.password_hash = generate_password_hash(pw)

    def check_password(self, pw):
        return check_password_hash(self.password_hash, pw)

    @property
    def role(self):
        return 'provider'

    def get_id(self):
        return f'provider-{self.id}'


class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    nama_kategori = db.Column(db.String(64), unique=True, nullable=False)
    slug = db.Column(db.String(64), unique=True, nullable=False)

    services = db.relationship('Service', backref='category', lazy=True)


class Service(db.Model):
    __tablename__ = 'service'
    id = db.Column(db.Integer, primary_key=True)
    provider_id = db.Column(db.Integer, db.ForeignKey('provider.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    judul = db.Column(db.String(128), nullable=False)
    deskripsi = db.Column(db.Text, nullable=False)
    harga = db.Column(db.Integer, nullable=False)
    image_path = db.Column(db.String(256), nullable=True)  # Supabase Storage path or local filename
    status = db.Column(db.String(20), default='active')  # active / inactive
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    orders = db.relationship('Order', backref='service', lazy=True, cascade='all, delete-orphan')


class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    nama_pemesan = db.Column(db.String(128), nullable=False)
    nim = db.Column(db.String(20), nullable=False)
    kelas = db.Column(db.String(20), nullable=False)
    no_whatsapp = db.Column(db.String(20), nullable=False)
    catatan = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='pending')  # pending / accepted / rejected / completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
