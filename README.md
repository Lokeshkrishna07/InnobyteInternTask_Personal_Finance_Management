# Personal Finance Tracker

## Quick start

1. Create a virtual env:
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # or .\venv\Scripts\Activate on Windows PowerShell
   pip install -r requirements.txt
   ```

2. Set env vars (backend/.env provided). Update SECRET_KEY and DATABASE_URL if needed.

3. Initialize DB and migrations:
   ```bash
   export FLASK_APP=run.py
   flask db init
   flask db migrate -m "Initial"
   flask db upgrade
   ```

4. Run:
   ```bash
   python run.py
   ```

Open http://127.0.0.1:5000/ to see the minimal frontend.

## Additional UI
- /reports -> Financial reports (monthly & range)
- /budgets -> Set and check budgets
- /backup -> Create and restore backups (requires login)

## Admin API
- POST /api/admin/backup -> create backup
- GET /api/admin/backups -> list backups
- POST /api/admin/restore {filename} -> restore

