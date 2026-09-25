import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-luxedrape-curtain-shop-ultra-luxury-secret-key-2026'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    
    # Strictly Two Applications
    'apps.user_app.apps.UserAppConfig',
    'apps.admin_app.apps.AdminAppConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'curtain_shop.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # Two Apps Context Processors
                'apps.user_app.context_processors.categories_processor',
                'apps.user_app.context_processors.cart_processor',
            ],
        },
    },
]

WSGI_APPLICATION = 'curtain_shop.wsgi.application'

# Database
# On Vercel / AWS Lambda / Serverless environments, the project folder is read-only.
# We copy the seeded db.sqlite3 to the writable /tmp directory so SQLite can read & write freely.
import sys
import shutil

def is_local_writable_env():
    if sys.platform == 'win32' and not os.environ.get('VERCEL') and not os.environ.get('VERCEL_ENV'):
        return True
    test_probe = BASE_DIR / '.write_probe.tmp'
    try:
        test_probe.write_text('probe')
        test_probe.unlink()
        return True
    except Exception:
        return False

if not is_local_writable_env():
    tmp_dir = Path('/tmp')
    tmp_db = tmp_dir / 'db.sqlite3'
    src_db = BASE_DIR / 'db.sqlite3'
    
    try:
        if not tmp_db.exists() or tmp_db.stat().st_size == 0:
            if src_db.exists():
                shutil.copyfile(src_db, tmp_db)
            else:
                tmp_db.touch()
        if tmp_db.exists():
            os.chmod(str(tmp_db), 0o666)
    except Exception as e:
        print("Notice: Error preparing sqlite database in /tmp:", e)
        
    db_path = str(tmp_db) if tmp_db.exists() else str(src_db)
else:
    db_path = BASE_DIR / 'db.sqlite3'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': db_path,
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# Media files (Uploaded images, attachments)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Authentication URLs
LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'core:home'
LOGOUT_REDIRECT_URL = 'core:home'

# Bootstrap Alert message tags mapping
from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.DEBUG: 'secondary',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',
}
