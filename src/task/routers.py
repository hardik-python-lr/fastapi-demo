from fastapi_crudrouter import SQLAlchemyCRUDRouter
from src.task.schemas import (
    TaskBaseSchema,
    TaskCreatePayloadSchema,
    TaskUpdatePayloadSchema,
    TaskResponseSchema,
    MessageSchema,
)
from database import get_db
from src.task.models import Task
from fastapi import Depends
from sqlalchemy.orm import Session
from typing import List
from src.task.services import get_task_by_id
from src.user.services import get_user_by_id
from src.user.models import User

# Create the router using SQLAlchemyCRUDRouter from fastapi_crudrouter
router = SQLAlchemyCRUDRouter(
    schema=TaskBaseSchema,
    create_schema=TaskCreatePayloadSchema,
    update_schema=TaskUpdatePayloadSchema,
    db_model=Task,
    db=get_db,
    get_all_route=False,
    get_one_route=False,
    create_route=False,
    update_route=False,
    delete_one_route=True,
    delete_all_route=True,
    tags=["Task"],
    prefix="/tasks",
)


@router.get("", response_model=List[TaskResponseSchema])
def get_tasks(db: Session = Depends(get_db)):
    """Retrieve all tasks from the database.

    Args:
        db (Session, optional): Database session object. Defaults to Depends(get_db).

    Returns:
        List of TaskResponseSchema: List of task objects.
    """

    # Get all Task records from the database
    all_tasks = db.query(Task).all()

    # Iterate through all tasks and return them based on the response schema
    return [TaskResponseSchema(**(vars(task))) for task in all_tasks]


@router.post("", response_model=TaskResponseSchema)
def create_task(payload: TaskCreatePayloadSchema, db: Session = Depends(get_db)):
    """Create a new task.

    Args:
        payload (TaskCreatePayloadSchema): Task details needed to create a new task record.
        db (Session, optional): Database session object. Defaults to Depends(get_db).

    Returns:
        TaskResponseSchema: Newly created task object.
    """
    user = get_user_by_id(user_id=payload.assign_to, db=db)

    new_task = Task(
        title=payload.title,
        category=payload.category,
        assign_to=user.id if user else None,
    )

    # Add the task object to the database
    db.add(new_task)
    # Commit the changes to the database
    db.commit()

    # Return the task object based on the response schema
    return TaskResponseSchema.from_orm(new_task)


@router.patch("/{task_id}", response_model=TaskResponseSchema)
def update_task(
    task_id: int, payload: TaskUpdatePayloadSchema, db: Session = Depends(get_db)
):
    """Update a task object.

    Args:
        task_id (int): ID of the task to update.
        payload (TaskUpdatePayloadSchema): Data to update the task with.
        db (Session, optional): Database session object. Defaults to Depends(get_db).

    Returns:
        TaskResponseSchema: Updated task object.
    """
    print(payload.assign_to)
    # Get the task object based on the provided task_id
    task = get_task_by_id(task_id=task_id, db=db)
    user = get_user_by_id(user_id=payload.assign_to, db=db)

    if task:
        # Convert the payload to a dictionary and exclude unset values
        update_data = payload.dict(exclude_unset=True)

        # Iterate through the dictionary items
        for field, value in update_data.items():
            # Update the fields in the task object
            setattr(task, field, value)

        # Add the updated task object to the database
        db.add(task)
        # Commit the changes to the database
        db.commit()
        # Refresh and reflect the changes
        db.refresh(task)

        # Return the updated task object based on the response schema
        return TaskResponseSchema.from_orm(task)

    # Return an error message if the task_id doesn't exist in the database
    return MessageSchema(message=f"task_id: {task_id} does not exist in the database")
