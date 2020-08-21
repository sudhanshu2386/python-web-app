# pylint: disable=unused-wildcard-import, method-hidden
# pylint: enable=too-many-lines
# pylint: disable=no-member
from mongoengine import * 
from oss_app.security.password_encoder import gen_salt, compute_hash
from flask import jsonify
from werkzeug.security import safe_str_cmp
import datetime
import jwt
from oss_app import app


# ------------------------------------------------------------------------------
# CLASS IDENTITY
# ------------------------------------------------------------------------------
class SessionIdentity:

    # --------------------------------------------------------------------------
    # CONSTRUCTOR METHOD
    # --------------------------------------------------------------------------
    def __init__(self, id, username, name, last_name, email):
        self.id = id
        self.username = username
        self.name = name
        self.last_name = last_name
        self.email = email

    # --------------------------------------------------------------------------
    # METHOD STR
    # --------------------------------------------------------------------------
    def as_json(self):
        return jsonify({
            "id": self.id,
            "username": self.username,
            "name": self.name,
            "last_name": self.last_name,
            "email": self.email
        })


# ------------------------------------------------------------------------------
# CLASS USER
# ------------------------------------------------------------------------------
class User(Document):

    # --------------------------------------------------------------------------
    # USER PROPERTIES
    # --------------------------------------------------------------------------
    user_id = StringField(max_length=40, required=True)
    name = StringField(max_length=120, required=True)
    last_name = StringField(max_length=120, required=True)
    email = StringField(max_length=120, required=True, unique=True)
    username = StringField(max_length=120, required=True, unique=True)
    password = StringField(max_length=256, required=True)
    salt = StringField(max_length=17, required=True, default=gen_salt(17))
    date_modified = DateTimeField(default=datetime.datetime.now)
    

    meta = {
        'indexes': [
            'user_id',
            'username',
            'email'
        ]
    }


  # --------------------------------------------------------------------------
    # METHOD STR
    # --------------------------------------------------------------------------
    # Creates a string representation of a user
    def __str__(self):
        return "User(username='%s')" % self.username

    # --------------------------------------------------------------------------
    # METHOD UPDATE PASSWORD
    # --------------------------------------------------------------------------
    def update_password(self, password):
        self.password = compute_hash(password, self.salt)
        self.save()
        return True

    # --------------------------------------------------------------------------
    # METHOD UPDATE EMAIL
    # --------------------------------------------------------------------------
    def update_email(self, email):
        self.email = email
        self.save()
        return True

    # --------------------------------------------------------------------------
    # METHOD ENCODE JWT TOKEN
    # --------------------------------------------------------------------------
    def encode_auth_token(self, user_id):
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=3600),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except jwt.InvalidTokenError:
            app.logger.error('Invalid token. Please log in again!!')
        return None

    
    # --------------------------------------------------------------------------
    # METHOD DECODE JWT TOKEN
    # --------------------------------------------------------------------------
    def decode_auth_token(self, auth_token):
        try:
            payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            app.logger.error('Signature expired. Please log in again!!')
        except jwt.InvalidTokenError:
            app.logger.error('Invalid token. Please log in again!!')
        return None


    # --------------------------------------------------------------------------
    # METHOD AUTHENTICATE
    # --------------------------------------------------------------------------
    def authenticate(self, password):
        challenge = compute_hash(password, self.salt)
        return safe_str_cmp(self.password.encode('utf-8'), challenge.encode('utf-8'))


    # --------------------------------------------------------------------------
    # METHOD GET IDENTITY
    # --------------------------------------------------------------------------
    def get_identity(self):
        return SessionIdentity(self.user_id,
                               self.username,
                               self.name,
                               self.last_name,
                               self.email)



# ------------------------------------------------------------------------------
# CLASS USER SERVICE
# ------------------------------------------------------------------------------
class UserService:
    def __init__(self, user_id):
        self.user_id = user_id

    def get_user(self):
        user = User.objects.get(user_id=self.user_id)
        if user:
            return user
        return None