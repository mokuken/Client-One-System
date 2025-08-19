from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
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
    # Add other fields as needed

class Owner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(120))
    email = db.Column(db.String(120))
    # Add other fields as needed

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/browse")
def browse():
    return render_template("browse.html")

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
        }
    return render_template("user/profile.html", user=user_data)

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
        )
        db.session.add(user)
        db.session.commit()
        flash("Registration successful! Please log in.", "success")
        return redirect(url_for("browse"))
    return render_template("userSignUp.html")

@app.route("/ownerSignUp", methods=["GET", "POST"])
def owner_sign_up():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        name = request.form.get("name")
        email = request.form.get("email")
        if Owner.query.filter_by(username=username).first():
            flash("Username already exists.", "danger")
            return redirect(url_for("owner_sign_up"))
        hashed_pw = generate_password_hash(password)
        owner = Owner(username=username, password=hashed_pw, name=name, email=email)
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
            session["owner_id"] = owner.id
            session["owner_username"] = owner.username
            session["owner_name"] = owner.name
            session["owner_email"] = owner.email
            flash("Logged in as owner!", "success")
            return redirect(url_for("home"))
        else:
            flash("Invalid owner credentials.", "danger")
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
            flash("Logged in as user!", "success")
            return redirect(url_for("browse"))
        else:
            flash("Invalid user credentials.", "danger")
    return redirect(url_for("home"))

@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out.", "info")
    return redirect(url_for("home"))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
