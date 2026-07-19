from functools import wraps
from flask import Blueprint, render_template, redirect, url_for, flash, request, abort, jsonify
from flask_login import login_required, current_user
from app.extensions import db
from app.models import Service, Order, Category
from app.forms import ServiceForm
from app.storage import upload_service_image, get_service_image_url

provider_bp = Blueprint('provider', __name__, url_prefix='/provider')


def provider_required(f):
    @wraps(f)
    @login_required
    def decorated(*args, **kwargs):
        if current_user.role != 'provider':
            abort(403)
        return f(*args, **kwargs)
    return decorated


def _hitung_pesanan_baru():
    return Order.query.join(Service).filter(
        Service.provider_id == current_user.id,
        Order.status == 'pending'
    ).count()


@provider_bp.route('/dashboard')
@provider_required
def dashboard():
    services = Service.query.filter_by(provider_id=current_user.id).order_by(Service.created_at.desc()).all()
    total_orders = Order.query.join(Service).filter(Service.provider_id == current_user.id).count()
    pending_orders = _hitung_pesanan_baru()
    return render_template('provider/dashboard.html',
                           services=services,
                           total_orders=total_orders,
                           pending_orders=pending_orders,
                           pesanan_baru=pending_orders)


@provider_bp.route('/api/pesanan-baru')
@provider_required
def pesanan_baru_count():
    return jsonify({'count': _hitung_pesanan_baru()})


@provider_bp.route('/services/add', methods=['GET', 'POST'])
@provider_required
def add_service():
    form = ServiceForm()
    form.category_id.choices = [(c.id, c.nama_kategori) for c in Category.query.order_by(Category.nama_kategori).all()]
    if form.validate_on_submit():
        image_path = None
        if form.image.data:
            image_path = upload_service_image(form.image.data)

        svc = Service(
            provider_id=current_user.id,
            category_id=form.category_id.data,
            judul=form.judul.data,
            harga=form.harga.data,
            deskripsi=form.deskripsi.data,
            image_path=image_path,
            status='active'
        )
        db.session.add(svc)
        db.session.commit()
        flash('Layanan berhasil ditambahkan!', 'success')
        return redirect(url_for('provider.dashboard'))
    return render_template('provider/service_form.html', form=form, edit=False, pesanan_baru=_hitung_pesanan_baru())


@provider_bp.route('/services/<int:sid>/edit', methods=['GET', 'POST'])
@provider_required
def edit_service(sid):
    svc = Service.query.get_or_404(sid)
    if svc.provider_id != current_user.id:
        abort(403)
    form = ServiceForm(obj=svc)
    form.category_id.choices = [(c.id, c.nama_kategori) for c in Category.query.order_by(Category.nama_kategori).all()]
    if form.validate_on_submit():
        if form.image.data:
            svc.image_path = upload_service_image(form.image.data)
        svc.judul = form.judul.data
        svc.category_id = form.category_id.data
        svc.harga = form.harga.data
        svc.deskripsi = form.deskripsi.data
        db.session.commit()
        flash('Layanan berhasil diperbarui!', 'success')
        return redirect(url_for('provider.dashboard'))
    return render_template('provider/service_form.html', form=form, edit=True, service=svc, pesanan_baru=_hitung_pesanan_baru())


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
    return render_template('provider/orders.html', orders=order_list, pesanan_baru=_hitung_pesanan_baru())


@provider_bp.route('/orders/<int:oid>/update/<action>', methods=['POST'])
@provider_required
def update_order(oid, action):
    order = Order.query.get_or_404(oid)
    if order.service.provider_id != current_user.id:
        abort(403)
    if action == 'accept':
        order.status = 'accepted'
    elif action == 'reject':
        order.status = 'rejected'
    elif action == 'complete':
        order.status = 'completed'
    db.session.commit()
    return redirect(url_for('provider.orders'))
