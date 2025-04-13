from fastapi import APIRouter
from typing import List, Optional
from fastapi import Query, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_session
from app.schemas.employee import EmployeeBase
from app.services.employee_service import get_all_employees, get_filtered_employees, create_employee, update_employee, update_employee_status


router = APIRouter()

@router.get("/", response_model=List[EmployeeBase])
def read_users(db: Session = Depends(get_session)):
    return get_all_employees(db)

@router.get("/employeeList", response_model=List[EmployeeBase])
async def employee_list(
    search: Optional[str] = Query(None),
    hire_date_from: Optional[str] = Query(None),
    hire_date_to: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    db: Session = Depends(get_session)
):
    try:
        return get_filtered_employees(
            db=db,
            search=search,
            hire_date_from=hire_date_from,
            hire_date_to=hire_date_to,
            status=status,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    
@router.post("/employee/add",  response_model=EmployeeBase)
async def add_employee_submit(
    employee: EmployeeBase, 
    db: Session = Depends(get_session)
):
    result = create_employee(
        db=db,
        employee_data=employee,
    )

    if result["success"]:
        return result["employee"]
    else:
        raise HTTPException(status_code=400, detail=result["error"])
    
@router.put("/employee/edit/{employee_id}", response_model=EmployeeBase, tags=["Employees"])
async def edit_employee_submit(
    employee_id: int,
    updated_employee: EmployeeBase,
    db: Session = Depends(get_session),
):
    result = update_employee(db, employee_id, updated_employee)
    if not result["success"]:
        raise HTTPException(status_code=result.get("code", 400), detail=result["error"])
    return result["employee"]

@router.put("/employee/status/{employee_id}", response_model=EmployeeBase, tags=["Employees"])
async def edit_employee_status(
    employee_id: int,
    status: str,
    db: Session = Depends(get_session),
):
    result = update_employee_status(db, employee_id, status)
    if not result["success"]:
        raise HTTPException(status_code=result.get("code", 400), detail=result["error"])
    return result["employee"]
