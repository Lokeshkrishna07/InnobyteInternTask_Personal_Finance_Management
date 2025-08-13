from .auth_routes import auth_bp
from .transaction_routes import transaction_bp
from .category_routes import category_bp
from .budget_routes import budget_bp
from .report_routes import report_bp
from .ui_routes import ui_bp
from .admin_routes import admin_bp

__all__ = ["auth_bp", "transaction_bp", "category_bp", "budget_bp", "report_bp", "ui_bp", "admin_bp"]
