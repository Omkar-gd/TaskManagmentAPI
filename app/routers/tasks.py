
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Optional
from datetime import date

from app.database import get_db
from app.models import Task
from app.schemas import TaskCreate, TaskUpdate, TaskResponse

router = APIRouter(prefix="/tasks", tags=["Tasks"])

# 1. Create a new task
@router.post("", response_model=TaskResponse, status_code=201)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):

    new_task = Task(**task.model_dump())

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task

# 2. Get all tasks with filtering and searching
@router.get("", response_model=list[TaskResponse])
def get_tasks(
    status: Optional[str] = None,
    priority: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):

    query = db.query(Task)

    if status:
        query = query.filter(Task.status == status)

    if priority:
        query = query.filter(Task.priority == priority)

    if search:
        query = query.filter(Task.title.ilike(f"%{search}%"))

    return query.all()

# 3. Get overdue tasks
@router.get("/overdue", response_model=list[TaskResponse])
def get_overdue_tasks(db: Session = Depends(get_db)):

    return db.query(Task).filter(
        Task.due_date < date.today(),
        Task.status != "Completed"
    ).all()

# 4. Task summary
@router.get("/summary")
def task_summary(db: Session = Depends(get_db)):

    total = db.query(Task).count()

    pending = db.query(Task).filter(
        Task.status == "Pending"
    ).count()

    in_progress = db.query(Task).filter(
        Task.status == "In Progress"
    ).count()

    completed = db.query(Task).filter(
        Task.status == "Completed"
    ).count()

    overdue = db.query(Task).filter(
        Task.due_date < date.today(),
        Task.status != "Completed"
    ).count()

    return {
        "total_tasks": total,
        "pending": pending,
        "in_progress": in_progress,
        "completed": completed,
        "overdue": overdue
    }

# 5. Get task by ID
@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):

    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return task

# 6. Update task by ID
@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    updated_data: TaskUpdate,
    db: Session = Depends(get_db)
):

    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    data = updated_data.model_dump(exclude_unset=True)

    for field in ["title", "priority", "status"]:
        if field in data and data[field] is None:
            raise HTTPException(
                status_code=422,
                detail=f"{field} cannot be null"
            )

    for key, value in data.items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)

    return task

# 7. Delete task by ID
@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):

    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    db.delete(task)
    db.commit()

    return {"message": "Task deleted successfully"}