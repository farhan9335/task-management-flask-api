import logging
from datetime import datetime
from db import db
from flask_smorest import Blueprint,abort
from redis_config import redis_client
from flask.views import MethodView
from schemas import LoginSchema
from passlib.hash import pbkdf2_sha256
from models import UserModel
from flask_jwt_extended import create_access_token,create_refresh_token,jwt_required,get_jwt,get_jwt_identity
from blocklist import BLOCKLIST

blp = Blueprint("login","Login",description="Login, Logout and refresh operations")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@blp.route("/login")
class UserLogin(MethodView):
    
    @blp.arguments(LoginSchema)
    def post(self,user_data):
        user = UserModel.query.filter(UserModel.username == user_data["username"]).first()
        if user and pbkdf2_sha256.verify(user_data["password"],user.password):
            access_token = create_access_token(
                identity=str(user.id),
                additional_claims={"role":user.role},
                fresh = True
            )
            refresh_token = create_refresh_token(
                identity=str(user.id),
                additional_claims={"role":user.role}
            )
            return {"access_token":access_token,"refresh_token":refresh_token},200
        logger.warning(f"Failed login attempt for username: {user_data['username']}")
        abort(401,message="Invalid credentials")

@blp.route("/logout")
class UserLogout(MethodView):
    
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        exp = get_jwt()["exp"]
        ttl = exp - int(datetime.utcnow().timestamp())
        redis_client.setex(f"bl:{jti}", ttl, "revoked")
        return {"message": "Successfully logged out."}, 200

@blp.route("/refresh")
class RefreshToken(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        claims = get_jwt()
        role = claims.get("role")
        new_token = create_access_token(identity=current_user,fresh=False,additional_claims={"role": role})
        return {"access_token":new_token},200


