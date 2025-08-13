from flask import Blueprint, jsonify, request, current_app
from flask_login import login_required, current_user
from pathlib import Path
import shutil, os
from ..cli import DATA_DIR, BACKUP_DIR, DB_FILE

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/backup", methods=["POST"])
@login_required
def backup():
    BACKUP_DIR.mkdir(exist_ok=True)
    dest = BACKUP_DIR / f"finance_tracker_backup_{int(__import__('time').time())}.db"
    if DB_FILE.exists():
        shutil.copy(DB_FILE, dest)
        return jsonify({"message":"backup created", "file": dest.name})
    return jsonify({"error":"db file not found"}), 404

@admin_bp.route("/backups", methods=["GET"])
@login_required
def list_backups():
    BACKUP_DIR.mkdir(exist_ok=True)
    files = [p.name for p in BACKUP_DIR.iterdir() if p.is_file()]
    return jsonify({"backups": files})

@admin_bp.route("/restore", methods=["POST"])
@login_required
def restore():
    data = request.get_json() or {}
    fname = data.get("filename")
    if not fname:
        return jsonify({"error":"filename required"}), 400
    src = BACKUP_DIR / fname
    if src.exists():
        shutil.copy(src, DB_FILE)
        return jsonify({"message":"restored"})
    return jsonify({"error":"backup not found"}), 404
