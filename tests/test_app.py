import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from app import create_app
from app.database import db as _db
from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False

@pytest.fixture
def app():
    app = create_app(TestConfig)
    with app.app_context():
        _db.create_all()
        yield app
        _db.session.remove()
        _db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_register_login_logout(client):
    res = client.post("/api/auth/register", json={"username":"testuser","password":"pass"})
    assert res.status_code == 201
    res = client.post("/api/auth/login", json={"username":"testuser","password":"pass"})
    assert res.status_code == 200

def test_budget_and_reports(client, app):
    # register & login
    client.post("/api/auth/register", json={"username":"u2","password":"pass"})
    client.post("/api/auth/login", json={"username":"u2","password":"pass"})
    # create category
    r = client.post("/api/categories/", json={"name":"Food","type":"expense"})
    assert r.status_code == 201
    cid = r.get_json()["id"]
    # set budget
    r = client.post("/api/budgets/", json={"category_id": cid, "month": 8, "year": 2025, "limit_amount": 50})
    assert r.status_code == 201
    bid = r.get_json()["id"]
    # create transaction under budget
    r = client.post("/api/transactions/", json={"amount": 60, "category_id": cid, "type": "expense", "date": "2025-08-05"})
    assert r.status_code == 201
    j = r.get_json()
    assert "budget" in j and j["budget"]["is_over"] == True
    # get monthly report
    r = client.get("/api/reports/monthly?month=8&year=2025")
    assert r.status_code == 200
    data = r.get_json()
    assert data["expense"] >= 60

def test_backup_restore(client, app):
    client.post("/api/auth/register", json={"username":"admin","password":"pass"})
    client.post("/api/auth/login", json={"username":"admin","password":"pass"})
    # create a backup (may return 404 if no db file yet, but should not 500)
    r = client.post("/api/admin/backup")
    assert r.status_code in (200, 404)
    r = client.get("/api/admin/backups")
    assert r.status_code == 200
