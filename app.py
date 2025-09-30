from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# file upload settings
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
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
    return render_template("owner/reservations.html")

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
        db.session.add(user)
        db.session.commit()
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
        db.session.add(owner)
        db.session.commit()
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
            flash("Logged in as owner!", "success")
            return redirect(url_for("browse"))
        else:
            flash("Invalid owner credentials.", "danger")
    elif user_type == "admin":
        admin = Admin.query.filter_by(username=username).first()
        if admin and check_password_hash(admin.password, password):
            session["admin_id"] = admin.id
            session["admin_username"] = admin.username
            session["admin_name"] = admin.name
            session["admin_email"] = admin.email
            flash("Logged in as admin!", "success")
            return redirect(url_for("admin_dashboard"))
        else:
            flash("Invalid admin credentials.", "danger")
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
            flash("Logged in as user!", "success")
            return redirect(url_for("browse"))
        else:
            flash("Invalid user credentials.", "danger")
    return redirect(url_for("home"))


@app.route('/admin')
def admin_dashboard():
    # simple admin landing page; render admin template if exists otherwise redirect
    if 'admin_id' not in session:
        flash('You must be logged in as admin to view that page.', 'danger')
        return redirect(url_for('home'))
    return render_template('admin/dashboard.html')


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

    return render_template('viewResortMain.html', resort=resort,
                           rooms_with_images=rooms_with_images,
                           cottages_with_images=cottages_with_images,
                           foods_with_images=foods_with_images)


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
