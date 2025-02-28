from flask import jsonify, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from app.models import db, Users, Birthdays
from app.helpers import log, calculate_age, date_convert, generate_potp_secret_key, verification_email
from sqlalchemy.sql import func

from flask import Blueprint
api = Blueprint('api', __name__)

@api.route("/api/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    phone = data.get("phone")
    dob = data.get("dob")
    name = data.get("name")
    password = data.get("password")
    confirmation = data.get("confirmation")
    
    if not username or not password or not email or not phone or not name:
        return jsonify({"error": "All fields are required!"}), 400

    if password != confirmation:
        return jsonify({"error": "Password mismatch!"}), 400

    hash = generate_password_hash(password, method='pbkdf2:sha256:600000', salt_length=16)
    
    try:
        user = Users(name=name, username=username, hash=hash, dob=dob, email=email, phone=phone, password_set=True, totp_secret=generate_potp_secret_key())
        db.session.add(user)
        db.session.commit()

        login_user(user)
        log("register")

        verification_email(current_user)
        return jsonify({"message": "User registered successfully!"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Username or email already exists!"}), 403

@api.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Must provide username and password"}), 400

    user = Users.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.hash, password):
        return jsonify({"error": "Invalid username or password"}), 403

    login_user(user)
    log("log_in")
    return jsonify({"message": "Login successful", "user": {"id": user.id, "username": user.username, "email": user.email}})

@api.route("/api/logout", methods=["POST"])
@login_required
def logout():
    log("log out")
    logout_user()
    return jsonify({"message": "You have successfully logged out"})

@api.route("/api/birthdays", methods=["GET"])
@login_required
def get_birthdays():
    birthdays = Birthdays.query.filter_by(user_id=current_user.id).all()
    friends = [{"id": b.id, "name": b.name, "birthdate": b.birthdates, "phone": b.phone, "email": b.email} for b in birthdays]
    return jsonify(friends)

@api.route("/api/add_birthday", methods=["POST"])
@login_required
def add_birthday():
    data = request.get_json()
    name = data.get("name")
    birthdate = date_convert(data.get("birthdate"))
    phone = data.get("phone")
    email = data.get("email")

    if not name or not birthdate or not phone or not email:
        return jsonify({"error": "All fields are required"}), 400

    age = calculate_age(birthdate)
    birthday = Birthdays(user_id=current_user.id, name=name, birthdates=birthdate, phone=phone, email=email, age=age)

    try:
        db.session.add(birthday)
        db.session.commit()
        log(f"added_{name}")
        return jsonify({"message": f"{name} added successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An error occurred while adding birthday"}), 500

@api.route("/api/delete_birthday/<int:id>", methods=["DELETE"])
@login_required
def delete_birthday(id):
    friend = Birthdays.query.filter_by(id=id, user_id=current_user.id).first()
    if not friend:
        return jsonify({"error": "Birthday not found"}), 404

    try:
        db.session.delete(friend)
        db.session.commit()
        log(f"deleted_{friend.name}")
        return jsonify({"message": f"{friend.name} deleted successfully"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An error occurred while deleting birthday"}), 500
