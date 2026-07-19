from flask import Blueprint, render_template, redirect, url_for, request
from app.extensions import db
from app.models import Category, Service, Order
from app.forms import OrderForm
from app.storage import get_service_image_url

public_bp = Blueprint('public', __name__)


@public_bp.route('/')
def home():
    cats = Category.query.order_by(Category.nama_kategori).all()
    # Latest 6 active services
    svcs = Service.query.filter_by(status='active').order_by(Service.created_at.desc()).limit(6).all()
    # Attach image URLs
    for s in svcs:
        s.image_url = get_service_image_url(s.image_path)
    return render_template('public/home.html', categories=cats, services=svcs)


@public_bp.route('/services')
def service_list():
    q = request.args.get('q', '')
    category_slug = request.args.get('category', '')

    cats = Category.query.order_by(Category.nama_kategori).all()

    query = Service.query.filter_by(status='active')
    if q:
        query = query.filter(Service.judul.ilike(f'%{q}%'))
    if category_slug:
        query = query.join(Category).filter(Category.slug == category_slug)

    svcs = query.order_by(Service.created_at.desc()).all()
    for s in svcs:
        s.image_url = get_service_image_url(s.image_path)

    return render_template('public/service_list.html',
                           services=svcs,
                           categories=cats,
                           q=q,
                           selected_cat=category_slug)


@public_bp.route('/services/<int:service_id>')
def service_detail(service_id):
    svc = Service.query.get_or_404(service_id)
    form = OrderForm()
    svc.image_url = get_service_image_url(svc.image_path)
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
            status='pending'
        )
        db.session.add(order)
        db.session.commit()
        return render_template('public/order_success.html', order=order)
    svc.image_url = get_service_image_url(svc.image_path)
    return render_template('public/service_detail.html', service=svc, form=form), 400
