import sqlalchemy
from app.models.category import Category
from app.models.eisenhower import Eisenhower
from app.models.exc import UrgencyImportanceError
from app.models.task import Task
from app.models.task_category import Task_Category
from flask import request, current_app
from app.configs.database import db

def get_all():

    # Formar relacionamento Categorias -> a


    query = db.session.query(Category, Task).select_from(Category).join(Task_Category).join(Task).all()
    print(query)

    return {}