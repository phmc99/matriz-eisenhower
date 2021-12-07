import sqlalchemy
from app.models.eisenhower import Eisenhower
from app.models.category import Category
from app.models.exc import UrgencyImportanceError
from app.models.task import Task
from flask import request, current_app


def eisenhower(i, u):
    if i == 1 and u == 1:
        eisenhower = (
            Eisenhower
            .query
            .filter(Eisenhower.type == "Do It First")
            .first()
        )
        return eisenhower.id

    if i == 1 and u == 2:
        eisenhower = (
            Eisenhower
            .query
            .filter(Eisenhower.type == "Delegate It")
            .first()
        )
        return eisenhower.id

    if i == 2 and u == 1:
        eisenhower = (
            Eisenhower
            .query
            .filter(Eisenhower.type == "Schedule It")
            .first()
        )
        return eisenhower.id

    if i == 2 and u == 2:
        eisenhower = (
            Eisenhower
            .query
            .filter(Eisenhower.type == "Delete It")
            .first()
        )
        return eisenhower.id

def create_task():
    session = current_app.db.session
    try:
        data = request.get_json()
        if data["importance"] > 2 or data["importance"] < 1:
            raise UrgencyImportanceError(data["importance"], data["urgency"])
        if data["urgency"] > 2 or data["urgency"] < 1:
            raise UrgencyImportanceError(data["importance"], data["urgency"])

        eisenhower_id = eisenhower(data["importance"], data["urgency"])
        data["eisenhower_id"] = eisenhower_id

        columns = ["name", "description", "duration", "importance", "urgency", "eisenhower_id"]
        valid_data = {k: data[k] for k in data if k in columns}
        new_task = Task(**valid_data)

        categories = []
        for c in data["categories"]:
            category = (
                Category
                .query
                .filter(Category.name == c["name"])
                .first()
            )

            if category == None:
                new_category = Category(**{
                    "name": c["name"],
                    "description": data["description"]
                    })
                session.add(new_category)
                session.commit()
                new_category.tasks.append(new_task)
                categories.append({"name": new_category.name})
            else:
                category.tasks.append(new_task)
                categories.append({"name": category.name})

        session.add(new_task)
        session.commit()

        return {
            "id": new_task.id,
            "name": new_task.name,
            "description": new_task.description,
            "duration": new_task.duration,
            "eisenhower": (Eisenhower.query.get(eisenhower_id).type),
            "category": categories
        }
    except sqlalchemy.exc.IntegrityError as e:
        return {"message": "task already exists"}, 409
    except UrgencyImportanceError as e:
        return {"message": e.message}, 409

def update_task(task_id):
    try:
        data = request.get_json()
        keys = data.keys()

        task = Task.query.get(task_id)

        if "importance" in keys and "urgency" in keys:
            eisenhower_id = eisenhower(data["importance"], data["urgency"])
            data["eisenhower_id"] = eisenhower_id
        elif "importance" in keys:
            eisenhower_id = eisenhower(data["importance"], task.urgency)
            data["eisenhower_id"] = eisenhower_id
        elif "urgency" in keys:
            eisenhower_id = eisenhower(task.importance, data["urgency"])
            data["eisenhower_id"] = eisenhower_id

        if task == None:
            return {"message": "task not found"}, 404

        for k, v in data.items():
            setattr(task, k, v)

        current_app.db.session.add(task)
        current_app.db.session.commit()

        return {
                "id": task.id,
                "name": task.name,
                "description": task.description,
                "duration": task.duration,
                "eisenhower": (Eisenhower.query.get(task.eisenhower_id).type)
            }
    except KeyError:
        return {"message": "key error"}, 400


def delete_task(task_id):
    task = Task.query.get(task_id)

    if task == None:
        return {"message": "task not found"}, 404

    current_app.db.session.delete(task)
    current_app.db.session.commit()

    return "", 204

