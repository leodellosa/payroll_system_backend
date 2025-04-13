from typing import List, Optional
from app.models.employee import Employee
from app.schemas.employee import EmployeeBase
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy.inspection import inspect

def get_all_employees(db: Session) -> List[EmployeeBase]:
    employees = db.query(Employee).all()
    return [
        EmployeeBase(**{c.key: getattr(employee, c.key) for c in inspect(Employee).mapper.column_attrs})
        for employee in employees
    ]

def get_filtered_employees(
    db: Session,
    search: Optional[str] = None,
    hire_date_from: Optional[str] = None,
    hire_date_to: Optional[str] = None,
    status: Optional[str] = None,
) -> List[EmployeeBase]:
    
    query = db.query(Employee)

    if search:
        query = query.filter(
            Employee.first_name.ilike(f"%{search}%") |
            Employee.last_name.ilike(f"%{search}%")
        )

    if hire_date_from:
        query = query.filter(Employee.hire_date >= hire_date_from)

    if hire_date_to:
        query = query.filter(Employee.hire_date <= hire_date_to)

    if status:
        query = query.filter(Employee.status == status)

    employees = query.all()
    if not employees:
        return []
    
    return [
        EmployeeBase(**{c.key: getattr(employee, c.key) for c in inspect(Employee).mapper.column_attrs})
        for employee in employees
    ]


def create_employee(db: Session, employee_data: EmployeeBase) -> dict:
    try:
        new_employee = Employee(**employee_data.model_dump())
        db.add(new_employee)
        db.commit()
        db.refresh(new_employee)
        return {"success": True, "employee": new_employee}
    except IntegrityError as e:
        db.rollback()
        return {"success": False, "error": "Email address already exists!"}
    except Exception as e:
        db.rollback()
        return {"success": False, "error": f"An error occurred: {str(e)}"}

def update_employee(db: Session, employee_id: int, employee_data: EmployeeBase) -> dict:
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        return {"success": False, "error": "Employee not found", "code": 404}
    try:
        update_data = employee_data.model_dump()
        for key, value in update_data.items():
            setattr(employee, key, value)

        db.commit()
        db.refresh(employee)
        return {"success": True, "employee": employee}
    except IntegrityError:
        db.rollback()
        return {"success": False, "error": "Email address already exists!", "code": 400}
    except Exception as e:
        db.rollback()
        return {"success": False, "error": f"An error occurred: {str(e)}", "code": 500}
    
def update_employee_status(db: Session,employee_id: int,status: str) -> dict:
    VALID_STATUSES = ["Active", "Inactive"]
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
         return {"success": False, "error": "Employee not found", "code": 404}

    if status and status not in VALID_STATUSES:
        return {"success": False, "error": f"Invalid status value: {status}. Allowed values are {VALID_STATUSES}", "code": 400}

    try:
        if status:
            employee.status = status
        else:
            employee.status = "Inactive" if employee.status == "Active" else "Active"

        db.commit()
        db.refresh(employee)

        return {"success": True, "employee": employee}
    except Exception as e:
        db.rollback()
        return {"success": False, "error": f"An error occurred: {str(e)}", "code": 500}