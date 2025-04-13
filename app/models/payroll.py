from app.db.session import Base
from sqlalchemy import Column, Integer, String, Float, DateTime, Date, ForeignKey, UniqueConstraint

class Payroll(Base):
    __tablename__ = "payroll"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employee.id"), nullable=False)
    time_in = Column(DateTime, nullable=False)
    time_out = Column(DateTime, nullable=False)
    total_hours_worked = Column(Float, nullable=False)
    deductions = Column(Float, nullable=False)
    subtotal = Column(Float, nullable=False)
    net_salary = Column(Float, nullable=False)
    deduction_remarks = Column(String, nullable=True)
    project = Column(String, nullable=True)
    overtime_pay = Column(Float, nullable=True)
    overtime_hour = Column(Float, nullable=True)
    night_differential_pay = Column(Float, nullable=True)
    night_differential_hour = Column(Float, nullable=True)
    allowance = Column(Float, nullable=True)
    date = Column(Date, nullable=False)
    created_at = Column(DateTime, nullable=False)

    __table_args__ = (
        UniqueConstraint('employee_id', 'date', name='unique_employee_date'),
    )