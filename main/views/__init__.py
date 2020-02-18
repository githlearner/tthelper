from manage import app

from flask_restplus import Api, Resource, fields

from flask import request, Blueprint

from flask_jwt_extended import (
    JWTManager,
    jwt_required,
    create_access_token,
    get_jwt_identity,
)

from .namespaces import api, user_ns, train_ns
from .request_body_models import api_login_model, api_model, admin_model, reset_password_model

from main.controller.controller_user import UserController, LoginController
from main.controller.controller_mongo import CustomMongoConnect

bp = Blueprint("/api", __name__)



@user_ns.route("/tcr")
class Users(Resource):
    @api.doc(description="<b>get all the users</b>", security="api-key")
    @jwt_required
    def get(self):
        current_username = get_jwt_identity()
        current_user_obj = UserController()
        if current_user_obj.isadmin(current_username):
            return UserController().get_all_users()
        else:
            return {"message": "Unauthorized"}, 401

    @api.doc(description="<b>Creates a New User</b>")
    @api.expect(api_model)
    def post(self):
        data = request.json
        res_message, res_code = UserController().create_new_user(data)
        return res_message, res_code

    @api.doc(description="<b>Promotes a user to admin</b>", security="api-key")
    @api.expect(admin_model)
    @jwt_required
    def put(self):
        data = request.json
        current_username = get_jwt_identity()
        user_obj = UserController()
        if user_obj.isadmin(current_username):
            if not user_obj.isadmin(data["username"]):
                res_message, res_code = user_obj.promoteadmin(data["username"])
                return res_message, res_code
            else:
                return {"message": "User already has admin privileges"}, 403
        else:
            return {"message": "Unauthorized"}, 401


@user_ns.route("/login")
class UserAuth(Resource):
    @user_ns.doc(description="<b>Login route for the API</b>")
    @api.expect(api_login_model)
    def post(self):
        data = request.json
        res_message, res_code = LoginController().login_api(data)
        return res_message, res_code

    @api.doc(
        description="<b>Resets the password</b>", security="api-key",
    )
    @api.expect(reset_password_model)
    @jwt_required
    def put(self):
        data = request.json
        res_message, res_code = LoginController().change_password(data)
        return res_message, res_code


@train_ns.route("/train/<string:coach>")
class TrainRoutes(Resource):
    @api.doc(
        description="<b>Gets the passenger details of a particular coach </b>", security="api-key", summary="Passenger Details"
    )
    @jwt_required
    def get(self, coach):
        res_message, res_code = CustomMongoConnect("tthelper", "T16316").show_by_coach(
            coach
        )
        return res_message, res_code

@train_ns.route("/train/<string:coach>/<string:seat>")
class SeatPostiion(Resource):
    @api.doc(
        description="<b>Gets the passenger details of a particular seat in a coach </b>", security="api-key", summary="Passenger Details"
    )
    @jwt_required
    def get(self, coach, seat):
        res_message, res_code = CustomMongoConnect("tthelper", "T16316").show_by_seat(
            coach, seat
        )
        return res_message, res_code


if __name__ == "__main__":
    pass
else:
    app.run(debug=app.config["DEBUG"])
