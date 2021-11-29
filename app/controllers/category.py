import sqlalchemy
from app.models.category import Category
from flask import request, current_app


def create_category():
    try:
        data = request.get_json()

        new_category = Category(**data)
        current_app.db.session.add(new_category)
        current_app.db.session.commit()

        return {
            "id": new_category.id,
            "name": new_category.name,
            "description": new_category.description
        }, 201
    except sqlalchemy.exc.IntegrityError as e:
        return {"message": "category already exists"}

def update_category(category_id):
    data = request.get_json()

    category = Category.query.get(category_id)

    if category == None:
        return {"message": "category not found"}, 404

    for k, v in data.items():
        setattr(category, k, v)

    current_app.db.session.add(category)
    current_app.db.session.commit()

    return {
            "id": category.id,
            "name": category.name,
            "description": category.description
        }

def delete_category(category_id):
    category = Category.query.get(category_id)

    if category == None:
        return {"message": "category not found"}, 404

    current_app.db.session.delete(category)
    current_app.db.session.commit()

    return "", 204