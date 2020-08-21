# pylint: disable=unused-wildcard-import, method-hidden
# pylint: enable=too-many-lines
# pylint: disable=no-member
from oss_app import app
from oss_app.models.userDetails import User
from mongoengine import *
import logging
 

# ------------------------------------------------------------------------------
# IDENTITY AND ACCESS MANAGEMENT
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# FUNCTION AUTHENTICATE
# ------------------------------------------------------------------------------
# Checks given credential in order to authenticate or deny authentication to the
# API.
def authenticate(username, password):
    try:
        user = User.objects.get(username=username)
        if user and user.authenticate(password=password):
            app.logger.warning('user authentication is successful !! user: '+username)
            return user.get_identity()
        else:
            app.logger.warning('User: attempted to login using invalid credentials. ' + username)
    except DoesNotExist:
        app.logger.warning('logging attempt of non-existing user: occurred. ' + username)
    except MultipleObjectsReturned:
        app.logger.error('username already found in database !! '+username)
    return None


# ------------------------------------------------------------------------------
# FUNCTION IDENTITY
# ------------------------------------------------------------------------------
# Gets the User associated with a given identity
def identity(payload):
    try:
        user_id = payload['identity']
        user = User.objects.get(user_id=user_id)
        return user.get_identity()
    except DoesNotExist:
        app.logger.warning('retrieval attempt of non-existing user occurred: ' + user_id)
    except MultipleObjectsReturned:
        app.logger.error('username already found in database !! '+user_id)
    return None


# ------------------------------------------------------------------------------
# FIND USER
# ------------------------------------------------------------------------------
def find_user(user_id):
    try:
        user = User.objects.get(user_id=user_id)
        return user.get_identity()
    except DoesNotExist:
        app.logger.warning('retrieval attempt of non-existing user occurred: ' + user_id)
    except MultipleObjectsReturned:
        app.logger.error('username already found in database !! ' + user_id)
    return None
