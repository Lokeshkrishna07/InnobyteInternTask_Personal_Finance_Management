from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from ..database import db
from ..models import Budget, Category
from ..utils import calculate_monthly_spend

budget_bp = Blueprint("budgets", __name__)

@budget_bp.route("/", methods=["POST"])
@login_required
def set_budget():
    data = request.get_json() or {}
    try:
        month = int(data.get("month"))
        year = int(data.get("year"))
        limit_amount = float(data.get("limit_amount"))
    except (TypeError, ValueError):
        return jsonify({"error": "invalid month/year/limit_amount"}), 400
    category_id = data.get("category_id")
    cat = Category.query.filter_by(id=category_id, user_id=current_user.id).first()
    if not cat:
        return jsonify({"error": "category not found"}), 404

    budget = Budget.query.filter_by(month=month, year=year, category_id=cat.id, user_id=current_user.id).first()
    if budget:
        budget.limit_amount = limit_amount
    else:
        budget = Budget(month=month, year=year, limit_amount=limit_amount, user_id=current_user.id, category_id=cat.id)
        db.session.add(budget)
    db.session.commit()
    return jsonify({"id": budget.id, "limit_amount": budget.limit_amount}), 201

@budget_bp.route("/<int:budget_id>", methods=["GET"])
@login_required
def get_budget(budget_id):
    b = Budget.query.filter_by(id=budget_id, user_id=current_user.id).first_or_404()
    spent = calculate_monthly_spend(current_user.id, b.category_id, b.month, b.year)
    return jsonify({"id": b.id, "month": b.month, "year": b.year, "limit_amount": b.limit_amount, "spent": spent})
