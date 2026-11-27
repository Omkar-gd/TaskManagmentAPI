from sqlalchemy import Column, Integer, String, Date, DateTime
from datetime import datetime

from app.database import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    priority = Column(String, default="Medium")
    status = Column(String, default="Pending")
    assigned_to = Column(String, nullable=True)
    due_date = Column(Date, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    