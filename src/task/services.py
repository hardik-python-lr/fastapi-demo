from database import get_db
from fastapi import Depends
from sqlalchemy.orm import Session
from src.task.models import Task
from fastapi.exceptions import HTTPException


def get_task_by_id(task_id: int, db: Session = Depends(get_db)):
    """Get task based on task id

    Args:
        task_id (int): task id, which want to get.
        db (Session, optional): Database session object. Defaults to Depends(get_db).

    Raises:
        HTTPException: Raise Exception, if id not exist in database.

    Returns:
        Task object: return task obj.
    """
    task = db.query(Task).get(task_id)
    if not task:
        raise HTTPException(
            status_code=400, detail=f"Task id: {task_id} not exist in database"
        )

    return task
