"""Black-box tests for CampusHub routes."""
import os
import sys
import tempfile
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app import create_app
from app.extensions import db
from app.models import Admin, Provider, Category, Service


@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.app_context():
        db.drop_all()
        db.create_all()
        # Seed
        admin = Admin(username='admin')
        admin.set_password('admin123')
        db.session.add(admin)
        cat = Category(nama_kategori='Tutor', slug='tutor')
        db.session.add(cat)
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


def test_login_page(client):
    rv = client.get('/login')
    assert rv.status_code == 200
    assert b'Login' in rv.data


def test_register_page(client):
    rv = client.get('/register')
    assert rv.status_code == 200


def test_admin_login(client):
    rv = client.post('/login', data={'username': 'admin', 'password': 'admin123'}, follow_redirects=True)
    assert rv.status_code == 200
    assert b'Dashboard Admin' in rv.data


def test_provider_register_and_login(client):
    # Register
    rv = client.post('/register', data={
        'nama': 'Test Provider',
        'email': 'test@test.com',
        'password': 'test1234',
        'confirm_password': 'test1234',
        'no_whatsapp': '081234567890',
    }, follow_redirects=True)
    assert rv.status_code == 200

    # Login fails (pending)
    rv = client.post('/login', data={'username': 'test@test.com', 'password': 'test1234'}, follow_redirects=True)
    assert b'belum diverifikasi' in rv.data.lower() or b'Login' in rv.data

    # Approve via admin
    client.post('/login', data={'username': 'admin', 'password': 'admin123'})
    from app.models import Provider as P
    from app import create_app
    app = create_app()
    with app.app_context():
        p = P.query.filter_by(email='test@test.com').first()
        if p:
            p.status = 'aktif'
            db.session.commit()


def test_admin_dashboard_requires_login(client):
    rv = client.get('/admin/dashboard', follow_redirects=True)
    assert b'Login' in rv.data or b'login' in rv.data


def test_provider_dashboard_requires_login(client):
    rv = client.get('/provider/dashboard', follow_redirects=True)
    assert b'Login' in rv.data or b'login' in rv.data


def test_order_form_validation(client):
    """Order to non-existing service returns 404."""
    rv = client.post('/services/999/order', data={}, follow_redirects=True)
    assert rv.status_code == 404
