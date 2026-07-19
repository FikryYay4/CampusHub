from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.extensions import db
from app.models import Service, Category, Order
from app.forms import OrderForm

public_bp = Blueprint('public', __name__)


@public_bp.route('/')
def home():
    categories = Category.query.all()
    latest_services = Service.query.filter_by(status='active').order_by(Service.created_at.desc()).limit(8).all()
    return render_template('public/home.html', categories=categories, services=latest_services)


@public_bp.route('/services')
def service_list():
    q = request.args.get('q', '').strip()
    cat = request.args.get('category', '')
    query = Service.query.filter_by(status='active')
    if q:
        query = query.filter(Service.judul.ilike(f'%{q}%'))
    if cat:
        query = query.join(Category).filter(Category.slug == cat)
    services = query.order_by(Service.created_at.desc()).all()
    categories = Category.query.all()
    return render_template('public/service_list.html', services=services, categories=categories, q=q, selected_cat=cat)


@public_bp.route('/services/<int:service_id>')
def service_detail(service_id):
    svc = Service.query.get_or_404(service_id)
    form = OrderForm()
    return render_template('public/service_detail.html', service=svc, form=form)


@public_bp.route('/services/<int:service_id>/order', methods=['POST'])
def order_service(service_id):
    svc = Service.query.get_or_404(service_id)
    form = OrderForm()
    if form.validate_on_submit():
        order = Order(
            service_id=svc.id,
            nama_pemesan=form.nama_pemesan.data,
            nim=form.nim.data,
            kelas=form.kelas.data,
            no_whatsapp=form.no_whatsapp.data,
            catatan=form.catatan.data,
        )
        db.session.add(order)
        db.session.commit()
        flash('Pesanan berhasil dikirim! Menunggu konfirmasi provider.', 'success')
        return redirect(url_for('public.order_success', order_id=order.id))
    flash('Data tidak valid, periksa kembali.', 'error')
    return render_template('public/service_detail.html', service=svc, form=form)


@public_bp.route('/order/<int:order_id>/success')
def order_success(order_id):
    order = Order.query.get_or_404(order_id)
    return render_template('public/order_success.html', order=order)
