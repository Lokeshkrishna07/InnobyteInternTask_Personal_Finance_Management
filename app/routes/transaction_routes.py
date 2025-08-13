from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from ..database import db
from ..models import Transaction, Category
from datetime import datetime
from ..utils import check_budget_and_notify

transaction_bp = Blueprint("transactions", __name__)

@transaction_bp.route("/", methods=["POST"])
@login_required
def create_transaction():
    data = request.get_json() or {}
    try:
        amount = float(data.get("amount"))
    except (TypeError, ValueError):
        return jsonify({"error": "invalid amount"}), 400
    category_id = data.get("category_id")
    ttype = data.get("type")
    date_str = data.get("date")
    description = data.get("description", "")

    if ttype not in ("income", "expense"):
        return jsonify({"error": "invalid type"}), 400

    cat = Category.query.filter_by(id=category_id, user_id=current_user.id).first()
    if not cat:
        return jsonify({"error": "category not found"}), 404

    if date_str:
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
    else:
        date = datetime.utcnow().date()

    tx = Transaction(amount=amount, description=description, date=date, type=ttype, user_id=current_user.id, category_id=cat.id)
    db.session.add(tx)
    db.session.commit()

    month, year = date.month, date.year
    is_over, spent, limit_amount = check_budget_and_notify(current_user, cat, month, year)
    if is_over:
        print(f"[BUDGET ALERT] User {current_user.username} exceeded budget for {cat.name}: spent {spent} > {limit_amount}")

    response = {"id": tx.id, "amount": tx.amount, "type": tx.type, "date": str(tx.date)}
    if limit_amount is not None:
        response["budget"] = {"category": cat.name, "limit": limit_amount, "spent": spent, "is_over": is_over}
    return jsonify(response), 201

@transaction_bp.route("/", methods=["GET"])
@login_required
def list_transactions():
    q = Transaction.query.filter_by(user_id=current_user.id)
    args = request.args
    if "category_id" in args:
        q = q.filter_by(category_id=int(args.get("category_id")))
    if "start_date" in args:
        q = q.filter(Transaction.date >= args.get("start_date"))
    if "end_date" in args:
        q = q.filter(Transaction.date <= args.get("end_date"))
    txs = q.order_by(Transaction.date.desc()).all()
    return jsonify([{"id": t.id, "amount": t.amount, "type": t.type, "date": str(t.date),
                     "category_id": t.category_id, "description": t.description} for t in txs])

@transaction_bp.route("/<int:tx_id>", methods=["PUT"])
@login_required
def update_transaction(tx_id):
    tx = Transaction.query.filter_by(id=tx_id, user_id=current_user.id).first_or_404()
    data = request.get_json() or {}
    if "amount" in data:
        try:
            tx.amount = float(data.get("amount"))
        except (TypeError, ValueError):
            pass
    if "description" in data:
        tx.description = data.get("description")
    if "date" in data:
        from datetime import datetime
        tx.date = datetime.strptime(data.get("date"), "%Y-%m-%d").date()
    if "type" in data and data.get("type") in ("income", "expense"):
        tx.type = data.get("type")
    if "category_id" in data:
        cat = Category.query.filter_by(id=data.get("category_id"), user_id=current_user.id).first()
        if not cat:
            return jsonify({"error": "category not found"}), 404
        tx.category_id = cat.id
    db.session.commit()
    return jsonify({"message": "updated"})

@transaction_bp.route("/<int:tx_id>", methods=["DELETE"])
@login_required
def delete_transaction(tx_id):
    tx = Transaction.query.filter_by(id=tx_id, user_id=current_user.id).first_or_404()
    db.session.delete(tx)
    db.session.commit()
    return jsonify({"message": "deleted"})
