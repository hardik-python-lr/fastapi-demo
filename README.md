## Title:

Sample Fastapi application

## Description:

This project is sample CRUD APIs of User and Product. In this project use alembic for migrations, also create seprate folder for seprate model.

## Technologies

- Python 3.8.10
- Fastapi
- Alembic
- Sqlalchemy
- Sqlite
- Rest API

## Installation

```bash
pip3 install -r requirements.txt
```

## Alembic Migrations

1. Intialize directory

```bash
alembic init alembic
```

2. Create migtations

```bash
alembic revision --autogenerate -m "Initial Migration"
```

3. Apply migrations

```bash
alembic upgrade head
```

## Run application

```bash
uvicorn main:app --reload
```

### Example Modules

- User Module

  - Create, Read, Update, Delete users using User modules APIs.

- Task Modules

  - Create, Read, Update, Delete Task using Task modules APIs.
  - Maintain relationship between Task and User, so Each task assign to Specific user.
