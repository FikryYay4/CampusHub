"""
Supabase Storage helper for KTM (private bucket) and service images (public bucket).
Falls back to local filesystem when Supabase is not configured.
"""
import os
import uuid
from flask import current_app

# Lazy-init Supabase client
_supabase = None

KTM_BUCKET = 'ktm-provider'           # private
SERVICE_IMG_BUCKET = 'service-images'  # public

ALLOWED_KTM_EXT = {'jpg', 'jpeg', 'png', 'pdf'}
ALLOWED_IMG_EXT = {'jpg', 'jpeg', 'png', 'webp'}


def _get_supabase():
    global _supabase
    if _supabase is not None:
        return _supabase
    url = current_app.config.get('SUPABASE_URL', '')
    key = current_app.config.get('SUPABASE_KEY', '')
    
    # If in Vercel/production or Supabase variables are partially set, enforce Supabase
    is_production = os.environ.get('VERCEL') or current_app.config.get('ENV') == 'production'
    if is_production and not (url and key):
        # Supabase not configured; fall through to local storage
        return None
    if url and key:
        from supabase import create_client
        _supabase = create_client(url, key)
        return _supabase
    return None


def _unique_name(filename, allowed):
    if not filename or '.' not in filename:
        return None
    ext = filename.rsplit('.', 1)[-1].lower()
    return f'{uuid.uuid4().hex}.{ext}' if ext in allowed else None


def _local_upload(file_storage, subfolder, allowed):
    """Save file locally when Supabase not available."""
    name = _unique_name(file_storage.filename, allowed)
    if not name:
        return None
    upload_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], subfolder)
    os.makedirs(upload_dir, exist_ok=True)
    file_storage.save(os.path.join(upload_dir, name))
    return name


# --- KTM (private) ---

def upload_ktm(file_storage):
    """Upload KTM. Returns path string or None if format rejected."""
    sb = _get_supabase()
    if sb:
        name = _unique_name(file_storage.filename, ALLOWED_KTM_EXT)
        if not name:
            return None
        sb.storage.from_(KTM_BUCKET).upload(
            name, file_storage.read(), {'content-type': file_storage.mimetype}
        )
        return name
    return _local_upload(file_storage, 'ktm', ALLOWED_KTM_EXT)


def get_ktm_url(ktm_path, expires_in=300):
    """Signed URL (5 min default). Only call from admin-protected routes."""
    if not ktm_path:
        return None
    sb = _get_supabase()
    if sb:
        result = sb.storage.from_(KTM_BUCKET).create_signed_url(ktm_path, expires_in)
        return result.get('signedURL') or result.get('signedUrl')
    # Local fallback
    from flask import url_for
    return url_for('admin.view_ktm', filename=ktm_path)


# --- Service images (public) ---

def upload_service_image(file_storage):
    """Upload service image. Returns path string or None."""
    sb = _get_supabase()
    if sb:
        name = _unique_name(file_storage.filename, ALLOWED_IMG_EXT)
        if not name:
            return None
        sb.storage.from_(SERVICE_IMG_BUCKET).upload(
            name, file_storage.read(), {'content-type': file_storage.mimetype}
        )
        return name
    return _local_upload(file_storage, 'services', ALLOWED_IMG_EXT)


def get_service_image_url(image_path):
    """Public URL for service image."""
    if not image_path:
        return None
    sb = _get_supabase()
    if sb:
        return sb.storage.from_(SERVICE_IMG_BUCKET).get_public_url(image_path)
    # Local fallback
    from flask import url_for
    return url_for('static_uploads', filename=f'services/{image_path}')
