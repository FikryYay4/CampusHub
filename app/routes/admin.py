import os
import re
from functools import wraps
from flask import Blueprint, render_template, redirect, url_for, flash, request, abort, current_app, send_from_directory, jsonify
from flask_login import login_required, current_user
from app.extensions import db
from app.models import Admin, Provider, Category, Service, Order
from app.forms import CategoryForm

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


def admin_required(f):
    @wraps(f)
    @login_required
    def decorated(*args, **kwargs):
        if current_user.role != 'admin':
            abort(403)
        return f(*args, **kwargs)
    return decorated


@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    stats = {
        'providers': Provider.query.filter_by(status='aktif').count(),
        'pending_providers': Provider.query.filter_by(status='pending').count(),
        'services': Service.query.count(),
        'orders': Order.query.count(),
    }
    # Category popularity
    cat_stats = db.session.query(
        Category.nama_kategori,
        db.func.count(Service.id)
    ).outerjoin(Service).group_by(Category.id).all()

    # Monthly orders (last 6 months)
    monthly = db.session.query(
        db.func.strftime('%Y-%m', Order.created_at),
        db.func.count(Order.id)
    ).group_by(db.func.strftime('%Y-%m', Order.created_at)).order_by(
        db.func.strftime('%Y-%m', Order.created_at)
    ).limit(6).all()

    # Convert Row objects to plain lists for JSON serialization in template
    cat_stats = [[r[0], r[1]] for r in cat_stats]
    monthly = [[r[0] or 'N/A', r[1]] for r in monthly]

    return render_template('admin/dashboard.html', stats=stats, cat_stats=cat_stats, monthly=monthly)


@admin_bp.route('/providers')
@admin_required
def providers():
    status_filter = request.args.get('status', '')
    query = Provider.query
    if status_filter:
        query = query.filter_by(status=status_filter)
    providers_list = query.order_by(Provider.created_at.desc()).all()
    return render_template('admin/providers.html', providers=providers_list, status_filter=status_filter)


@admin_bp.route('/providers/<int:pid>/approve', methods=['POST'])
@admin_required
def approve_provider(pid):
    p = Provider.query.get_or_404(pid)
    p.status = 'aktif'
    db.session.commit()
    flash(f'Provider {p.nama} disetujui!', 'success')
    return redirect(url_for('admin.providers'))


@admin_bp.route('/providers/<int:pid>/reject', methods=['POST'])
@admin_required
def reject_provider(pid):
    p = Provider.query.get_or_404(pid)
    p.status = 'ditolak'
    db.session.commit()
    flash(f'Provider {p.nama} ditolak.', 'warning')
    return redirect(url_for('admin.providers'))


@admin_bp.route('/ktm/<path:filename>')
@admin_required
def view_ktm(filename):
    upload_dir = os.path.join(current_app.instance_path, 'uploads', 'ktm')
    return send_from_directory(upload_dir, filename)


@admin_bp.route('/categories')
@admin_required
def categories():
    cats = Category.query.order_by(Category.nama_kategori).all()
    form = CategoryForm()
    return render_template('admin/categories.html', categories=cats, form=form)


@admin_bp.route('/categories/add', methods=['POST'])
@admin_required
def add_category():
    form = CategoryForm()
    if form.validate_on_submit():
        nama = form.nama_kategori.data.strip()
        slug = re.sub(r'[^a-z0-9]+', '-', nama.lower()).strip('-')
        if Category.query.filter_by(slug=slug).first():
            flash('Kategori sudah ada.', 'error')
        else:
            db.session.add(Category(nama_kategori=nama, slug=slug))
            db.session.commit()
            flash('Kategori ditambahkan!', 'success')
    return redirect(url_for('admin.categories'))


@admin_bp.route('/categories/<int:cid>/delete', methods=['POST'])
@admin_required
def delete_category(cid):
    cat = Category.query.get_or_404(cid)
    if cat.services:
        flash('Tidak bisa hapus kategori yang masih memiliki layanan.', 'error')
    else:
        db.session.delete(cat)
        db.session.commit()
        flash('Kategori dihapus!', 'success')
    return redirect(url_for('admin.categories'))


@admin_bp.route('/services')
@admin_required
def services():
    svc_list = Service.query.order_by(Service.created_at.desc()).all()
    return render_template('admin/services.html', services=svc_list)


@admin_bp.route('/services/<int:sid>/delete', methods=['POST'])
@admin_required
def delete_service(sid):
    svc = Service.query.get_or_404(sid)
    db.session.delete(svc)
    db.session.commit()
    flash('Layanan dihapus oleh admin!', 'success')
    return redirect(url_for('admin.services'))


@admin_bp.route('/api/stats')
@admin_required
def api_stats():
    """JSON endpoint for dashboard charts."""
    cat_stats = db.session.query(
        Category.nama_kategori,
        db.func.count(Service.id)
    ).outerjoin(Service).group_by(Category.id).all()

    monthly = db.session.query(
        db.func.strftime('%Y-%m', Order.created_at),
        db.func.count(Order.id)
    ).group_by(db.func.strftime('%Y-%m', Order.created_at)).order_by(
        db.func.strftime('%Y-%m', Order.created_at)
    ).limit(12).all()

    return jsonify({
        'categories': [{'name': c[0], 'count': c[1]} for c in cat_stats],
        'monthly': [{'month': m[0] or 'N/A', 'count': m[1]} for m in monthly],
    })
