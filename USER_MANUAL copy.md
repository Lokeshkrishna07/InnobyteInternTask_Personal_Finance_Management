# 📘 **Personal Finance Tracker – User Manual**

A complete personal finance management system with budgeting, financial reports, and backup/restore capabilities.  
It includes a **Flask backend** and a **HTML frontend** for testing, with **Postman support** for API validation.

---

## **1. Project Overview**

This application helps users:
- Register, log in, and manage their transactions (income/expenses).
- Set monthly budgets per category.
- Generate monthly and yearly financial reports.
- Backup and restore their financial data.
- Test APIs with **Postman** or interact with the **HTML test UI**.

---

## **2. Installation Steps**

### **Backend Setup**
1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/personal_finance_tracker.git
   cd personal_finance_tracker/backend
   ```

2. **Create Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # For macOS/Linux
   venv\Scripts\activate      # For Windows
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Environment Variables**
   Create a `.env` file in `/backend`:
   ```env
   FLASK_APP=run.py
   FLASK_ENV=development
   SECRET_KEY=your_secret_key
   DATABASE_URL=sqlite:///finance.db
   ```

5. **Initialize the Database**
   ```bash
   flask db upgrade
   ```

6. **Run the Backend**
   ```bash
   flask run
   ```
   Backend runs at: **http://127.0.0.1:5000**

---

### **Frontend Setup (Minimal HTML Testing UI)**
1. Open `/frontend/index.html` in your browser.
2. Change `API_BASE_URL` in the HTML script section if needed (default: `http://127.0.0.1:5000`).

---

## **3. Usage Instructions**

### **API Testing with Postman**
- Import `postman_collection.json` from the repo.
- Set `{{base_url}}` variable to your backend address.
- Available API Endpoints:
  - **Auth**:
    - `POST /register`
    - `POST /login`
    - `POST /logout`
  - **Transactions**:
    - `POST /transactions`
    - `GET /transactions`
  - **Budgets**:
    - `POST /budgets`
    - `GET /budgets`
  - **Reports**:
    - `GET /reports/monthly`
    - `GET /reports/yearly`
  - **Backup/Restore**:
    - `GET /backup`
    - `POST /restore`

---

### **Example CLI Commands**
#### **Register**
```bash
curl -X POST http://127.0.0.1:5000/register -H "Content-Type: application/json" -d '{"username": "lokesh", "password": "pass123"}'
```

#### **Add Transaction**
```bash
curl -X POST http://127.0.0.1:5000/transactions -H "Authorization: Bearer <token>" -H "Content-Type: application/json" -d '{"type": "income", "amount": 5000, "category": "Salary"}'
```

#### **Get Monthly Report**
```bash
curl -X GET "http://127.0.0.1:5000/reports/monthly?month=8&year=2025" -H "Authorization: Bearer <token>"
```

---

## **4. Backup/Restore Guide**

### **Backup Data**
```bash
curl -X GET http://127.0.0.1:5000/backup -H "Authorization: Bearer <token>" -o backup.json
```
This creates a `backup.json` file with all your transactions and budget data.

### **Restore Data**
```bash
curl -X POST http://127.0.0.1:5000/restore -H "Authorization: Bearer <token>" -F "file=@backup.json"
```
This restores data from the backup.

---

## **5. Testing**
Run tests inside the backend folder:
```bash
pytest -v
```
Expected Output:
```
backend/tests/test_app.py::test_register_login_logout PASSED
backend/tests/test_app.py::test_budget_and_reports PASSED
backend/tests/test_app.py::test_backup_restore PASSED
```

---

## **6. Folder Structure**
```
personal_finance_tracker/
│
├── backend/
│   ├── app/
│   │   ├── routes/        # API routes
│   │   ├── models.py      # DB models
│   │   ├── __init__.py    # App factory
│   ├── tests/             # Unit tests
│   ├── requirements.txt
│   ├── run.py
│   └── .env
│
├── frontend/
│   └── index.html         # Minimal HTML UI
│
├── postman_collection.json
└── README.md
```
