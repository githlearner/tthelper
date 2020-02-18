from main import db, bcrypt
import datetime


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True)
    username = db.Column(db.String(255))
    password_hash = db.Column(db.String(50))
    admin = db.Column(db.Boolean)
    public_id = db.Column(db.String(255), unique=True)
    added_on = db.Column(db.DateTime, default=datetime.datetime.now())

    @property
    def password():
        raise AttributeError("Password : Write only field")

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode("UTF-8")

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

