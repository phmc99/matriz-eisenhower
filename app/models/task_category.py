from sqlalchemy.orm import backref, relationship
from app.configs.database import db
from sqlalchemy import Column, Integer, ForeignKey
from dataclasses import dataclass

from app.models.task import Task
from app.models.category import Category


@dataclass
class Task_Category(db.Model):
    id: int
    task: Task
    category: Category

    __tablename__ = "task_categories"

    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey(
        "tasks.id"), nullable=False)
    category_id = Column(Integer, ForeignKey(
    "categories.id"), nullable=False)

    task = relationship(
        "Task", backref=backref("task", uselist=False))
    category = relationship(
        "Category", backref=backref("category", uselist=False))
