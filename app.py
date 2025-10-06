from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import uuid
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
# base directory for paths used by the app
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# ensure instance folder exists (so the sqlite file can be created there)
INSTANCE_DIR = os.path.join(BASE_DIR, 'instance')
os.makedirs(INSTANCE_DIR, exist_ok=True)
# SQLAlchemy DB (store under instance/ to match view_db.py)
# Use absolute path so SQLAlchemy can open the file regardless of CWD
DB_FILE = os.path.join(INSTANCE_DIR, 'site.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_FILE.replace('\\','/')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# file upload settings
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(120))
    email = db.Column(db.String(120))
    birthdate = db.Column(db.String(50))
    gender = db.Column(db.String(20))
    address = db.Column(db.String(200))
    age = db.Column(db.String(10))
    contact_number = db.Column(db.String(30))
    facebook = db.Column(db.String(120))
    emergency_name = db.Column(db.String(120))
    emergency_number = db.Column(db.String(30))
    relationship = db.Column(db.String(50))
    avatar = db.Column(db.String(300))
    # Add other fields as needed

class Owner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(120))
    email = db.Column(db.String(120))
    birthdate = db.Column(db.String(50))
    gender = db.Column(db.String(20))
    address = db.Column(db.String(200))
    resort_address = db.Column(db.String(200))
    age = db.Column(db.String(10))
    contact_number = db.Column(db.String(30))
    facebook = db.Column(db.String(120))
    resort_name = db.Column(db.String(200))
    business_id = db.Column(db.String(120))
    tax_id = db.Column(db.String(120))
    bank_account = db.Column(db.String(120))
    gcash = db.Column(db.String(120))
    paymaya = db.Column(db.String(120))
    paypal = db.Column(db.String(120))
    avatar = db.Column(db.String(300))
    # Add other fields as needed


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(120))
    email = db.Column(db.String(120))
    # add more admin-specific fields if needed


class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('owner.id'), nullable=True)
    name = db.Column(db.String(200), nullable=False)
    price = db.Column(db.String(50))
    capacity = db.Column(db.String(20))
    other_feature2 = db.Column(db.String(200))
    other_feature3 = db.Column(db.String(200))
    other_feature5 = db.Column(db.String(200))
    image1 = db.Column(db.String(300))
    image2 = db.Column(db.String(300))
    image3 = db.Column(db.String(300))
    image4 = db.Column(db.String(300))
    image5 = db.Column(db.String(300))

    owner = db.relationship('Owner', backref=db.backref('rooms', lazy=True))


class Cottage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('owner.id'), nullable=True)
    name = db.Column(db.String(200), nullable=False)
    price = db.Column(db.String(50))
    capacity = db.Column(db.String(20))
    beds = db.Column(db.String(20))
    other_feature2 = db.Column(db.String(200))
    other_feature3 = db.Column(db.String(200))
    other_feature5 = db.Column(db.String(200))
    image1 = db.Column(db.String(300))
    image2 = db.Column(db.String(300))
    image3 = db.Column(db.String(300))
    image4 = db.Column(db.String(300))
    image5 = db.Column(db.String(300))

    owner = db.relationship('Owner', backref=db.backref('cottages', lazy=True))


class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('owner.id'), nullable=True)
    name = db.Column(db.String(200), nullable=False)
    size = db.Column(db.String(100))
    capacity = db.Column(db.String(50))
    price = db.Column(db.String(50))
    other_feature1 = db.Column(db.String(200))
    other_feature2 = db.Column(db.String(200))
    other_feature3 = db.Column(db.String(200))
    other_feature4 = db.Column(db.String(200))
    image1 = db.Column(db.String(300))
    image2 = db.Column(db.String(300))
    image3 = db.Column(db.String(300))
    image4 = db.Column(db.String(300))
    image5 = db.Column(db.String(300))

    owner = db.relationship('Owner', backref=db.backref('foods', lazy=True))


class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('owner.id'), nullable=True)
    name = db.Column(db.String(200), nullable=False)
    size = db.Column(db.String(100))
    capacity = db.Column(db.String(50))
    price = db.Column(db.String(50))
    other_feature1 = db.Column(db.String(200))
    other_feature2 = db.Column(db.String(200))
    other_feature3 = db.Column(db.String(200))
    other_feature4 = db.Column(db.String(200))
    image1 = db.Column(db.String(300))
    image2 = db.Column(db.String(300))
    image3 = db.Column(db.String(300))
    image4 = db.Column(db.String(300))
    image5 = db.Column(db.String(300))

    owner = db.relationship('Owner', backref=db.backref('activities', lazy=True))


class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('owner.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('conversations', lazy=True))
    owner = db.relationship('Owner', backref=db.backref('conversations', lazy=True))


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversation.id'), nullable=False)
    sender = db.Column(db.String(10), nullable=False)  # 'user' or 'owner'
    sender_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    sender_owner_id = db.Column(db.Integer, db.ForeignKey('owner.id'), nullable=True)
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    conversation = db.relationship('Conversation', backref=db.backref('messages', lazy=True, order_by='Message.created_at'))
    sender_user = db.relationship('User', foreign_keys=[sender_user_id])
    sender_owner = db.relationship('Owner', foreign_keys=[sender_owner_id])


class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('owner.id'), nullable=False)
    resource_type = db.Column(db.String(30), nullable=False)  # 'room' or 'cottage'
    resource_id = db.Column(db.Integer, nullable=False)
    check_in = db.Column(db.Date)
    check_out = db.Column(db.Date)
    guests = db.Column(db.String(50))
    status = db.Column(db.String(30), default='pending')  # pending, confirmed, cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('reservations', lazy=True))
    owner = db.relationship('Owner', backref=db.backref('reservations', lazy=True))


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def _delete_static_file(rel_path):
    """Delete a file stored under the static folder given a relative path like 'uploads/xxx.jpg'."""
    if not rel_path:
        return
    # prevent directory traversal
    rel_path = rel_path.replace('..', '')
    abs_path = os.path.join(BASE_DIR, 'static', rel_path)
    try:
        if os.path.exists(abs_path) and os.path.isfile(abs_path):
            os.remove(abs_path)
    except Exception:
        # don't raise; best-effort cleanup
        pass

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/browse")
def browse():
    owners = Owner.query.all()
    return render_template("browse.html", owners=owners)

@app.route("/user/profile")
def user_profile():
    user_data = None
    if "user_id" in session:
        user_data = {
            "username": session.get("username"),
            "name": session.get("name"),
            "email": session.get("email"),
            "birthdate": session.get("birthdate"),
            "gender": session.get("gender"),
            "address": session.get("address"),
            "age": session.get("age"),
            "contact_number": session.get("contact_number"),
            "facebook": session.get("facebook"),
            "emergency_name": session.get("emergency_name"),
            "emergency_number": session.get("emergency_number"),
            "relationship": session.get("relationship"),
            "avatar": session.get("avatar"),
        }
    return render_template("user/profile.html", user=user_data)

