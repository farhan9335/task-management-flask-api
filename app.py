import os
from redis_config import redis_client
from datetime import timedelta
from flask import Flask
from flask_migrate import Migrate
from flask_smorest import Api
from flask_jwt_extended import JWTManager

from db import db
from resources.task import blp as TaskBlueprint
from resources.user import blp as UserBlueprint
from resources.login import blp as LoginBlueprint


def create_app(db_url=None):
    app = Flask(__name__)
   
    # === JWT Configuration ===
    app.config["JWT_SECRET_KEY"] = "FARHAN"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=30)
    app.config["PROPAGATE_EXCEPTIONS"] = True
    jwt = JWTManager(app)

    @jwt.token_in_blocklist_loader
    def check_token_in_blocklist_loader(jwt_header,jwt_payload):
        jti = jwt_payload["jti"]
        return redis_client.get(f"bl:{jti}") is not None

    # === API Documentation ===
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    # === Database Configuration ===
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    Migrate(app, db)

    # === Import Models ===
    import models  # Ensure models are registered after db.init_app

    # === Register Blueprints ===
    api = Api(app)
    api.register_blueprint(TaskBlueprint)
    api.register_blueprint(UserBlueprint)
    api.register_blueprint(LoginBlueprint)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
