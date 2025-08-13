import shutil
from flask import current_app
from flask.cli import with_appcontext
import click
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
BACKUP_DIR = DATA_DIR / "backup"
DB_FILE = DATA_DIR / "finance_tracker.db"

@click.command("backup-db")
@with_appcontext
def backup_db():
    BACKUP_DIR.mkdir(exist_ok=True)
    dest = BACKUP_DIR / f"finance_tracker_backup_{int(__import__('time').time())}.db"
    if DB_FILE.exists():
        shutil.copy(DB_FILE, dest)
        click.echo(f"Backup saved to: {dest}")
    else:
        click.echo("Database file not found.")

@click.command("restore-db")
@click.argument("backup_file")
@with_appcontext
def restore_db(backup_file):
    src = BACKUP_DIR / backup_file
    if src.exists():
        shutil.copy(src, DB_FILE)
        click.echo("Database restored.")
    else:
        click.echo("Backup not found.")