@app.route("/user/bookings")
def user_bookings():
    # fetch reservations for logged-in user
    if 'user_id' not in session:
        flash('You must be logged in to view your bookings.', 'danger')
        return redirect(url_for('home'))
    resvs = Reservation.query.filter_by(user_id=session['user_id']).order_by(Reservation.created_at.desc()).all()
    bookings = []
    for r in resvs:
        title = ''
        img = None
        if r.resource_type == 'room':
            room = Room.query.get(r.resource_id)
            if room:
                title = f"{room.name}"
                img = room.image1 or room.image2 or room.image3
        elif r.resource_type == 'cottage':
            c = Cottage.query.get(r.resource_id)
            if c:
                title = f"{c.name}"
                img = c.image1 or c.image2 or c.image3
        bookings.append({
            'id': r.id,
            'resource_type': r.resource_type,
            'title': title,
            'img': img,
            'guests': r.guests,
            'check_in': r.check_in.isoformat() if r.check_in else None,
            'check_out': r.check_out.isoformat() if r.check_out else None,
            'status': r.status,
            'owner_id': r.owner_id,
            'resource_id': r.resource_id,
        })
    return render_template('user/bookings.html', bookings=bookings)

@app.route('/user/chats')
def user_chats():
    # Render the user chats page. In the future attach the user's chat list.
    if 'user_id' not in session:
        return redirect(url_for('home'))
    # load conversations where this user participates
    convs = Conversation.query.filter_by(user_id=session['user_id']).order_by(Conversation.created_at.desc()).all()
    conversations = []
    for c in convs:
        last_msg = None
        if c.messages:
            last_msg = c.messages[-1]
        conversations.append({
            'id': c.id,
            'owner_id': c.owner.id if c.owner else None,
            'partner_name': c.owner.name if c.owner else 'Owner',
            'partner_avatar': c.owner.avatar if c.owner else None,
            'last_text': last_msg.text if last_msg else None,
            'last_time': last_msg.created_at.isoformat() if last_msg else None
        })
    return render_template('user/chats.html', conversations=conversations)


@app.route('/owner/chats')
def owner_chats():
    # Render the owner chats page (owner must be logged in)
    if 'owner_id' not in session:
        return redirect(url_for('home'))
    convs = Conversation.query.filter_by(owner_id=session['owner_id']).order_by(Conversation.created_at.desc()).all()
    conversations = []
    for c in convs:
        last_msg = None
        if c.messages:
            last_msg = c.messages[-1]
        conversations.append({
            'id': c.id,
            'user_id': c.user.id if c.user else None,
            'partner_name': c.user.name if c.user else 'User',
            'partner_avatar': c.user.avatar if c.user else None,
            'last_text': last_msg.text if last_msg else None,
            'last_time': last_msg.created_at.isoformat() if last_msg else None
        })
    return render_template('owner/chats.html', conversations=conversations)


@app.route("/owner/profile")
def owner_profile():
    owner_data = None
    if "owner_id" in session:
        owner_data = {
            "username": session.get("owner_username"),
            "name": session.get("owner_name"),
            "email": session.get("owner_email"),
            "birthdate": session.get("owner_birthdate"),
            "gender": session.get("owner_gender"),
            "address": session.get("owner_address"),
            "resort_address": session.get("owner_resort_address"),
            "age": session.get("owner_age"),
            "contact_number": session.get("owner_contact_number"),
            "facebook": session.get("owner_facebook"),
            "resort_name": session.get("owner_resort_name"),
            "business_id": session.get("owner_business_id"),
            "tax_id": session.get("owner_tax_id"),
            "bank_account": session.get("owner_bank_account"),
            "gcash": session.get("owner_gcash"),
            "paymaya": session.get("owner_paymaya"),
            "paypal": session.get("owner_paypal"),
            # owner may not have emergency/contact relationship fields used by the user template;
            # those will be None if not set.
            "emergency_name": session.get("emergency_name"),
            "emergency_number": session.get("emergency_number"),
            "relationship": session.get("relationship"),
            "avatar": session.get("owner_avatar"),
        }
    return render_template("owner/profile.html", user=owner_data)

@app.route("/owner/dashboard")
def owner_dashboard():
    # Build owner context from session / DB so the template always has `owner`
    owner = None
    current_count = 0
    upcoming_count = 0
    pending_count = 0
    current_guests = []

    if "owner_id" in session:
        owner_obj = Owner.query.get(session["owner_id"])
        if owner_obj:
            owner = {
                "resort_name": owner_obj.resort_name,
                "resort_address": owner_obj.resort_address,
                "name": owner_obj.name,
                "contact_number": owner_obj.contact_number,
                # optional fields (if you add them to Owner model)
                "cover_photo": getattr(owner_obj, "cover_photo", None),
                "avatar": getattr(owner_obj, "avatar", None),
            }

    # TODO: replace with real queries once you add Reservation/Booking models.
    # For now, pass defaults so template renders without errors.
    return render_template(
        "owner/dashboard.html",
        owner=owner,
        current_count=current_count,
        upcoming_count=upcoming_count,
        pending_count=pending_count,
        current_guests=current_guests,
    )

@app.route("/owner/reservations")
def owner_reservations():
    # owner must be logged in
    if 'owner_id' not in session:
        flash('You must be logged in as owner to view reservations.', 'danger')
        return redirect(url_for('home'))
    resvs = Reservation.query.filter_by(owner_id=session['owner_id']).order_by(Reservation.created_at.desc()).all()
    reservations = []
    for r in resvs:
        user = User.query.get(r.user_id)
        title = ''
        if r.resource_type == 'room':
            room = Room.query.get(r.resource_id)
            title = room.name if room else 'Room'
        else:
            c = Cottage.query.get(r.resource_id)
            title = c.name if c else 'Cottage'
        reservations.append({
            'id': r.id,
            'user_name': user.name if user else 'Customer',
            'user_id': r.user_id,
            'title': title,
            'check_in': r.check_in.isoformat() if r.check_in else None,
            'check_out': r.check_out.isoformat() if r.check_out else None,
            'guests': r.guests,
            'status': r.status,
        })
    return render_template("owner/reservations.html", reservations=reservations)

