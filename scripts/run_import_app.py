import importlib.util
import os
import sys
base = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
app_path = os.path.join(base, 'app.py')
print('Loading', app_path)
spec = importlib.util.spec_from_file_location('app', app_path)
app_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app_mod)
app = getattr(app_mod, 'app')
db = getattr(app_mod, 'db')
print('Imported app:', app)
with app.app_context():
    db.create_all()
    print('DB create_all OK')
