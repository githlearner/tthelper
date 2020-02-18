import uuid
import datetime
from main import db, bcrypt
from flask_jwt_extended import (
    JWTManager,
    jwt_required,
    create_access_token,
    get_jwt_identity,
)

from models import User


class UserController:
    def create_new_user(self, data):
        user = User.query.filter_by(email=data["email"]).first()
        if not user:
            new_user = User(
                username=data["username"],
                email=data["email"],
                password=data["password"],
                public_id=str(uuid.uuid4()),
                admin=data["admin"],
            )

            self.add_to_db(new_user)
            response_object = {
                "status": "success",
                "message": "user successfully created",
            }
            return response_object, 201
        else:
            response_object = {"status": "failed", "message": "user already exists"}
            return response_object, 201

    def get_all_users(self):
        users = User.query.all()
        user_res = []
        for user in users:
            user_dict = dict()
            user_dict["username"] = user.username
            user_dict["email"] = user.email
            user_dict["public_id"] = user.public_id
            user_dict["admin"] = user.admin
            user_dict["date"] = str(user.added_on)
            user_res.append(user_dict)
        response_object = {"result": user_res}
        return response_object, 200

    def isadmin(self, data):
        user = User.query.filter_by(username=data).first()
        return True if user.admin else False

    def promoteadmin(self, data):
        user = User.query.filter_by(username=data).first()
        print(user)
        if user:
            user.admin = True
            db.session.commit()
            return {"message": "User promoted as admin"}, 200
        else:
            return {"message": "Invalid Username"}, 401

    def add_to_db(self, data):
        db.session.add(data)
        db.session.commit()


class LoginController:
    def login_api(self, data):
        user = User.query.filter_by(username=data["username"]).first()
        if not user:
            response_object = {"message": "Invalid Username"}
            return response_object, 401

        else:
            res = bcrypt.check_password_hash(user.password_hash, data["password"])
            if res:
                access_token = create_access_token(identity=user.username)
                response_object = {"access_token": access_token}
                return response_object, 201
            else:
                response_object = {"message": "Invalid Password"}
                return response_object, 401

    def change_password(self, data):
        user = User.query.filter_by(email=data["email"]).first()
        if not user:
            return {"message": "Invalid Username"}, 403
        elif bcrypt.check_password_hash(user.password_hash, data["new_password"]):
            return {"message": "Please choose a different password"}, 403
        else:
            user.password_hash = bcrypt.generate_password_hash(
                data["new_password"]
            ).decode("UTF-8")
            db.session.commit()
            return {"message": "Password Updated Successfully"}, 201
