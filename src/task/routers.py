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
    prefix="",
)


@router.get(
    "/all-tasks", response_model=List[TaskResponseSchema]
)  # response_model: how looks response
def get_tasks(db: Session = Depends(get_db)):
    """Retrieve all tasks from the database.

    Returns:
        Pydantic Schema: return List of TaskResponseSchema object.
    """

    # Get all Task record query
    tasks = db.query(Task).all()

    # Itrate all tasks object and return based on respective response schema's object
    lst_tasks = [TaskResponseSchema(**(vars(task))) for task in tasks]

    return lst_tasks


@router.post("/create-task", response_model=TaskResponseSchema)
def create_task(payload: TaskCreatePayloadSchema, db: Session = Depends(get_db)):
    """Create new task

    Args:
        payload (TaskCreatePayloadSchema): Task details, which need for create task record.
        db (Session, optional): Database session object. Defaults to Depends(get_db).

    Returns:
        Pydantic Schema: Return TaskResponseSchema object.
    """
    user = get_user_by_id(user_id=payload.asign_to, db=db)
    print(user)

    task = Task(
        title=payload.title,
        category=payload.category,
        asign_to=user.id if user else None,
    )
    # else:
    #     task = Task(title=payload.title, category=payload.category)

    # add task obj in database
    db.add(task)
    # commit changes
    db.commit()

    # return task object based on respective schema
    return TaskResponseSchema.from_orm(task)


@router.patch("/update-task", response_model=TaskResponseSchema)
def update_task(
    task_id: int, payload: TaskUpdatePayloadSchema, db: Session = Depends(get_db)
):
    """Update task object

    Args:
        task_id (int): task_id which need to update.
        payload (TaskUpdatePayloadSchema): Data which need to update.
        db (Session, optional): Database session object. Defaults to Depends(get_db).

    Returns:
        Pydantic schema: return updated record object
    """

    # return task object, which id pass
    task = get_task_by_id(task_id=task_id, db=db)
    user = get_user_by_id(user_id=payload.asign_to, db=db)
    if task:
        # convert into dict.
        update_data = payload.dict(exclude_unset=True)
        # ittrate dict items.
        for field, value in update_data.items():
            if value is not None:
                # update fields in to task object
                setattr(task, field, value)

        # add task obj in db
        db.add(task)
        # change commits
        db.commit()
        # refresh and reflact change
        db.refresh(task)

        # return task obj
        return TaskResponseSchema.from_orm(task)

    # return error message
    return MessageSchema(message=f"task_id: {task_id} not exist in database")
