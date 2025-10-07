import logging
from db import db
from flask_smorest import Blueprint,abort
from flask.views import MethodView
from schemas import UserSchema,UpdateUserSchema
from models import UserModel
from sqlalchemy.exc import SQLAlchemyError
from passlib.hash import pbkdf2_sha256

blp = Blueprint("users","Users",description="Operations on users")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@blp.route("/user/<int:user_id>")
class User(MethodView):
    
    @blp.response(200,UserSchema)
    def get(self,user_id):
        user = UserModel.query.get_or_404(user_id)
        return user

    @blp.arguments(UpdateUserSchema)
    @blp.response(200,UserSchema)
    def put(self,user_data,user_id):
        user = UserModel.query.get_or_404(user_id)
        logger.info(f"Updating User ID {user_id} with data: {user_data}")
        for key,value in user_data.items():
            setattr(user,key,value)
            logger.debug(f"Set {key} to {value}")
        db.session.commit()
        logger.info(f"Task ID {user_id} updated successfully.")
        return user

    def delete(self,user_id):
        user = UserModel.query.get_or_404(user_id)
        try:
            db.session.delete(user)
            db.session.commit()
        except SQLAlchemyError as e:
            logging.error(f"Exception occurred while deleting user: {e}")
            abort(500,message="Exception occurred while deleting user")
        return {"message":f"User Id {user.id} deleted successfully"}


@blp.route("/user")
class UserList(MethodView):
    
    @blp.response(200,UserSchema(many=True))
    def get(self):
        logging.info("Fetch all users")
        users = UserModel.query.all()
        logging.info(f"Reterived {len(users)} users")
        return users

    @blp.arguments(UserSchema)
    def post(self,user_data):
        if UserModel.query.filter(UserModel.username == user_data["username"]).first():
            abort(409,message="A user with that name already exists")
        user = UserModel(
            username = user_data["username"],
            password = pbkdf2_sha256.hash(user_data["password"]),
            **{ "role": user_data["role"] } if "role" in user_data else {}
        )    
        try:
            db.session.add(user)
            db.session.commit()
            logging.info(f"user saved successfully")
        except SQLAlchemyError as e:
            logging.info(f"Exception occured while saving user: {e}")
            abort(500,message="Exception occurred while saving data")
        return {"message":"User created successfully"},201