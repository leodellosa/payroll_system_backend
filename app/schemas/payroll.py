from pydantic import BaseModel, ValidationError, model_validator
from typing import Optional
from decimal import Decimal
from datetime import datetime

class PayrollSchema(BaseModel):
    id: Optional[int] = None

class PayrollCreate(PayrollSchema):
    employee_id: int
    time_in: datetime
    time_out: datetime
    total_hours_worked: Optional[Decimal] = None
    overtime_hour: Optional[Decimal] = None
    overtime_pay: Optional[Decimal] = None
    night_differential_hour: Optional[Decimal] = None
    night_differential_pay: Optional[Decimal] = None 
    deductions: Optional[Decimal] = None
    allowance: Optional[Decimal] = None 
    subtotal: Optional[Decimal] = None
    net_salary: Optional[Decimal] = None
    deduction_remarks: Optional[str] = None
    project: Optional[str] = None
    date: Optional[datetime] = None
    created_at: Optional[datetime] = datetime.now()

    @model_validator(mode="after")
    def validate_payroll(cls, values):
        """
        Custom validation logic for payroll data.
        """
        time_in = values.time_in
        time_out = values.time_out
        total_hours_worked = values.total_hours_worked
        overtime_hour = values.overtime_hour or Decimal(0)
        deductions = values.deductions or Decimal(0)
        subtotal = values.subtotal

        if time_in and not values.date:
            values.date = time_in.date()

        # Ensure time_in is before time_out
        if time_in >= time_out:
            raise ValueError("Time in must be earlier than time out.")

        # Calculate total hours worked if not provided
        if not total_hours_worked:
            total_hours_worked = Decimal((time_out - time_in).total_seconds() / 3600)
            values.total_hours_worked = total_hours_worked

        # Validate overtime hours
        if total_hours_worked <= 10 and overtime_hour > 0:
            raise ValueError("Overtime cannot be recorded if total hours worked is less than 10.")
        if overtime_hour > 0 and (total_hours_worked - overtime_hour) < 10:
            raise ValueError("Overtime hours cannot exceed total hours worked.")

        # Validate deductions
        if subtotal is not None and deductions > subtotal:
            raise ValueError("Deductions cannot exceed the gross salary.")

        # Calculate net salary
        if subtotal is not None:
            values.net_salary = subtotal - deductions

        return values
    
class PayrollUpdate(PayrollSchema):
    employee_id: Optional[int] = None
    time_in: Optional[datetime] = None
    time_out: Optional[datetime] = None
    total_hours_worked: Optional[Decimal] = None
    overtime_hour: Optional[Decimal] = None
    overtime_pay: Optional[Decimal] = None
    night_differential_hour: Optional[Decimal] = None
    night_differential_pay: Optional[Decimal] = None 
    deductions: Optional[Decimal] = None
    allowance: Optional[Decimal] = None 
    subtotal: Optional[Decimal] = None
    net_salary: Optional[Decimal] = None
    deduction_remarks: Optional[str] = None
    project: Optional[str] = None
    date: Optional[datetime] = None

    @model_validator(mode="after")
    def validate_payroll(cls, values):
        """
        Custom validation logic for payroll data.
        """
        time_in = values.time_in
        time_out = values.time_out
        total_hours_worked = values.total_hours_worked
        overtime_hour = values.overtime_hour or Decimal(0)
        deductions = values.deductions or Decimal(0)
        subtotal = values.subtotal

        if time_in and not values.date:
            values.date = time_in.date()

        # Ensure time_in is before time_out
        if time_in >= time_out:
            raise ValueError("Time in must be earlier than time out.")

        # Calculate total hours worked if not provided
        if not total_hours_worked:
            total_hours_worked = Decimal((time_out - time_in).total_seconds() / 3600)
            values.total_hours_worked = total_hours_worked

        # Validate overtime hours
        if total_hours_worked <= 10 and overtime_hour > 0:
            raise ValueError("Overtime cannot be recorded if total hours worked is less than 10.")
        if overtime_hour > 0 and (total_hours_worked - overtime_hour) < 10:
            raise ValueError("Overtime hours cannot exceed total hours worked.")

        # Validate deductions
        if subtotal is not None and deductions > subtotal:
            raise ValueError("Deductions cannot exceed the gross salary.")

        # Calculate net salary
        if subtotal is not None:
            values.net_salary = subtotal - deductions

        return values
    
class PayrollResponse(PayrollSchema):
    employee_id: int
    time_in: datetime
    time_out: datetime
    total_hours_worked: Optional[Decimal] = None
    overtime_hour: Optional[Decimal] = None
    overtime_pay: Optional[Decimal] = None
    night_differential_hour: Optional[Decimal] = None
    night_differential_pay: Optional[Decimal] = None 
    deductions: Optional[Decimal] = None
    allowance: Optional[Decimal] = None 
    subtotal: Optional[Decimal] = None
    net_salary: Optional[Decimal] = None
    deduction_remarks: Optional[str] = None
    project: Optional[str] = None
    date: Optional[datetime] = None
    created_at: Optional[datetime] = None