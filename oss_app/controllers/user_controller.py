# pylint: disable=unused-wildcard-import, method-hidden
# pylint: enable=too-many-lines
# pylint: disable=no-member
from oss_app import app
from flask import request, jsonify
from oss_app.models.userDetails import User
from oss_app.models.userDetails import UserService
from oss_app.security.identity import find_user
from oss_app.errors.jsonp import enable_jsonp
from oss_app.errors.error_handling import ErrorResponse
from oss_app.errors.error_handling import SuccessResponse
from flask_jwt import jwt_required, current_identity
import uuid
import logging


# --------------------------------------------------------------------------
# GET USERS
# --------------------------------------------------------------------------
# Gets the users information associated with current session
@app.route('/api/v1/users', methods=['GET'])
@jwt_required()
@enable_jsonp
def get_account():
    return current_identity.as_json()


# --------------------------------------------------------------------------
# GET: /users/<uid>
# --------------------------------------------------------------------------
@app.route('/api/v1/users/<user_id>', methods=['GET'])
@jwt_required()
@enable_jsonp
def get_user_by_id(user_id):
    identity = find_user(user_id)
    if identity:
        return identity.as_json()
    return ErrorResponse('User not found !!', 'user_id is invalid !!').as_json()


# --------------------------------------------------------------------------
# PUT: /users/<uid>/password
# --------------------------------------------------------------------------
@app.route('/api/v1/users/<user_id>/password', methods=['PATCH'])
@jwt_required()
@enable_jsonp
def update_user_password(user_id):
    try:
        pass_data = request.get_json()
        user_service = UserService(user_id)
        usr = user_service.get_user()
        if user_id == current_identity.id:
            if usr.update_password(pass_data['password']):
                app.logger.info('Updated password for user_id: %s', user_id)
                return SuccessResponse('Success', 'Password updated successfully !!', 'EMAIL_OK').as_json()
        else:
            app.logger.error('Permission denied. User not authorized to update other user\'s password. User performing operation %s', user_id)
            return ErrorResponse('Permission denied', 'This action generated a security alert').as_json()
    except:
        app.logger.error('Invalid json received for user: %s', user_id)
        return ErrorResponse('Could not update password', 'Invalid password provided').as_json()


# --------------------------------------------------------------------------
# PUT: /users/<uid>/email
# --------------------------------------------------------------------------
@app.route('/api/v1/users/<user_id>/email', methods=['PATCH'])
@jwt_required()
@enable_jsonp
def update_user_email(user_id):
    try:
        email_data = request.get_json()
        user_service = UserService(user_id)
        user = user_service.get_user()
        if user.update_email(email_data['email']):
            app.logger.info('Updated email for user_id: %s', user_id)
            return SuccessResponse('Success', 'Email updated successfully !!', 'EMAIL_OK').as_json()
    except:
        app.logger.error('Invalid json received for user: %s', user_id)
        return ErrorResponse('Could not update email !!', 'Invalid email provided !!').as_json()


# --------------------------------------------------------------------------
# POST: /users
# --------------------------------------------------------------------------
@app.route('/api/v1/users', methods=['POST'])
@enable_jsonp
def post_user():
    user_data = request.get_json()
    if user_data:
        user = User(
            user_id=str(uuid.uuid4()),
            name=user_data['name'],
            last_name=user_data['last_name'],
            email=user_data['email'],
            username=user_data['username'],
            password=None
            )
        user.update_password(user_data['password'])
        encoded_token = user.encode_auth_token(user.user_id)
        decoded_token = user.decode_auth_token(encoded_token)
        app.logger.info('encoded_token %s was created', encoded_token)
        app.logger.info('decoded_token %s was created', decoded_token)
        user.save(validate=True)
        app.logger.info('User %s was created', user.user_id)
        return SuccessResponse(user.user_id, 'User created successfully !!', 'n/a').as_json()
    return ErrorResponse('Error processing request !!', 'data is invalid !!').as_json()
