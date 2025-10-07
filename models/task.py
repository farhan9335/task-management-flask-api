from db import db

class TaskModel(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80),unique = True,nullable=False)
    description = db.Column(db.Text,nullable=True)
    status = db.Column(db.String(12),nullable = False)
    due_date = db.Column(db.DateTime,nullable = False)
    assigned_to = db.Column(db.String(80),nullable = False)