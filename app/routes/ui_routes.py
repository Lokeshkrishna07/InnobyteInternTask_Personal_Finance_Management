from flask import Blueprint, render_template

ui_bp = Blueprint("ui", __name__)

@ui_bp.route("/")
def index():
    return render_template("index.html")

@ui_bp.route("/login")
def login_page():
    return render_template("login.html")

@ui_bp.route("/register")
def register_page():
    return render_template("register.html")

@ui_bp.route("/transactions")
def transactions_page():
    return render_template("transactions.html")

@ui_bp.route("/reports")
def reports_page():
    return render_template("reports.html")

@ui_bp.route("/budgets")
def budgets_page():
    return render_template("budgets.html")

@ui_bp.route("/backup")
def backup_page():
    return render_template("backup.html")
