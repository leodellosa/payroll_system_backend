from app.db.session import Base
from sqlalchemy import Column, Integer, String, Float, DateTime, Date, ForeignKey

class Employee(Base):
    __tablename__ = "employee" 

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    hire_date = Column(Date, nullable=False)
    position = Column(String(100), nullable=False)
    salary = Column(Float, nullable=False)
    status = Column(String(8), nullable=False, default="Active") 

    def __repr__(self):
        return f"<Employee(id={self.id}, first_name={self.first_name}, last_name={self.last_name})>"
    