@app.route("/owner/rooms", methods=["GET","POST"]) 
def owner_rooms():
    # Support GET: list rooms for current owner (if logged in) or all rooms
    if request.method == 'POST':
        # handle room creation with up to 5 images
        if 'owner_id' not in session:
            flash('You must be logged in as owner to add rooms.', 'danger')
            return redirect(url_for('owner_rooms'))
        owner_id = session['owner_id']
        room_name = request.form.get('room_name') or 'Untitled Room'
        price = request.form.get('price')
        capacity = request.form.get('capacity')
        beds = request.form.get('beds')
        other_feature2 = request.form.get('other_feature2')
        other_feature3 = request.form.get('other_feature3')
        other_feature5 = request.form.get('other_feature5')

        # prepare filenames
        filenames = [None] * 5
        for i in range(1,6):
            file = request.files.get(f'image{i}')
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # ensure unique filename using uuid4
                name, ext = os.path.splitext(filename)
                uniq = f"{name}_{owner_id}_{uuid.uuid4().hex}_{i}{ext}"
                save_path = os.path.join(app.config['UPLOAD_FOLDER'], uniq)
                file.save(save_path)
                # store path relative to static for use in templates
                filenames[i-1] = os.path.join('uploads', uniq).replace('\\','/')

        room = Room(
            owner_id=owner_id,
            name=room_name,
            price=price,
            capacity=capacity,
            # beds removed for cottages
            other_feature2=other_feature2,
            other_feature3=other_feature3,
            other_feature5=other_feature5,
            image1=filenames[0],
            image2=filenames[1],
            image3=filenames[2],
            image4=filenames[3],
            image5=filenames[4]
        )
        db.session.add(room)
        db.session.commit()
        flash('Room added successfully.', 'success')
        return redirect(url_for('owner_rooms'))

    # GET
    rooms = []
    if 'owner_id' in session:
        rooms = Room.query.filter_by(owner_id=session['owner_id']).all()
    else:
        rooms = Room.query.all()
    return render_template('owner/rooms.html', rooms=rooms)


@app.route('/owner/rooms/edit/<int:room_id>', methods=['POST'])
def edit_room(room_id):
    room = Room.query.get_or_404(room_id)
    if 'owner_id' not in session or session['owner_id'] != room.owner_id:
        flash('Not authorized to edit this room.', 'danger')
        return redirect(url_for('owner_rooms'))

    room.name = request.form.get('room_name') or room.name
    room.price = request.form.get('price') or room.price
    room.capacity = request.form.get('capacity') or room.capacity
    room.beds = request.form.get('beds') or room.beds
    room.other_feature2 = request.form.get('other_feature2') or room.other_feature2
    room.other_feature3 = request.form.get('other_feature3') or room.other_feature3
    room.other_feature5 = request.form.get('other_feature5') or room.other_feature5

    # handle delete flags first (user removed image in modal)
    for i in range(1,6):
        if request.form.get(f'delete_image{i}') == '1':
            old = getattr(room, f'image{i}')
            if old:
                _delete_static_file(old)
            setattr(room, f'image{i}', None)

    # handle optional replacement images
    for i in range(1,6):
        file = request.files.get(f'image{i}')
        if file and file.filename and allowed_file(file.filename):
            # delete old (if any) to replace
            old = getattr(room, f'image{i}')
            if old:
                _delete_static_file(old)
            filename = secure_filename(file.filename)
            name, ext = os.path.splitext(filename)
            uniq = f"{name}_{room.owner_id}_{uuid.uuid4().hex}_{i}{ext}"
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], uniq)
            file.save(save_path)
            setattr(room, f'image{i}', os.path.join('uploads', uniq).replace('\\','/'))

    db.session.commit()
    flash('Room updated.', 'success')
    return redirect(url_for('owner_rooms'))


@app.route('/owner/rooms/delete/<int:room_id>', methods=['POST'])
def delete_room(room_id):
    room = Room.query.get_or_404(room_id)
    if 'owner_id' not in session or session['owner_id'] != room.owner_id:
        flash('Not authorized to delete this room.', 'danger')
        return redirect(url_for('owner_rooms'))

    # delete image files
    for i in range(1,6):
        img = getattr(room, f'image{i}')
        if img:
            _delete_static_file(img)

    db.session.delete(room)
    db.session.commit()
    flash('Room deleted.', 'info')
    return redirect(url_for('owner_rooms'))

@app.route("/owner/cottages", methods=["GET","POST"]) 
def owner_cottages():
    # Support GET: list cottages for current owner (if logged in) or all cottages
    if request.method == 'POST':
        # handle cottage creation with up to 5 images
        if 'owner_id' not in session:
            flash('You must be logged in as owner to add cottages.', 'danger')
            return redirect(url_for('owner_cottages'))
        owner_id = session['owner_id']
        name = request.form.get('room_name') or 'Untitled Cottage'
        price = request.form.get('price')
        capacity = request.form.get('capacity')
        beds = request.form.get('beds')
        other_feature2 = request.form.get('other_feature2')
        other_feature3 = request.form.get('other_feature3')
        other_feature5 = request.form.get('other_feature5')

        # prepare filenames
        filenames = [None] * 5
        for i in range(1,6):
            file = request.files.get(f'image{i}')
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                name_only, ext = os.path.splitext(filename)
                uniq = f"{name_only}_{owner_id}_{uuid.uuid4().hex}_{i}{ext}"
                save_path = os.path.join(app.config['UPLOAD_FOLDER'], uniq)
                file.save(save_path)
                filenames[i-1] = os.path.join('uploads', uniq).replace('\\','/')

        cottage = Cottage(
            owner_id=owner_id,
            name=name,
            price=price,
            capacity=capacity,
            beds=beds,
            other_feature2=other_feature2,
            other_feature3=other_feature3,
            other_feature5=other_feature5,
            image1=filenames[0],
            image2=filenames[1],
            image3=filenames[2],
            image4=filenames[3],
            image5=filenames[4]
        )
        db.session.add(cottage)
        db.session.commit()
        flash('Cottage added successfully.', 'success')
        return redirect(url_for('owner_cottages'))

    # GET
    cottages = []
    if 'owner_id' in session:
        cottages = Cottage.query.filter_by(owner_id=session['owner_id']).all()
    else:
        cottages = Cottage.query.all()
    return render_template('owner/cottages.html', cottages=cottages)


