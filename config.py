import datetime
import os

# Turns on debugging features in Flask
DEBUG = True
#
# For use in web_app emails
MAIL_FROM_EMAIL = "susatyam@in.ibm.com"

# secret key used by Flask to sign cookies.
SECRET_KEY = os.getenv('SECRET_KEY', 'secretkey')
#
# Configuration for the Flask-Bcrypt extension
BCRYPT_LEVEL = 12
#
# ----------------------------------------------------------------
# JWT CONFIGURATIONS
# ----------------------------------------------------------------
# Set the token validity
JWT_AUTH_URL_RULE = '/api/v1/auth'
JWT_EXPIRATION_DELTA = datetime.timedelta(3600) 
