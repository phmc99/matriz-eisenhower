import sqlalchemy
from app.models.category import Category
from app.models.eisenhower import Eisenhower
from app.models.exc import UrgencyImportanceError
from app.models.task import Task
from app.models.task_category import task_category
from flask import request, current_app
from app.configs.database import db

def get_all():
    query = db.session.query(Category, Task).select_from(Category).join(task_category).join(Task).all()
    result = []
    aux = []

    for i in range(len(query)):
        category = {
            "id": query[i][0].id,
            "name": query[i][0].name,
            "description": query[i][0].description,
            "tasks": []
        }
        if not category["name"] in aux:
            aux.append(category["name"])
            result.append(category)
        

    for i in range(len(query)):
        item_id = query[i][0].id
        category = list(filter(lambda item: item["id"] == item_id, result))
        task = {
            "id": query[i][1].id,
            "name": query[i][1].name,
            "description": query[i][1].description,
            "priority": query[i][1].eisenhower.type
        }
        category[0]["tasks"].append(task)

    return {"data": result}, 200