@app.route("/owner/foods", methods=["GET","POST"]) 
def owner_foods():
    # list or create food items
    if request.method == 'POST':
        if 'owner_id' not in session:
            flash('You must be logged in as owner to add foods.', 'danger')
            return redirect(url_for('owner_foods'))
        owner_id = session['owner_id']
        name = request.form.get('food_name') or 'Untitled Food'
        size = request.form.get('size')
        capacity = request.form.get('capacity')
        price = request.form.get('price')
        of1 = request.form.get('other_feature1')
        of2 = request.form.get('other_feature2')
        of3 = request.form.get('other_feature3')
        of4 = request.form.get('other_feature4')

        filenames = [None]*5
        for i in range(1,6):
            file = request.files.get(f'image{i}')
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                name_only, ext = os.path.splitext(filename)
                uniq = f"{name_only}_{owner_id}_{uuid.uuid4().hex}_{i}{ext}"
                save_path = os.path.join(app.config['UPLOAD_FOLDER'], uniq)
                file.save(save_path)
                filenames[i-1] = os.path.join('uploads', uniq).replace('\\','/')

        food = Food(
            owner_id=owner_id,
            name=name,
            size=size,
            capacity=capacity,
            price=price,
            other_feature1=of1,
            other_feature2=of2,
            other_feature3=of3,
            other_feature4=of4,
            image1=filenames[0],
            image2=filenames[1],
            image3=filenames[2],
            image4=filenames[3],
            image5=filenames[4]
        )
        db.session.add(food)
        db.session.commit()
        flash('Food item added.', 'success')
        return redirect(url_for('owner_foods'))

    foods = []
    if 'owner_id' in session:
        foods = Food.query.filter_by(owner_id=session['owner_id']).all()
    else:
        foods = Food.query.all()
    return render_template('owner/foods.html', foods=foods)


@app.route('/owner/foods/edit/<int:food_id>', methods=['POST'])
def edit_food(food_id):
    food = Food.query.get_or_404(food_id)
    if 'owner_id' not in session or session['owner_id'] != food.owner_id:
        flash('Not authorized to edit this food item.', 'danger')
        return redirect(url_for('owner_foods'))

    food.name = request.form.get('food_name') or food.name
    food.size = request.form.get('size') or food.size
    food.capacity = request.form.get('capacity') or food.capacity
    food.price = request.form.get('price') or food.price
    food.other_feature1 = request.form.get('other_feature1') or food.other_feature1
    food.other_feature2 = request.form.get('other_feature2') or food.other_feature2
    food.other_feature3 = request.form.get('other_feature3') or food.other_feature3
    food.other_feature4 = request.form.get('other_feature4') or food.other_feature4

    # handle delete flags
    for i in range(1,6):
        if request.form.get(f'delete_image{i}') == '1':
            old = getattr(food, f'image{i}')
            if old:
                _delete_static_file(old)
            setattr(food, f'image{i}', None)

    # replacements
    for i in range(1,6):
        file = request.files.get(f'image{i}')
        if file and file.filename and allowed_file(file.filename):
            old = getattr(food, f'image{i}')
            if old:
                _delete_static_file(old)
            filename = secure_filename(file.filename)
            name_only, ext = os.path.splitext(filename)
            uniq = f"{name_only}_{food.owner_id}_{uuid.uuid4().hex}_{i}{ext}"
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], uniq)
            file.save(save_path)
            setattr(food, f'image{i}', os.path.join('uploads', uniq).replace('\\','/'))

    db.session.commit()
    flash('Food updated.', 'success')
    return redirect(url_for('owner_foods'))


@app.route('/owner/foods/delete/<int:food_id>', methods=['POST'])
def delete_food(food_id):
    food = Food.query.get_or_404(food_id)
    if 'owner_id' not in session or session['owner_id'] != food.owner_id:
        flash('Not authorized to delete this food item.', 'danger')
        return redirect(url_for('owner_foods'))
    for i in range(1,6):
        img = getattr(food, f'image{i}')
        if img:
            _delete_static_file(img)
    db.session.delete(food)
    db.session.commit()
    flash('Food deleted.', 'info')
    return redirect(url_for('owner_foods'))


@app.route("/owner/activities", methods=["GET","POST"]) 
def owner_activities():
    # list or create activities
    if request.method == 'POST':
        if 'owner_id' not in session:
            flash('You must be logged in as owner to add activities.', 'danger')
            return redirect(url_for('owner_activities'))
        owner_id = session['owner_id']
        name = request.form.get('activity_name') or 'Untitled Activity'
        size = request.form.get('size')
        capacity = request.form.get('capacity')
        price = request.form.get('price')
        of1 = request.form.get('other_feature1')
        of2 = request.form.get('other_feature2')
        of3 = request.form.get('other_feature3')
        of4 = request.form.get('other_feature4')

        filenames = [None]*5
        for i in range(1,6):
            file = request.files.get(f'image{i}')
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                name_only, ext = os.path.splitext(filename)
                uniq = f"{name_only}_{owner_id}_{uuid.uuid4().hex}_{i}{ext}"
                save_path = os.path.join(app.config['UPLOAD_FOLDER'], uniq)
                file.save(save_path)
                filenames[i-1] = os.path.join('uploads', uniq).replace('\\','/')

        activity = Activity(
            owner_id=owner_id,
            name=name,
            size=size,
            capacity=capacity,
            price=price,
            other_feature1=of1,
            other_feature2=of2,
            other_feature3=of3,
            other_feature4=of4,
            image1=filenames[0],
            image2=filenames[1],
            image3=filenames[2],
            image4=filenames[3],
            image5=filenames[4]
        )
        db.session.add(activity)
        db.session.commit()
        flash('Activity added.', 'success')
        return redirect(url_for('owner_activities'))

    activities = []
    if 'owner_id' in session:
        activities = Activity.query.filter_by(owner_id=session['owner_id']).all()
    else:
        activities = Activity.query.all()
    return render_template('owner/activities.html', activities=activities)


@app.route('/owner/activities/edit/<int:activity_id>', methods=['POST'])
def edit_activity(activity_id):
    activity = Activity.query.get_or_404(activity_id)
    if 'owner_id' not in session or session['owner_id'] != activity.owner_id:
        flash('Not authorized to edit this activity.', 'danger')
        return redirect(url_for('owner_activities'))

    activity.name = request.form.get('activity_name') or activity.name
    activity.size = request.form.get('size') or activity.size
    activity.capacity = request.form.get('capacity') or activity.capacity
    activity.price = request.form.get('price') or activity.price
    activity.other_feature1 = request.form.get('other_feature1') or activity.other_feature1
    activity.other_feature2 = request.form.get('other_feature2') or activity.other_feature2
    activity.other_feature3 = request.form.get('other_feature3') or activity.other_feature3
    activity.other_feature4 = request.form.get('other_feature4') or activity.other_feature4

    # handle delete flags
    for i in range(1,6):
        if request.form.get(f'delete_image{i}') == '1':
            old = getattr(activity, f'image{i}')
            if old:
                _delete_static_file(old)
            setattr(activity, f'image{i}', None)

    # replacements
    for i in range(1,6):
        file = request.files.get(f'image{i}')
        if file and file.filename and allowed_file(file.filename):
            old = getattr(activity, f'image{i}')
            if old:
                _delete_static_file(old)
            filename = secure_filename(file.filename)
            name_only, ext = os.path.splitext(filename)
            uniq = f"{name_only}_{activity.owner_id}_{uuid.uuid4().hex}_{i}{ext}"
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], uniq)
            file.save(save_path)
            setattr(activity, f'image{i}', os.path.join('uploads', uniq).replace('\\','/'))

    db.session.commit()
    flash('Activity updated.', 'success')
    return redirect(url_for('owner_activities'))


