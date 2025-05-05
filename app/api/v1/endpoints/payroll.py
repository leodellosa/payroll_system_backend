from fastapi import APIRouter, UploadFile, File
from typing import List, Optional
from fastapi import Query, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_session
from app.schemas.payroll import PayrollSchema, PayrollResponse,PayrollCreate,PayrollUpdate
from fastapi import status
from app.services.payroll_service import(
    get_all_payrolls,
    generate_payroll,
    update_payroll,
    delete_payroll,
    get_payroll_summary,
    generate_payslip_pdf,
    generate_payslip_excel,
    batch_upload_payroll,
    download_payroll_template
)
    
router = APIRouter()

@router.get("/", response_model=List[PayrollResponse])
def read_users(db: Session = Depends(get_session)):
    return get_all_payrolls(db)

@router.post("/generate", response_model=PayrollResponse,status_code=status.HTTP_201_CREATED)
def create_payroll(
    employee_id: int,
    payroll_data: PayrollCreate,
    db: Session = Depends(get_session)
):
    result = generate_payroll(db, payroll_data, employee_id)
    if not result["success"]:
        raise HTTPException(status_code=result.get("code", 400), detail=result["error"])
    return result["payroll"]

@router.put("/update", response_model=PayrollResponse)
def update_payroll_data(
    payroll_id: int,
    payroll_data: PayrollUpdate,
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

@router.get("/payslip/pdf", response_model=dict)
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
    result = generate_payslip_excel(db, employee_id)
    if not result["success"]:
        raise HTTPException(status_code=result.get("code", 400), detail=result["error"])
    
    return result

@router.post("/batch-upload", response_model=dict)
async def batch_upload_payroll_data(
    excel_file: UploadFile = File(...),
    db: Session = Depends(get_session)
):
    result = await batch_upload_payroll(db, excel_file)
    if not result["success"]:
        raise HTTPException(status_code=result.get("code", 400), detail=result["error"])
    
    return result

""" In postman
    Go to the Body tab
    Select form-data.
    Add the Excel file field
    Under Key, type: excel_file (same name as in your function).
    Set the type to File using the dropdown.
    Upload your .xlsx file in the Value column."""

@router.get("/download-template")
def download_template():
    try:
        return download_payroll_template()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate template: {str(e)}")
    
"""
    Open Postman
    Look in the response panel
    The response will show up as a binary file (.xlsx content).
    In the bottom right corner of the response tab, Postman will show a “Save Response” button (icon).
    Click it → Choose “Save to a file” → name it payroll_template.xlsx.
"""
