from functools import wraps
from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app.extensions import db
from app.models import Service, Order, Category
from app.forms import ServiceForm

provider_bp = Blueprint('provider', __name__, url_prefix='/provider')


def provider_required(f):
    @wraps(f)
    @login_required
    def decorated(*args, **kwargs):
        if current_user.role != 'provider':
            abort(403)
        return f(*args, **kwargs)
    return decorated


@provider_bp.route('/dashboard')
@provider_required
def dashboard():
    services = Service.query.filter_by(provider_id=current_user.id).all()
    total_orders = Order.query.join(Service).filter(Service.provider_id == current_user.id).count()
    pending_orders = Order.query.join(Service).filter(
        Service.provider_id == current_user.id, Order.status == 'pending'
    ).count()
    return render_template('provider/dashboard.html',
                           services=services, total_orders=total_orders, pending_orders=pending_orders)


@provider_bp.route('/services/add', methods=['GET', 'POST'])
@provider_required
def add_service():
    form = ServiceForm()
    form.category_id.choices = [(c.id, c.nama_kategori) for c in Category.query.order_by(Category.nama_kategori).all()]
    if form.validate_on_submit():
        svc = Service(
            provider_id=current_user.id,
            category_id=form.category_id.data,
            judul=form.judul.data,
            harga=form.harga.data,
            deskripsi=form.deskripsi.data,
        )
        db.session.add(svc)
        db.session.commit()
        flash('Layanan berhasil ditambahkan!', 'success')
        return redirect(url_for('provider.dashboard'))
    return render_template('provider/service_form.html', form=form, edit=False)


@provider_bp.route('/services/<int:sid>/edit', methods=['GET', 'POST'])
@provider_required
def edit_service(sid):
    svc = Service.query.get_or_404(sid)
    if svc.provider_id != current_user.id:
        abort(403)
    form = ServiceForm(obj=svc)
    form.category_id.choices = [(c.id, c.nama_kategori) for c in Category.query.order_by(Category.nama_kategori).all()]
    if form.validate_on_submit():
        svc.judul = form.judul.data
        svc.category_id = form.category_id.data
        svc.harga = form.harga.data
        svc.deskripsi = form.deskripsi.data
        db.session.commit()
        flash('Layanan berhasil diperbarui!', 'success')
        return redirect(url_for('provider.dashboard'))
    return render_template('provider/service_form.html', form=form, edit=True, service=svc)


@provider_bp.route('/services/<int:sid>/delete', methods=['POST'])
@provider_required
def delete_service(sid):
    svc = Service.query.get_or_404(sid)
    if svc.provider_id != current_user.id:
        abort(403)
    db.session.delete(svc)
    db.session.commit()
    flash('Layanan berhasil dihapus!', 'success')
    return redirect(url_for('provider.dashboard'))


@provider_bp.route('/orders')
@provider_required
def orders():
    order_list = Order.query.join(Service).filter(
        Service.provider_id == current_user.id
    ).order_by(Order.created_at.desc()).all()
    return render_template('provider/orders.html', orders=order_list)


@provider_bp.route('/orders/<int:oid>/<action>', methods=['POST'])
@provider_required
def update_order(oid, action):
    order = Order.query.get_or_404(oid)
    if order.service.provider_id != current_user.id:
        abort(403)
    valid_transitions = {
        'accept': ('pending', 'accepted'),
        'reject': ('pending', 'rejected'),
        'complete': ('accepted', 'completed'),
    }
    if action not in valid_transitions:
        abort(400)
    expected_from, new_status = valid_transitions[action]
    if order.status != expected_from:
        flash(f'Pesanan tidak bisa di-{action} dari status {order.status}.', 'error')
        return redirect(url_for('provider.orders'))
    order.status = new_status
    db.session.commit()
    flash(f'Pesanan berhasil di-{action}!', 'success')
    return redirect(url_for('provider.orders'))