@app.route('/owner/activities/delete/<int:activity_id>', methods=['POST'])
def delete_activity(activity_id):
    activity = Activity.query.get_or_404(activity_id)
    if 'owner_id' not in session or session['owner_id'] != activity.owner_id:
        flash('Not authorized to delete this activity.', 'danger')
        return redirect(url_for('owner_activities'))
    for i in range(1,6):
        img = getattr(activity, f'image{i}')
        if img:
            _delete_static_file(img)
    db.session.delete(activity)
    db.session.commit()
    flash('Activity deleted.', 'info')
    return redirect(url_for('owner_activities'))


@app.route('/owner/cottages/edit/<int:cottage_id>', methods=['POST'])
def edit_cottage(cottage_id):
    cottage = Cottage.query.get_or_404(cottage_id)
    if 'owner_id' not in session or session['owner_id'] != cottage.owner_id:
        flash('Not authorized to edit this cottage.', 'danger')
        return redirect(url_for('owner_cottages'))

    cottage.name = request.form.get('room_name') or cottage.name
    cottage.price = request.form.get('price') or cottage.price
    cottage.capacity = request.form.get('capacity') or cottage.capacity
    # beds removed for cottages
    cottage.other_feature2 = request.form.get('other_feature2') or cottage.other_feature2
    cottage.other_feature3 = request.form.get('other_feature3') or cottage.other_feature3
    cottage.other_feature5 = request.form.get('other_feature5') or cottage.other_feature5

    # handle delete flags
    for i in range(1,6):
        if request.form.get(f'delete_image{i}') == '1':
            old = getattr(cottage, f'image{i}')
            if old:
                _delete_static_file(old)
            setattr(cottage, f'image{i}', None)

    # handle replacements
    for i in range(1,6):
        file = request.files.get(f'image{i}')
        if file and file.filename and allowed_file(file.filename):
            old = getattr(cottage, f'image{i}')
            if old:
                _delete_static_file(old)
            filename = secure_filename(file.filename)
            name_only, ext = os.path.splitext(filename)
            uniq = f"{name_only}_{cottage.owner_id}_{uuid.uuid4().hex}_{i}{ext}"
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], uniq)
            file.save(save_path)
            setattr(cottage, f'image{i}', os.path.join('uploads', uniq).replace('\\','/'))

    db.session.commit()
    flash('Cottage updated.', 'success')
    return redirect(url_for('owner_cottages'))


@app.route('/owner/cottages/delete/<int:cottage_id>', methods=['POST'])
def delete_cottage(cottage_id):
    cottage = Cottage.query.get_or_404(cottage_id)
    if 'owner_id' not in session or session['owner_id'] != cottage.owner_id:
        flash('Not authorized to delete this cottage.', 'danger')
        return redirect(url_for('owner_cottages'))

    for i in range(1,6):
        img = getattr(cottage, f'image{i}')
        if img:
            _delete_static_file(img)

    db.session.delete(cottage)
    db.session.commit()
    flash('Cottage deleted.', 'info')
    return redirect(url_for('owner_cottages'))

@app.route("/userSignUp", methods=["GET", "POST"])
def user_sign_up():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        name = request.form.get("name")
        email = request.form.get("email")
        birthdate = request.form.get("birthdate")
        gender = request.form.get("gender")
        address = request.form.get("address")
        age = request.form.get("age")
        contact_number = request.form.get("contact_number")
        facebook = request.form.get("facebook")
        emergency_name = request.form.get("emergency_name")
        emergency_number = request.form.get("emergency_number")
        relationship = request.form.get("relationship")

        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return redirect(url_for("user_sign_up"))
        if User.query.filter_by(username=username).first():
            flash("Username already exists.", "danger")
            return redirect(url_for("user_sign_up"))
        hashed_pw = generate_password_hash(password)
        # handle avatar upload (single image)
        avatar_path = None
        file = request.files.get('avatar')
        if file and file.filename and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            name_only, ext = os.path.splitext(filename)
            uniq = f"{name_only}_{uuid.uuid4().hex}{ext}"
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], uniq)
            file.save(save_path)
            avatar_path = os.path.join('uploads', uniq).replace('\\','/')

        user = User(
            username=username,
            password=hashed_pw,
            name=name,
            email=email,
            birthdate=birthdate,
            gender=gender,
            address=address,
            age=age,
            contact_number=contact_number,
            facebook=facebook,
            emergency_name=emergency_name,
            emergency_number=emergency_number,
            relationship=relationship
            ,avatar=avatar_path
        )
        try:
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            # Surface the error to the user and keep them on the signup page
            flash(f"Registration failed: {e}", "danger")
            return redirect(url_for("user_sign_up"))
        flash("Registration successful! Please log in.", "success")
        return redirect(url_for("browse"))
    return render_template("userSignUp.html")

@app.route("/ownerSignUp", methods=["GET", "POST"])
def owner_sign_up():
    if request.method == "POST":
        # collect all form fields present in ownerSignUp.html
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        name = request.form.get("name")
        email = request.form.get("email")
        birthdate = request.form.get("birthdate")
        gender = request.form.get("gender")
        address = request.form.get("address")
        resort_address = request.form.get("resort_address")
        age = request.form.get("age")
        contact_number = request.form.get("contact_number")
        facebook = request.form.get("facebook")
        resort_name = request.form.get("resort_name")
        business_id = request.form.get("business_id")
        tax_id = request.form.get("tax_id")
        bank_account = request.form.get("bank_account")
        gcash = request.form.get("gcash")
        paymaya = request.form.get("paymaya")
        paypal = request.form.get("paypal")

        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return redirect(url_for("owner_sign_up"))
        if Owner.query.filter_by(username=username).first():
            flash("Username already exists.", "danger")
            return redirect(url_for("owner_sign_up"))
        hashed_pw = generate_password_hash(password)
        # handle avatar upload (single image)
        avatar_path = None
        file = request.files.get('avatar')
        if file and file.filename and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            name_only, ext = os.path.splitext(filename)
            uniq = f"{name_only}_{uuid.uuid4().hex}{ext}"
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], uniq)
            file.save(save_path)
            avatar_path = os.path.join('uploads', uniq).replace('\\','/')

        owner = Owner(
            username=username,
            password=hashed_pw,
            name=name,
            email=email,
            birthdate=birthdate,
            gender=gender,
            address=address,
            resort_address=resort_address,
            age=age,
            contact_number=contact_number,
            facebook=facebook,
            resort_name=resort_name,
            business_id=business_id,
            tax_id=tax_id,
            bank_account=bank_account,
            gcash=gcash,
            paymaya=paymaya,
            paypal=paypal
            ,avatar=avatar_path
        )
        try:
            db.session.add(owner)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash(f"Owner registration failed: {e}", "danger")
            return redirect(url_for("owner_sign_up"))
        flash("Owner registration successful! Please log in.", "success")
        return redirect(url_for("home"))
    return render_template("ownerSignUp.html")

