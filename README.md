# FastAPI Payroll Management System

A backend API built using **FastAPI** to manage employees, generate payroll records, export payslips as PDF/Excel, and support batch payroll uploads from Excel files.

---

## Features

- Employee Management (Create, Read, Update, Delete)
- Payroll Calculation & Tracking
- Bulk Payroll Upload from Excel
- Export Payslip as PDF and Excel
- Static Assets (Company Logo, CSS)
- RESTful JSON API Responses
- Error Handling & Validation
- Search, Filter, and Query Support

---

## Tech Stack

- **FastAPI** – High-performance web framework
- **SQLAlchemy** – ORM for interacting with the database
- **Pydantic** – Request/Response validation
- **WeasyPrint** – PDF generation from HTML/CSS
- **OpenPyXL** – Excel file generation and parsing
- **Uvicorn** – ASGI server

---

##  Project Structure
app/ 
├── api/ # Routers and endpoint logic 
├── core/ # Configuration (DB, settings)
├── db/ # DB sttings
├── models/ # SQLAlchemy models 
├── schemas/ # Pydantic schemas 
├── services/ # Business logic (CRUD, PDF, Excel) 
├── static/ # Static files
    ├── css/ 
    ├── images/ 
├── templates/ # HTML for PDF generation 


## Instructions

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

git clone https://github.com/leodellosa/payroll_system_backend.git "fast_api"
cd fast_api
python -m venv .venv
source .venv/scripts/activate
pip install -r requirements.txt
py run.py

    
