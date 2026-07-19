import os
import re
from functools import wraps
from flask import Blueprint, render_template, redirect, url_for, flash, request, abort, current_app, send_from_directory, jsonify
from flask_login import login_required, current_user
from app.extensions import db
from app.models import Admin, Provider, Category, Service, Order
from app.forms import CategoryForm
from app.storage import get_ktm_url

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

    # Category statistics (Category name vs Service count)
    cats = Category.query.all()
    cat_stats = []
    for c in cats:
        service_count = Service.query.filter_by(category_id=c.id).count()
        cat_stats.append([c.nama_kategori, service_count])

    # Monthly orders (grouping in Python to be DB-agnostic: SQLite & PostgreSQL compatible)
    orders_all = Order.query.order_by(Order.created_at.asc()).all()
    monthly_dict = {}
    for o in orders_all:
        month_str = o.created_at.strftime('%Y-%m')
        monthly_dict[month_str] = monthly_dict.get(month_str, 0) + 1

    # Take last 6 months
    sorted_months = sorted(monthly_dict.keys())[-6:]
    monthly = [[m, monthly_dict[m]] for m in sorted_months]
    if not monthly:
        monthly = [['No Data', 0]]

    return render_template('admin/dashboard.html', stats=stats, cat_stats=cat_stats, monthly=monthly)


@admin_bp.route('/providers')
@admin_required
def providers():
    status_filter = request.args.get('status', '')
    query = Provider.query
    if status_filter:
        query = query.filter_by(status=status_filter)
    providers_list = query.order_by(Provider.created_at.desc()).all()

    # Generate KTM signed URLs
    for p in providers_list:
        p.ktm_url = get_ktm_url(p.ktm_path)

    return render_template('admin/providers.html', providers=providers_list, status_filter=status_filter)


@admin_bp.route('/providers/<int:pid>/approve', methods=['POST'])
@admin_required
def approve_provider(pid):
    p = Provider.query.get_or_404(pid)
    p.status = 'aktif'
    db.session.commit()
    return redirect(url_for('admin.providers'))


@admin_bp.route('/providers/<int:pid>/reject', methods=['POST'])
@admin_required
def reject_provider(pid):
    p = Provider.query.get_or_404(pid)
    p.status = 'ditolak'
    db.session.commit()
    return redirect(url_for('admin.providers'))


@admin_bp.route('/ktm/<path:filename>')
@admin_required
def view_ktm(filename):
    # Route to serve KTM locally if Supabase not configured
    upload_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], 'ktm')
    return send_from_directory(upload_dir, filename)


@admin_bp.route('/categories', methods=['GET', 'POST'])
@admin_required
def categories():
    cats = Category.query.order_by(Category.nama_kategori).all()
    form = CategoryForm()
    if request.method == 'POST' and form.validate_on_submit():
        nama = form.nama_kategori.data.strip()
        slug = re.sub(r'[^a-z0-9]+', '-', nama.lower()).strip('-')
        if Category.query.filter_by(slug=slug).first():
            pass
        else:
            db.session.add(Category(nama_kategori=nama, slug=slug))
            db.session.commit()
        return redirect(url_for('admin.categories'))
    return render_template('admin/categories.html', categories=cats, form=form)


@admin_bp.route('/categories/<int:cid>/delete', methods=['POST'])
@admin_required
def delete_category(cid):
    cat = Category.query.get_or_404(cid)
    # Re-assign or protect services in category
    # For simplicity, we just delete the category (cascade might not be configured, so let's delete manually or set category_id)
    # Check if category has services
    has_services = Service.query.filter_by(category_id=cid).first()
    if has_services:
        flash('Kategori sedang digunakan oleh layanan.', 'error')
    else:
        db.session.delete(cat)
        db.session.commit()
        flash('Message deleted!', 'success')
    return redirect(url_for('admin.categories'))


@admin_bp.route('/services')
@admin_required
def services():
    svcs = Service.query.order_by(Service.created_at.desc()).all()
    return render_template('admin/services.html', services=svcs)


@admin_bp.route('/services/<int:sid>/approve', methods=['POST'])
@admin_required
def approve_service(sid):
    svc = Service.query.get_or_404(sid)
    svc.status = 'active'
    db.session.commit()
    return redirect(url_for('admin.services'))


@admin_bp.route('/services/<int:sid>/reject', methods=['POST'])
@admin_required
def reject_service(sid):
    svc = Service.query.get_or_404(sid)
    svc.status = 'rejected'
    db.session.commit()
    return redirect(url_for('admin.services'))


@admin_bp.route('/services/<int:sid>/delete', methods=['POST'])
@admin_required
def delete_service(sid):
    svc = Service.query.get_or_404(sid)
    db.session.delete(svc)
    db.session.commit()
    # Flash "Message deleted!" exactly as requested
    flash('Message deleted!', 'success')
    return redirect(url_for('admin.services'))
