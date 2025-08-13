from datetime import date
from .models import Transaction, Budget
from .database import db

def get_month_year_from_date(d):
    return d.month, d.year

def calculate_monthly_spend(user_id, category_id, month, year):
    from sqlalchemy import extract, func
    total = db.session.query(func.coalesce(func.sum(Transaction.amount), 0.0)).filter(
        Transaction.user_id == user_id,
        Transaction.category_id == category_id,
        extract('month', Transaction.date) == month,
        extract('year', Transaction.date) == year,
        Transaction.type == "expense"
    ).scalar()
    return float(total or 0.0)

def check_budget_and_notify(user, category, month, year):
    budget = Budget.query.filter_by(user_id=user.id, category_id=category.id, month=month, year=year).first()
    spent = calculate_monthly_spend(user.id, category.id, month, year)
    if not budget:
        return False, spent, None
    is_over = spent > budget.limit_amount
    return is_over, spent, budget.limit_amount
