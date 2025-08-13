import os
from flask import Flask
from .database import db, migrate
from .models import User, Category, Transaction, Budget
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from config import Config

bcrypt = Bcrypt()
login_manager = LoginManager()

def create_app(config_class=Config):
    app = Flask(__name__, instance_relative_config=False, template_folder="../templates", static_folder="../static")
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    # register blueprints
    from .routes import auth_bp, transaction_bp, category_bp, budget_bp, report_bp, ui_bp, admin_bp
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(transaction_bp, url_prefix="/api/transactions")
    app.register_blueprint(category_bp, url_prefix="/api/categories")
    app.register_blueprint(budget_bp, url_prefix="/api/budgets")
    app.register_blueprint(report_bp, url_prefix="/api/reports")
    app.register_blueprint(admin_bp, url_prefix="/api/admin")
    app.register_blueprint(ui_bp, url_prefix="")

    # ensure data dir exists
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    os.makedirs(data_dir, exist_ok=True)

    # register CLI
    from .cli import backup_db, restore_db
    app.cli.add_command(backup_db)
    app.cli.add_command(restore_db)

    return app

from .models import User as UserModel

@login_manager.user_loader
def load_user(user_id):
    return UserModel.query.get(int(user_id))
