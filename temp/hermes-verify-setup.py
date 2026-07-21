import os, sys
from app import create_app
app = create_app()
upload_dir = app.config.get('UPLOAD_FOLDER')
if not upload_dir:
    print('UPLOAD_FOLDER not set')
    sys.exit(1)
if not os.path.isdir(upload_dir):
    print(f'Upload folder does not exist: {upload_dir}')
    sys.exit(1)
print('Verification passed: upload folder exists at', upload_dir)
