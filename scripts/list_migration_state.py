import sqlite3, os, sys
from pathlib import Path
BASE = Path(__file__).resolve().parent.parent
DB = BASE / 'db.sqlite3'
print('DB path:', DB)
if not DB.exists():
    print('No db.sqlite3 found')
    sys.exit(0)
conn = sqlite3.connect(str(DB))
c = conn.cursor()
print('\nApplied migrations (from django_migrations):')
for row in c.execute('select id, app, name, applied from django_migrations order by applied'):
    print(row)

print('\nAvailable migration files per app:')
apps_dir = BASE / 'apps'
for app in sorted([p for p in apps_dir.iterdir() if p.is_dir()]):
    mig_dir = app / 'migrations'
    if mig_dir.exists():
        files = sorted([f.name for f in mig_dir.iterdir() if f.name.endswith('.py')])
        print(f"{app.name}: {files}")
    else:
        print(f"{app.name}: (no migrations dir)")
conn.close()
