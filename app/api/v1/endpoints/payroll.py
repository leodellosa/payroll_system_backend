from fastapi import APIRouter
from typing import List, Optional
from fastapi import Query, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_session
from app.schemas.payroll import PayrollSchema
from fastapi import status
from app.services.payroll_service import(
    get_all_payrolls,
    generate_payroll,
    update_payroll,
    delete_payroll,
    get_payroll_summary,
    generate_payslip_pdf,
    generate_payslip_excel
)
    

router = APIRouter()

@router.get("/", response_model=List[PayrollSchema])
def read_users(db: Session = Depends(get_session)):
    return get_all_payrolls(db)

@router.post("/generate", response_model=PayrollSchema,status_code=status.HTTP_201_CREATED)
def create_payroll(
    employee_id: int,
    payroll_data: PayrollSchema,
    db: Session = Depends(get_session)
):
    result = generate_payroll(db, payroll_data, employee_id)
    if not result["success"]:
        raise HTTPException(status_code=result.get("code", 400), detail=result["error"])
    return result["payroll"]

@router.put("/update", response_model=PayrollSchema)
def update_payroll_data(
    payroll_id: int,
    payroll_data: PayrollSchema,
    db: Session = Depends(get_session)
):
    result = update_payroll(db,payroll_id, payroll_data)
    if not result["success"]:
        raise HTTPException(status_code=result.get("code", 400), detail=result["error"])
    
    return result["payroll"]

@router.delete("/delete", response_model=dict)
def delete_payroll_data(
    payroll_id: int,
    db: Session = Depends(get_session)
):
    result = delete_payroll(db, payroll_id)
    if not result["success"]:
        raise HTTPException(status_code=result.get("code", 400), detail=result["error"])
    
    return result

@router.get("/summary", response_model=dict)
def generate_payroll_summary(
    employee_id: int,
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    db: Session = Depends(get_session)
):
    result = get_payroll_summary(db, employee_id, start_date, end_date)
    if not result["success"]:
        raise HTTPException(status_code=result.get("code", 400), detail=result["error"])
    
    payrolls = result["payrolls"]
    total_hours_worked = sum(p.total_hours_worked or 0 for p in payrolls)
    overtime_pay = sum(p.overtime_pay or 0 for p in payrolls)
    night_differential_pay = sum(p.night_differential_pay or 0 for p in payrolls)
    deductions = sum(p.deductions or 0 for p in payrolls)
    allowance = sum(p.allowance or 0 for p in payrolls)
    net_salary = sum(p.net_salary or 0 for p in payrolls)

    return {
        "payrolls": payrolls,
        "totals": {
            "total_hours_worked": total_hours_worked,
            "overtime_pay": overtime_pay,
            "night_differential_pay": night_differential_pay,
            "deductions": deductions,
            "allowance": allowance,
            "net_salary": net_salary,
        }
    }

@router.get("/payslip", response_model=dict)
def generate_payslip(
    employee_id: int,
    db: Session = Depends(get_session)
):
    result = generate_payslip_pdf(employee_id, db)
    if not result["success"]:
        raise HTTPException(status_code=result.get("code", 400), detail=result["error"])
    
    return result

@router.get("/payslip/excel", response_model=dict)
def generate_payslip_excel_file(
    employee_id: int,
    db: Session = Depends(get_session)
):
    return generate_payslip_excel(db, employee_id)