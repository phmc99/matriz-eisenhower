from sqlalchemy.orm import backref, relationship, validates
from app.configs.database import db
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from dataclasses import dataclass

from app.models.eisenhower import Eisenhower


@dataclass
class Task(db.Model):
    id: int
    name: str
    description: str
    duration: int
    importance: int
    urgency: int
    eisenhower: Eisenhower

    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=False)
    duration = Column(Integer, nullable=False)
    importance = Column(Integer, nullable=False)
    urgency = Column(Integer, nullable=False)
    eisenhower_id = Column(Integer, ForeignKey(
        "eisenhowers.id"), nullable=False)
    
    eisenhower = relationship(
        "Eisenhower", backref=backref("eisenhower", uselist=False))