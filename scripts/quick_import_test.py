from app import app, db
print('Imported app:', app)
with app.app_context():
    db.create_all()
    print('DB create_all OK')