@app.route("/login", methods=["POST"])
def login():
    user_type = request.form.get("user_type")
    username = request.form.get("username")
    password = request.form.get("password")
    if user_type == "owner":
        owner = Owner.query.filter_by(username=username).first()
        if owner and check_password_hash(owner.password, password):
            # store owner fields in session similar to user
            session["owner_id"] = owner.id
            session["owner_username"] = owner.username
            session["owner_name"] = owner.name
            session["owner_email"] = owner.email
            session["owner_birthdate"] = owner.birthdate
            session["owner_gender"] = owner.gender
            session["owner_address"] = owner.address
            session["owner_resort_address"] = owner.resort_address
            session["owner_age"] = owner.age
            session["owner_contact_number"] = owner.contact_number
            session["owner_facebook"] = owner.facebook
            session["owner_resort_name"] = owner.resort_name
            session["owner_business_id"] = owner.business_id
            session["owner_tax_id"] = owner.tax_id
            session["owner_bank_account"] = owner.bank_account
            session["owner_gcash"] = owner.gcash
            session["owner_paymaya"] = owner.paymaya
            session["owner_paypal"] = owner.paypal
            session["owner_avatar"] = owner.avatar
            # keep consistency for template fields (if used)
            session["emergency_name"] = None
            session["emergency_number"] = None
            session["relationship"] = None
            # on AJAX requests return JSON so client can stay on the page and handle navigation
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.is_json:
                return jsonify({"success": True, "redirect": url_for("browse")})
            flash("Logged in as owner!", "success")
            return redirect(url_for("browse"))
        else:
            message = "Invalid owner credentials."
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.is_json:
                return jsonify({"success": False, "message": message, "user_type": "owner"})
            flash(message, "danger")
    elif user_type == "admin":
        admin = Admin.query.filter_by(username=username).first()
        if admin and check_password_hash(admin.password, password):
            session["admin_id"] = admin.id
            session["admin_username"] = admin.username
            session["admin_name"] = admin.name
            session["admin_email"] = admin.email
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.is_json:
                return jsonify({"success": True, "redirect": url_for("admin_dashboard")})
            flash("Logged in as admin!", "success")
            return redirect(url_for("admin_dashboard"))
        else:
            message = "Invalid admin credentials."
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.is_json:
                return jsonify({"success": False, "message": message, "user_type": "admin"})
            flash(message, "danger")
    else:
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["username"] = user.username
            session["name"] = user.name
            session["email"] = user.email
            session["birthdate"] = user.birthdate
            session["gender"] = user.gender
            session["address"] = user.address
            session["age"] = user.age
            session["contact_number"] = user.contact_number
            session["facebook"] = user.facebook
            session["emergency_name"] = user.emergency_name
            session["emergency_number"] = user.emergency_number
            session["relationship"] = user.relationship
            session["avatar"] = user.avatar
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.is_json:
                return jsonify({"success": True, "redirect": url_for("browse")})
            flash("Logged in as user!", "success")
            return redirect(url_for("browse"))
        else:
            message = "Invalid user credentials."
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.is_json:
                return jsonify({"success": False, "message": message, "user_type": "user"})
            flash(message, "danger")
    # For non-AJAX requests, keep previous behavior (redirect back to referrer or home)
    return redirect(request.referrer or url_for("home"))


@app.route('/admin')
def admin_dashboard():
    # simple admin landing page; render admin template if exists otherwise redirect
    if 'admin_id' not in session:
        flash('You must be logged in as admin to view that page.', 'danger')
        return redirect(url_for('home'))
    # show latest 5 resorts (owners) on the admin dashboard
    recent_resorts = Owner.query.order_by(Owner.id.desc()).limit(5).all()
    return render_template('admin/dashboard.html', recent_resorts=recent_resorts)


@app.route('/admin/users')
def admin_users():
    if 'admin_id' not in session:
        flash('You must be logged in as admin to view that page.', 'danger')
        return redirect(url_for('home'))
    users = User.query.all()
    return render_template('admin/user.html', users=users)


@app.route('/admin/owners')
def admin_owners():
    if 'admin_id' not in session:
        flash('You must be logged in as admin to view that page.', 'danger')
        return redirect(url_for('home'))
    owners = Owner.query.all()
    return render_template('admin/owners.html', owners=owners)


@app.route('/admin/chats')
def admin_chats():
    if 'admin_id' not in session:
        flash('You must be logged in as admin to view that page.', 'danger')
        return redirect(url_for('home'))
    # Template renders chat UI; pass empty list for now
    chats = []
    return render_template('admin/chats.html', chats=chats)

@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out.", "info")
    return redirect(url_for("home"))

@app.route('/viewResortMain')
def view_resort_main():
    owner_id = request.args.get('owner_id')
    resort = None
    if owner_id:
        resort = Owner.query.get(owner_id)
    # build lists of images for rooms, cottages, and foods (first non-empty image per item)
    rooms_with_images = []
    cottages_with_images = []
    foods_with_images = []
    activities_with_images = []
    if resort:
        for r in getattr(resort, 'rooms', []) or []:
            img = r.image1 or r.image2 or r.image3 or r.image4 or r.image5
            if img:
                rooms_with_images.append(img)
        for c in getattr(resort, 'cottages', []) or []:
            img = c.image1 or c.image2 or c.image3 or c.image4 or c.image5
            if img:
                cottages_with_images.append(img)
        for f in getattr(resort, 'foods', []) or []:
            img = f.image1 or f.image2 or f.image3 or f.image4 or f.image5
            if img:
                foods_with_images.append(img)
        for a in getattr(resort, 'activities', []) or []:
            img = a.image1 or a.image2 or a.image3 or a.image4 or a.image5
            if img:
                activities_with_images.append(img)

    return render_template('viewResortMain.html', resort=resort,
                           rooms_with_images=rooms_with_images,
                           cottages_with_images=cottages_with_images,
                           foods_with_images=foods_with_images,
                           activities_with_images=activities_with_images)


