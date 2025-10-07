from db import db
import logging
from flask_smorest import Blueprint,abort
from flask.views import MethodView
from schemas import TaskSchema,TaskUpdateSchema
from models import TaskModel
from flask_jwt_extended import jwt_required,get_jwt
from sqlalchemy.exc import SQLAlchemyError

blp = Blueprint("tasks","Tasks",description="Operations on tasks")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@blp.route("/task/<string:task_id>")
class Task(MethodView):
    @blp.response(200,TaskSchema)
    def get(self,task_id):
        task = TaskModel.query.get_or_404(task_id)
        return task
    
    @jwt_required()
    def delete(self,task_id):
        claims = get_jwt()
        if claims["role"] != "admin":
            abort(403,message="Only admin user can delete the task")
        task = TaskModel.query.get_or_404(task_id)
        if task:
            try:
                db.session.delete(task)
                db.session.commit()
            except SQLAlchemyError as e:
                logging.error(f"Exception occuured while deleting task : {e}")
                abort(500,message = "Exception occuured while deleting task")
        return {"message":f"Task successfully Deleted with Task Id {task.id}"},200
    
    @jwt_required()
    @blp.arguments(TaskUpdateSchema)
    @blp.response(200,TaskSchema)
    def put(self,task_data,task_id):
        claims = get_jwt()
        if claims["role"] != "admin":
            abort(403,message="only admin user can update the task")
        task = TaskModel.query.get_or_404(task_id)
        logger.info(f"Updating Task ID {task_id} with data: {task_data}")
        for key,value in task_data.items():
            setattr(task,key,value)
            logger.debug(f"Set {key} to {value}")
        db.session.commit()
        logger.info(f"Task ID {task_id} updated successfully.")
        return task    


@blp.route("/task")
class TaskList(MethodView):
    
    @blp.response(200,TaskSchema(many=True))
    def get(self):
        logging.info("Fetching all tasks")
        tasks = TaskModel.query.all()
        logging.info(f"Reterived {len(tasks)} tasks")
        return tasks

    @jwt_required()
    @blp.arguments(TaskSchema)
    @blp.response(201,TaskSchema)
    def post(self,task_data):
        claims = get_jwt()
        if claims["role"] != "admin":
         abort(403, message="Only admin user can create tasks")
        existing_task = TaskModel.query.filter_by(name=task_data["name"]).first()
        if existing_task:
            abort(409,message="Task name already exists")
        task = TaskModel(**task_data)
        try:
            db.session.add(task)
            db.session.commit()
            logging.info(f"task created with ID: {task.id}")
        except SQLAlchemyError as e:
            logging.error(f"Error inserting task: {e}")
            abort(500,message="Exception occurred while inserting task data")
        return task
            

