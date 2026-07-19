from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, TextAreaField, SelectField, IntegerField, HiddenField
from wtforms.validators import DataRequired, Email, Length, NumberRange, Regexp, Optional, EqualTo


class LoginForm(FlaskForm):
    username = StringField('Username / Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


class ProviderRegisterForm(FlaskForm):
    nama = StringField('Nama Lengkap', validators=[DataRequired(), Length(min=3, max=128)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Konfirmasi Password', validators=[DataRequired(), EqualTo('password')])
    no_whatsapp = StringField('No. WhatsApp', validators=[
        DataRequired(),
        Regexp(r'^08\d{8,13}$', message='Format: 08xxxxxxxxxx')
    ])
    ktm = FileField('Upload KTM (opsional)', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'pdf'], 'Format: JPG, PNG, atau PDF'),
        Optional()
    ])


class ServiceForm(FlaskForm):
    judul = StringField('Judul Layanan', validators=[DataRequired(), Length(max=128)])
    category_id = SelectField('Kategori', coerce=int, validators=[DataRequired()])
    harga = IntegerField('Harga (Rp)', validators=[DataRequired(), NumberRange(min=0)])
    deskripsi = TextAreaField('Deskripsi', validators=[DataRequired()])


class OrderForm(FlaskForm):
    nama_pemesan = StringField('Nama', validators=[DataRequired(), Length(max=128)])
    nim = StringField('NIM', validators=[DataRequired(), Length(max=20)])
    kelas = StringField('Kelas', validators=[DataRequired(), Length(max=20)])
    no_whatsapp = StringField('No. WhatsApp', validators=[
        DataRequired(),
        Regexp(r'^08\d{8,13}$', message='Format: 08xxxxxxxxxx')
    ])
    catatan = TextAreaField('Catatan', validators=[Optional()])


class CategoryForm(FlaskForm):
    nama_kategori = StringField('Nama Kategori', validators=[DataRequired(), Length(max=64)])
