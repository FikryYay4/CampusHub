from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.extensions import db
from app.models import Admin, Provider
from app.forms import LoginForm, ProviderRegisterForm
from app.storage import upload_ktm

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard' if current_user.role == 'admin' else 'provider.dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        # Check Admin
        admin = Admin.query.filter_by(username=form.username.data).first()
        if admin and admin.check_password(form.password.data):
            login_user(admin)
            return redirect(url_for('admin.dashboard'))

        # Check Provider
        provider = Provider.query.filter_by(email=form.username.data).first()
        if provider and provider.check_password(form.password.data):
            if provider.status != 'aktif':
                flash('Akun belum aktif atau ditolak.', 'error')
                return render_template('auth/login.html', form=form)
            login_user(provider)
            return redirect(url_for('provider.dashboard'))

        flash('Kredensial salah.', 'error')
    return render_template('auth/login.html', form=form)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('public.home'))
    form = ProviderRegisterForm()
    if form.validate_on_submit():
        if Provider.query.filter_by(email=form.email.data).first():
            flash('Email sudah terdaftar.', 'error')
            return render_template('auth/register.html', form=form)

        ktm_path = upload_ktm(form.ktm.data)
        if not ktm_path:
            flash('Gagal upload KTM. Periksa format file (JPG/PNG/PDF).', 'error')
            return render_template('auth/register.html', form=form)

        provider = Provider(
            nama=form.nama.data,
            email=form.email.data,
            no_whatsapp=form.no_whatsapp.data,
            ktm_path=ktm_path,
            status='pending'
        )
        provider.set_password(form.password.data)
        db.session.add(provider)
        db.session.commit()
        flash('Pendaftaran berhasil. Silakan tunggu persetujuan Admin.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('public.home'))