@app.route('/api/conversation', methods=['POST'])
def api_create_conversation():
    """Create or return an existing conversation between current user and an owner.
    Request JSON: { owner_id: int }
    Response: { success: bool, conversation_id: int, message: str }
    """
    data = request.get_json() or {}

    # require a logged-in user or owner
    if 'user_id' not in session and 'owner_id' not in session:
        return jsonify({'success': False, 'message': 'Authentication required'}), 401

    # If a user is initiating chat with owner, require owner_id in payload
    if 'user_id' in session:
        owner_id = data.get('owner_id')
        if not owner_id:
            return jsonify({'success': False, 'message': 'owner_id required'}), 400
        user_id = session['user_id']
        # check existing
        conv = Conversation.query.filter_by(user_id=user_id, owner_id=owner_id).first()
        if not conv:
            conv = Conversation(user_id=user_id, owner_id=owner_id)
            db.session.add(conv)
            db.session.commit()
        return jsonify({'success': True, 'conversation_id': conv.id})

    # If an owner is initiating (owner messaging a user), require user_id in payload
    if 'owner_id' in session:
        user_id = data.get('user_id')
        if not user_id:
            return jsonify({'success': False, 'message': 'user_id required for owner-initiated conversation'}), 400
        conv = Conversation.query.filter_by(user_id=user_id, owner_id=session['owner_id']).first()
        if not conv:
            conv = Conversation(user_id=user_id, owner_id=session['owner_id'])
            db.session.add(conv)
            db.session.commit()
        return jsonify({'success': True, 'conversation_id': conv.id})


@app.route('/api/conversation/<int:conv_id>/messages', methods=['GET'])
def api_get_messages(conv_id):
    # auth check: user or owner must be part of the conversation
    conv = Conversation.query.get(conv_id)
    if not conv:
        return jsonify({'success': False, 'message': 'conversation not found'}), 404

    if 'user_id' in session and session['user_id'] != conv.user_id:
        return jsonify({'success': False, 'message': 'not authorized'}), 403
    if 'owner_id' in session and session['owner_id'] != conv.owner_id:
        return jsonify({'success': False, 'message': 'not authorized'}), 403

    msgs = []
    for m in conv.messages:
        msgs.append({
            'id': m.id,
            'sender': m.sender,
            'text': m.text,
            'created_at': m.created_at.isoformat()
        })
    return jsonify({'success': True, 'messages': msgs})


@app.route('/api/conversation/<int:conv_id>/message', methods=['POST'])
def api_send_message(conv_id):
    conv = Conversation.query.get(conv_id)
    if not conv:
        return jsonify({'success': False, 'message': 'conversation not found'}), 404

    data = request.get_json() or {}
    text = (data.get('text') or '').strip()
    if not text:
        return jsonify({'success': False, 'message': 'text required'}), 400

    # determine sender
    if 'user_id' in session and session['user_id'] == conv.user_id:
        sender = 'user'
        m = Message(conversation_id=conv.id, sender=sender, sender_user_id=session['user_id'], text=text)
    elif 'owner_id' in session and session['owner_id'] == conv.owner_id:
        sender = 'owner'
        m = Message(conversation_id=conv.id, sender=sender, sender_owner_id=session['owner_id'], text=text)
    else:
        return jsonify({'success': False, 'message': 'not authorized to send message in this conversation'}), 403

    db.session.add(m)
    db.session.commit()

    return jsonify({'success': True, 'message_id': m.id, 'created_at': m.created_at.isoformat()})


