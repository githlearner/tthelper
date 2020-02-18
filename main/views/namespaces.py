
from flask_restplus import Api, Resource, fields

from manage import app

auth = {
    "api-key": {"type": "apiKey", "in": "header", "name": "Authorization"},
    "x-api-key": {"type": "apiKey", "in": "header", "name": "X-API-KEY"},
}

api = Api(
    app,
    version="1.0",
    title="TTHelper",
    description="<i>Helps the Ticket Checkers to do updates and allocations</i>",
    contact_email="githinvgeorge@gmail.com",
    authorizations=auth,
)

user_ns = api.namespace("Users", description="TC Routes")
api.add_namespace(user_ns, path="/tcr")

train_ns = api.namespace("Train", description="Train Routes and endpoints")
api.add_namespace(train_ns, path="/train")