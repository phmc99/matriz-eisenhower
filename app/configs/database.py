from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_app(app: Flask):
    db.init_app(app)
    app.db = db

    from app.models.category import Category
    from app.models.eisenhower import Eisenhower
    from app.models.task import Task
    from app.models.task_category import task_category