@app.route('/api/reserve', methods=['POST'])
def api_reserve():
    """Create a reservation. Expects JSON with: resource_type, resource_id, owner_id, check_in, check_out, guests"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Login required'}), 401
    data = request.get_json() or {}
    resource_type = (data.get('resource_type') or '').lower()
    resource_id = data.get('resource_id')
    owner_id = data.get('owner_id')
    check_in = data.get('check_in')
    check_out = data.get('check_out')
    guests = data.get('guests')

    if resource_type not in ('room', 'cottage'):
        return jsonify({'success': False, 'message': 'Invalid resource_type'}), 400
    if not resource_id or not owner_id or not check_in or not check_out:
        return jsonify({'success': False, 'message': 'Missing fields'}), 400
    try:
        check_in_date = datetime.fromisoformat(check_in).date()
        check_out_date = datetime.fromisoformat(check_out).date()
    except Exception:
        return jsonify({'success': False, 'message': 'Invalid date format, use YYYY-MM-DD'}), 400
    if check_out_date <= check_in_date:
        return jsonify({'success': False, 'message': 'check_out must be after check_in'}), 400

    # Basic conflict check: ensure no existing confirmed reservation overlaps for same resource
    overlaps = Reservation.query.filter(
        Reservation.resource_type == resource_type,
        Reservation.resource_id == resource_id,
        Reservation.status == 'confirmed',
        Reservation.check_in <= check_out_date,
        Reservation.check_out >= check_in_date,
    ).count()
    if overlaps > 0:
        return jsonify({'success': False, 'message': 'Selected dates are not available'}), 409

    r = Reservation(
        user_id=session['user_id'],
        owner_id=owner_id,
        resource_type=resource_type,
        resource_id=resource_id,
        check_in=check_in_date,
        check_out=check_out_date,
        guests=guests,
        status='pending'
    )
    db.session.add(r)
    db.session.commit()
    return jsonify({'success': True, 'reservation_id': r.id, 'status': r.status})


@app.route('/api/owner/reservations/<int:reservation_id>/action', methods=['POST'])
def api_owner_reservation_action(reservation_id):
    # owner-only: action in JSON { action: 'confirm'|'cancel' }
    if 'owner_id' not in session:
        return jsonify({'success': False, 'message': 'Owner login required'}), 401
    r = Reservation.query.get(reservation_id)
    if not r or r.owner_id != session['owner_id']:
        return jsonify({'success': False, 'message': 'Reservation not found or not authorized'}), 404
    data = request.get_json() or {}
    action = (data.get('action') or '').lower()
    if action == 'confirm':
        # ensure no confirmed overlap
        overlaps = Reservation.query.filter(
            Reservation.id != r.id,
            Reservation.resource_type == r.resource_type,
            Reservation.resource_id == r.resource_id,
            Reservation.status == 'confirmed',
            Reservation.check_in <= r.check_out,
            Reservation.check_out >= r.check_in,
        ).count()
        if overlaps > 0:
            return jsonify({'success': False, 'message': 'Conflicting confirmed reservation exists'}), 409
        r.status = 'confirmed'
    elif action == 'cancel':
        r.status = 'cancelled'
    else:
        return jsonify({'success': False, 'message': 'Invalid action'}), 400
    db.session.commit()
    return jsonify({'success': True, 'status': r.status})


@app.route('/api/confirmed_reservations', methods=['GET'])
def api_confirmed_reservations():
    """Return list of confirmed reservation dates for an owner/resource in a given month.
    Query params: owner_id, resource_type (optional), resource_id (optional), month (1-12), year
    Response: { success: True, dates: ['YYYY-MM-DD', ...] }
    """
    owner_id = request.args.get('owner_id')
    resource_type = request.args.get('resource_type')
    resource_id = request.args.get('resource_id')
    try:
        month = int(request.args.get('month') or 0)
        year = int(request.args.get('year') or 0)
    except Exception:
        return jsonify({'success': False, 'message': 'Invalid month/year'}), 400
    if not owner_id:
        return jsonify({'success': False, 'message': 'owner_id required'}), 400

    # build base query
    q = Reservation.query.filter_by(owner_id=owner_id, status='confirmed')
    if resource_type:
        q = q.filter(Reservation.resource_type == resource_type)
    if resource_id:
        q = q.filter(Reservation.resource_id == resource_id)

    results = q.all()

    # compute first and last day of month
    from calendar import monthrange
    from datetime import timedelta
    try:
        first_day = datetime(year, month, 1).date()
    except Exception:
        return jsonify({'success': False, 'message': 'Invalid month/year combination'}), 400
    last_day = datetime(year, month, monthrange(year, month)[1]).date()

    dates = set()
    for r in results:
        # if reservation overlaps the month
        if not r.check_in or not r.check_out:
            continue
        if r.check_out < first_day or r.check_in > last_day:
            continue
        # overlap -> enumerate dates within the overlap range
        start = max(r.check_in, first_day)
        end = min(r.check_out, last_day)
        d = start
        while d <= end:
            dates.add(d.isoformat())
            d = d + timedelta(days=1)

    return jsonify({'success': True, 'dates': sorted(list(dates))})


@app.route('/api/user/reservations', methods=['GET'])
def api_user_reservations():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Login required'}), 401
    resvs = Reservation.query.filter_by(user_id=session['user_id']).order_by(Reservation.created_at.desc()).all()
    out = []
    for r in resvs:
        out.append({
            'id': r.id,
            'resource_type': r.resource_type,
            'resource_id': r.resource_id,
            'check_in': r.check_in.isoformat() if r.check_in else None,
            'check_out': r.check_out.isoformat() if r.check_out else None,
            'guests': r.guests,
            'status': r.status,
            'owner_id': r.owner_id,
        })
    return jsonify({'success': True, 'reservations': out})


@app.route('/api/user/reservations/<int:reservation_id>/action', methods=['POST'])
def api_user_reservation_action(reservation_id):
    # user-only actions like cancel
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Login required'}), 401
    r = Reservation.query.get(reservation_id)
    if not r or r.user_id != session['user_id']:
        return jsonify({'success': False, 'message': 'Reservation not found or not authorized'}), 404
    data = request.get_json() or {}
    action = (data.get('action') or '').lower()
    if action == 'cancel':
        r.status = 'cancelled'
    else:
        return jsonify({'success': False, 'message': 'Invalid action'}), 400
    db.session.commit()
    return jsonify({'success': True, 'status': r.status})


@app.route('/api/recent_conversations', methods=['GET'])
def api_recent_conversations():
    """Return recent conversations for the currently logged-in user or owner.
    Response: { success: True, conversations: [ { id, partner_name, partner_avatar, last_text, last_time, unread, owner_id, user_id } ] }
    """
    if 'user_id' not in session and 'owner_id' not in session:
        return jsonify({'success': False, 'message': 'Authentication required'}), 401

    convs = []
    if 'user_id' in session:
        rows = Conversation.query.filter_by(user_id=session['user_id']).order_by(Conversation.created_at.desc()).all()
        for c in rows:
            last_msg = c.messages[-1] if c.messages else None
            partner_name = c.owner.resort_name if c.owner and c.owner.resort_name else (c.owner.name if c.owner else 'Owner')
            unread = False
            if last_msg and last_msg.sender == 'owner':
                # treat last messages from owner as unread for the user (simple heuristic)
                unread = True
            convs.append({
                'id': c.id,
                'partner_name': partner_name,
                'partner_avatar': c.owner.avatar if c.owner else None,
                'last_text': last_msg.text if last_msg else None,
                'last_time': last_msg.created_at.isoformat() if last_msg else None,
                'unread': unread,
                'owner_id': c.owner_id,
                'user_id': c.user_id,
            })
    else:
        rows = Conversation.query.filter_by(owner_id=session['owner_id']).order_by(Conversation.created_at.desc()).all()
        for c in rows:
            last_msg = c.messages[-1] if c.messages else None
            partner_name = c.user.name if c.user and c.user.name else 'Customer'
            unread = False
            if last_msg and last_msg.sender == 'user':
                # treat last messages from user as unread for the owner
                unread = True
            convs.append({
                'id': c.id,
                'partner_name': partner_name,
                'partner_avatar': c.user.avatar if c.user else None,
                'last_text': last_msg.text if last_msg else None,
                'last_time': last_msg.created_at.isoformat() if last_msg else None,
                'unread': unread,
                'owner_id': c.owner_id,
                'user_id': c.user_id,
            })

    return jsonify({'success': True, 'conversations': convs})


@app.route('/viewResortRoom')
def view_resort_room():
    owner_id = request.args.get('owner_id')
    owner = None
    rooms = []
    if owner_id:
        owner = Owner.query.get(owner_id)
        if owner:
            rooms = getattr(owner, 'rooms', []) or []
    else:
        # show all rooms when no owner specified
        rooms = Room.query.all()

    return render_template('viewResortRoom.html', owner=owner, rooms=rooms)


@app.route('/viewResortCottage')
def view_resort_cottage():
    owner_id = request.args.get('owner_id')
    owner = None
    cottages = []
    if owner_id:
        owner = Owner.query.get(owner_id)
        if owner:
            cottages = getattr(owner, 'cottages', []) or []
    else:
        # show all cottages when no owner specified
        cottages = Cottage.query.all()

    return render_template('viewResortCottage.html', owner=owner, cottages=cottages)


@app.route('/viewResortFood')
def view_resort_food():
    owner_id = request.args.get('owner_id')
    owner = None
    foods = []
    if owner_id:
        owner = Owner.query.get(owner_id)
        if owner:
            foods = getattr(owner, 'foods', []) or []
    else:
        # show all foods when no owner specified
        foods = Food.query.all()

    return render_template('viewResortFood.html', owner=owner, foods=foods)


@app.route('/viewResortActivities')
def view_resort_activities():
    owner_id = request.args.get('owner_id')
    owner = None
    activities = []
    if owner_id:
        owner = Owner.query.get(owner_id)
        if owner:
            activities = getattr(owner, 'activities', []) or []
    else:
        # show all activities when no owner specified
        activities = Activity.query.all()

    return render_template('viewResortActivities.html', owner=owner, activities=activities)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Ensure default admin exists
        default_admin = Admin.query.filter_by(username='admin').first()
        if not default_admin:
            hashed = generate_password_hash('password')
            admin = Admin(username='admin', password=hashed, name='Administrator', email='admin@example.com')
            db.session.add(admin)
            db.session.commit()
    app.run(debug=True)
