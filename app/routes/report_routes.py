from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from ..models import Transaction
from sqlalchemy import func
from datetime import datetime

report_bp = Blueprint("reports", __name__)

@report_bp.route("/monthly", methods=["GET"])
@login_required
def monthly_report():
    month = int(request.args.get("month", datetime.utcnow().month))
    year = int(request.args.get("year", datetime.utcnow().year))
    category_id = request.args.get("category_id", None)

    q = Transaction.query.filter(func.extract('month', Transaction.date) == month, func.extract('year', Transaction.date) == year, Transaction.user_id == current_user.id)
    if category_id:
        q = q.filter(Transaction.category_id == int(category_id))

    income = q.filter(Transaction.type == "income").with_entities(func.coalesce(func.sum(Transaction.amount), 0.0)).scalar() or 0.0
    expense = q.filter(Transaction.type == "expense").with_entities(func.coalesce(func.sum(Transaction.amount), 0.0)).scalar() or 0.0
    savings = float(income) - float(expense)

    return jsonify({"month": month, "year": year, "income": float(income), "expense": float(expense), "savings": float(savings)})

@report_bp.route("/range", methods=["GET"])
@login_required
def range_report():
    start = request.args.get("start_date")
    end = request.args.get("end_date")
    q = Transaction.query.filter(Transaction.user_id == current_user.id)
    if start:
        q = q.filter(Transaction.date >= start)
    if end:
        q = q.filter(Transaction.date <= end)
    income = q.filter(Transaction.type == "income").with_entities(func.coalesce(func.sum(Transaction.amount), 0.0)).scalar() or 0.0
    expense = q.filter(Transaction.type == "expense").with_entities(func.coalesce(func.sum(Transaction.amount), 0.0)).scalar() or 0.0
    return jsonify({"start": start, "end": end, "income": float(income), "expense": float(expense), "savings": float(income) - float(expense)})
