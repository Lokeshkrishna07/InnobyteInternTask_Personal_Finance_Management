from flask import Blueprint, request, jsonify
from ..database import db
from ..models import User
from flask_login import login_user, logout_user, login_required, current_user
from .. import bcrypt

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return jsonify({"error": "username and password required"}), 400
    if User.query.filter_by(username=username).first():
        return jsonify({"error": "username already exists"}), 400
    user = User(username=username)
    user.set_password(password, bcrypt)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "user created", "username": username}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return jsonify({"error": "username and password required"}), 400
    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password, bcrypt):
        return jsonify({"error": "invalid credentials"}), 401
    login_user(user)
    return jsonify({"message": "logged in", "username": user.username}), 200

@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "logged out"}), 200

@auth_bp.route("/me", methods=["GET"])
@login_required
def me():
    return jsonify({"id": current_user.id, "username": current_user.username})
