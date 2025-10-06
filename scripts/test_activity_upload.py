from io import BytesIO
from app import app, db, Owner, Activity
import os

with app.app_context():
    db.create_all()
    owner = Owner.query.filter_by(username='test_owner_for_upload').first()
    if not owner:
        owner = Owner(username='test_owner_for_upload', password='x', name='Test Owner')
        db.session.add(owner)
        db.session.commit()
    owner_id = owner.id

    client = app.test_client()
    # set session owner_id
    with client.session_transaction() as sess:
        sess['owner_id'] = owner_id

    fake_png = BytesIO(b"\x89PNG\r\n\x1a\n" + b"0"*100)  # tiny fake png-like content
    data = {
        'activity_name': 'Test Activity',
        'size': 'Small',
        'capacity': '2',
        'price': '10',
        'other_feature1': 'x',
        'image1': (fake_png, 'test.png'),
    }

    resp = client.post('/owner/activities', data=data, content_type='multipart/form-data', follow_redirects=True)
    print('POST status_code:', resp.status_code)

    acts = Activity.query.filter_by(owner_id=owner_id).order_by(Activity.id.desc()).limit(1).all()
    if not acts:
        print('No activity created')
    else:
        a = acts[0]
        print('Created activity id=', a.id, 'name=', a.name)
        print('image1 path in DB:', a.image1)
        if a.image1:
            abs_path = os.path.join(os.path.dirname(__file__), '..', 'static', a.image1).replace('\\','/')
            abs_path = os.path.abspath(abs_path)
            print('Expected file path:', abs_path)
            print('Exists on disk:', os.path.exists(abs_path))
