import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-change-me')

    # Database — Supabase PostgreSQL pooler (port 6543) for app,
    # direct (port 5432) for migrations only
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'sqlite:///' + os.path.join(os.path.dirname(basedir), 'instance', 'campushub.db')
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Serverless-friendly pool settings (Vercel)
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
    }

    # Upload limit 2 MB
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024

    # Supabase Storage
    SUPABASE_URL = os.environ.get('SUPABASE_URL', '')
    SUPABASE_KEY = os.environ.get('SUPABASE_KEY', '')

    # Local upload fallback (when Supabase not configured)
    UPLOAD_FOLDER = os.path.join(os.path.dirname(basedir), 'instance', 'uploads')
