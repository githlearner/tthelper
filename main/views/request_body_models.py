
from flask_restplus import Api, Resource, fields

from manage import app
from .namespaces import api

api_model = api.model(
    "user",
    {
        "username": fields.String(required=True, description="Username"),
        "password": fields.String(required=True, description="Password"),
        "email": fields.String(required=True, description="Email"),
        "admin": fields.Boolean(required=True, description="Admin"),
    },
)


api_login_model = api.model(
    "login",
    {
        "username": fields.String(required=True, description="Username"),
        "password": fields.String(required=True, description="Password"),
    },
)

admin_model = api.model(
    "admin_model",
    {
        "username": fields.String(
            required=True, description="Username to be promoted as Admin"
        ),
    },
)

reset_password_model = api.model(
    "reset_password",
    {
        "username": fields.String(required=True, description="Username"),
        "email": fields.String(required=True, description="Email"),
        "new_password": fields.Boolean(required=True, description="New_Password"),
    },
)
