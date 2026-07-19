import os
import uuid
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from app.extensions import db
from app.models import Admin, Provider
from app.forms import LoginForm, ProviderRegisterForm

auth_bp = Blueprint('auth', __name__)

ALLOWED_EXT = {'jpg', 'jpeg', 'png', 'pdf'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXT


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for(_dashboard_for(current_user)))
    form = LoginForm()
    if form.validate_on_submit():
        # Try admin first
        admin = Admin.query.filter_by(username=form.username.data).first()
        if admin and admin.check_password(form.password.data):
            login_user(admin)
            flash('Login berhasil!', 'success')
            return redirect(url_for('admin.dashboard'))
        # Try provider
        provider = Provider.query.filter_by(email=form.username.data).first()
        if provider and provider.check_password(form.password.data):
            if provider.status != 'aktif':
                flash('Akun belum diverifikasi atau ditolak oleh admin.', 'error')
                return render_template('auth/login.html', form=form)
            login_user(provider)
            flash('Login berhasil!', 'success')
            return redirect(url_for('provider.dashboard'))
        flash('Username/email atau password salah.', 'error')
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

        ktm_filename = None
        file = form.ktm.data
        if file and hasattr(file, 'filename') and file.filename:
            if not allowed_file(file.filename):
                flash('Format KTM harus JPG, PNG, atau PDF.', 'error')
                return render_template('auth/register.html', form=form)
            ext = secure_filename(file.filename).rsplit('.', 1)[1]
            ktm_filename = f"{uuid.uuid4().hex}.{ext}"
            upload_dir = os.path.join(current_app.instance_path, 'uploads', 'ktm')
            os.makedirs(upload_dir, exist_ok=True)
            file.save(os.path.join(upload_dir, ktm_filename))

        provider = Provider(
            nama=form.nama.data,
            email=form.email.data,
            no_whatsapp=form.no_whatsapp.data,
            ktm_filename=ktm_filename,
        )
        provider.set_password(form.password.data)
        db.session.add(provider)
        db.session.commit()
        flash('Registrasi berhasil! Tunggu verifikasi admin.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Berhasil logout.', 'success')
    return redirect(url_for('public.home'))


def _dashboard_for(user):
    if user.role == 'admin':
        return 'admin.dashboard'
    return 'provider.dashboard'
