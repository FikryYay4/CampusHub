"""Black-box tests for CampusHub routes."""
import os
import sys
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app import create_app
from app.extensions import db
from app.models import Admin, Provider, Category, Service, Order


@pytest.fixture
def client(monkeypatch):
    # Disable Supabase environment variables during test so storage fallbacks to local filesystem
    monkeypatch.setenv('SUPABASE_URL', '')
    monkeypatch.setenv('SUPABASE_KEY', '')

    app = create_app()
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.app_context():
        db.drop_all()
        db.create_all()
        # Seed admin
        admin = Admin(username='admin')
        admin.set_password('admin123')
        db.session.add(admin)
        # Seed categories
        cats = [
            Category(nama_kategori='Tutor', slug='tutor'),
            Category(nama_kategori='Jasa Desain', slug='jasa-desain')
        ]
        db.session.add_all(cats)
        db.session.commit()

    with app.test_client() as c:
        with app.app_context():
            yield c


def test_home_page(client):
    rv = client.get('/')
    assert rv.status_code == 200
    assert b'CampusHub' in rv.data


def test_service_list(client):
    rv = client.get('/services')
    assert rv.status_code == 200
    assert b'Daftar Layanan' in rv.data


def test_login_page(client):
    rv = client.get('/login')
    assert rv.status_code == 200
    assert b'Login' in rv.data


def test_register_page(client):
    rv = client.get('/register')
    assert rv.status_code == 200
    assert b'Daftar sebagai Provider' in rv.data


def test_admin_login_and_dashboard(client):
    # Success Login
    rv = client.post('/login', data={'username': 'admin', 'password': 'admin123'}, follow_redirects=True)
    assert rv.status_code == 200
    assert b'Dashboard Admin' in rv.data

    # View categories
    rv = client.get('/admin/categories')
    assert rv.status_code == 200
    assert b'Kelola Kategori' in rv.data

    # Add category
    rv = client.post('/admin/categories', data={'nama_kategori': 'Jasa Foto'}, follow_redirects=True)
    assert rv.status_code == 200
    assert b'Jasa Foto' in rv.data


def test_provider_register_and_login(client):
    # Register Provider
    rv = client.post('/register', data={
        'nama': 'Mochammad Fikry',
        'email': 'fikry@example.com',
        'password': 'password123',
        'confirm_password': 'password123',
        'no_whatsapp': '081234567890',
    }, follow_redirects=True)
    assert rv.status_code == 200

    # Try login (fails because still pending)
    rv = client.post('/login', data={'username': 'fikry@example.com', 'password': 'password123'}, follow_redirects=True)
    assert b'belum aktif' in rv.data or b'Login' in rv.data

    # Approve provider using admin session
    # Log in as admin
    client.post('/login', data={'username': 'admin', 'password': 'admin123'})
    p = Provider.query.filter_by(email='fikry@example.com').first()
    assert p is not None
    assert p.status == 'pending'

    # Approve post
    rv = client.post(f'/admin/providers/{p.id}/approve', follow_redirects=True)
    assert rv.status_code == 200

    # Assert active
    db.session.refresh(p)
    assert p.status == 'aktif'

    # Logout admin
    client.get('/logout')

    # Login provider now succeeds
    rv = client.post('/login', data={'username': 'fikry@example.com', 'password': 'password123'}, follow_redirects=True)
    assert rv.status_code == 200
    assert b'Dashboard Provider' in rv.data


def test_provider_crud_and_guest_ordering(client):
    # Register & approve provider
    p = Provider(nama='Fikry', email='fikry2@example.com', no_whatsapp='081212121212', status='aktif')
    p.set_password('password123')
    db.session.add(p)
    db.session.commit()

    # Login provider
    client.post('/login', data={'username': 'fikry2@example.com', 'password': 'password123'})

    # Add service
    cat = Category.query.filter_by(slug='tutor').first()
    rv = client.post('/provider/services/add', data={
        'judul': 'Tutor Python Dasar',
        'category_id': cat.id,
        'harga': 50000,
        'deskripsi': 'Belajar Python bareng Fikry dari nol sampai bisa.',
    }, follow_redirects=True)
    assert rv.status_code == 200
    assert b'Tutor Python Dasar' in rv.data

    svc = Service.query.filter_by(judul='Tutor Python Dasar').first()
    assert svc is not None

    # Logout provider
    client.get('/logout')

    # Guest places order on this service
    rv = client.post(f'/services/{svc.id}/order', data={
        'nama_pemesan': 'Budi Pemesan',
        'nim': '12345678',
        'kelas': 'IF-4A',
        'no_whatsapp': '089876543210',
        'catatan': 'Mau tutor hari sabtu besok.',
    }, follow_redirects=True)
    assert rv.status_code == 200
    assert b'Pesanan Berhasil Dikirim' in rv.data

    # Log in provider to check and process order
    client.post('/login', data={'username': 'fikry2@example.com', 'password': 'password123'})
    rv = client.get('/provider/orders')
    assert rv.status_code == 200
    assert b'Budi Pemesan' in rv.data

    order = Order.query.filter_by(nama_pemesan='Budi Pemesan').first()
    assert order is not None
    assert order.status == 'pending'

    # Accept order
    client.post(f'/provider/orders/{order.id}/update/accept')
    db.session.refresh(order)
    assert order.status == 'accepted'

    # Complete order
    client.post(f'/provider/orders/{order.id}/update/complete')
    db.session.refresh(order)
    assert order.status == 'completed'
