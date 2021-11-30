from app.configs.database import db

task_category = db.Table('task_category',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('task_id', db.Integer, db.ForeignKey('tasks.id')),
    db.Column('category_id', db.Integer, db.ForeignKey('categories.id'))
)