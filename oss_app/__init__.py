import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from mongoengine import *
from flask_jwt import JWT


# ------------------------------------------------------------------------------
# SETUP GENERAL APPLICATION
# ------------------------------------------------------------------------------
__version__ = '1.0'
app = Flask('oss_app')
app.config.from_object('config')
app.debug = True

# ------------------------------------------------------------------------------
# SETUP LOGGING
# ------------------------------------------------------------------------------
logger = logging.getLogger()
handler = RotatingFileHandler('oss_app.log', maxBytes=10000, backupCount=1)
handler.setLevel(logging.INFO)
logger.addHandler(handler)

# ------------------------------------------------------------------------------
# SETUP MONGO DB 
# ------------------------------------------------------------------------------
connect('OSS-MVS-DEV', host='127.0.0.1', port=27017)

# Import all oss_app controller files
from oss_app.controllers import default_controller, user_controller

# ------------------------------------------------------------------------------
# SETUP JWT AUTHENTICATION
# ------------------------------------------------------------------------------
from oss_app.security import identity
jwt = JWT(app, identity.authenticate, identity.identity)