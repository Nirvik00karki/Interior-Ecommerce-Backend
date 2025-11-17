import importlib, os, sys
from pathlib import Path

# Ensure project root is on sys.path (same approach manage.py uses)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

os.environ.setdefault('DJANGO_SETTINGS_MODULE','interior_backend.settings')
settings = importlib.import_module('interior_backend.settings')
print('DATABASES in settings.py ->', settings.DATABASES)
print('ENGINE value ->', settings.DATABASES.get('default', {}).get('ENGINE'))
print('BASE_DIR ->', getattr(settings, 'BASE_DIR', None))
print('DJANGO_SETTINGS_MODULE ->', os.environ.get('DJANGO_SETTINGS_MODULE'))
