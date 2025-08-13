from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from ..database import db
from ..models import Category

category_bp = Blueprint("categories", __name__)

@category_bp.route("/", methods=["POST"])
@login_required
def create_category():
    data = request.get_json() or {}
    name = data.get("name")
    ctype = data.get("type")
    if not name or ctype not in ("income", "expense"):
        return jsonify({"error": "name and valid type required"}), 400
    existing = Category.query.filter_by(name=name, user_id=current_user.id, type=ctype).first()
    if existing:
        return jsonify({"error": "category already exists"}), 400
    cat = Category(name=name, type=ctype, user_id=current_user.id)
    db.session.add(cat)
    db.session.commit()
    return jsonify({"id": cat.id, "name": cat.name, "type": cat.type}), 201

@category_bp.route("/", methods=["GET"])
@login_required
def list_categories():
    cats = Category.query.filter_by(user_id=current_user.id).all()
    return jsonify([{"id": c.id, "name": c.name, "type": c.type} for c in cats])

@category_bp.route("/<int:cat_id>", methods=["PUT"])
@login_required
def update_category(cat_id):
    cat = Category.query.filter_by(id=cat_id, user_id=current_user.id).first_or_404()
    data = request.get_json() or {}
    name = data.get("name")
    if name:
        cat.name = name
    db.session.commit()
    return jsonify({"id": cat.id, "name": cat.name, "type": cat.type})

@category_bp.route("/<int:cat_id>", methods=["DELETE"])
@login_required
def delete_category(cat_id):
    cat = Category.query.filter_by(id=cat_id, user_id=current_user.id).first_or_404()
    db.session.delete(cat)
    db.session.commit()
    return jsonify({"message": "deleted"})
