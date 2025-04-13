from fastapi import APIRouter
from app.api.v1.endpoints import employees, payroll

api_router = APIRouter()
api_router.include_router(employees.router, prefix="/employees", tags=["Employees"])
api_router.include_router(payroll.router, prefix="/payroll", tags=["Payroll"])
