from oss_app import app
from flask import jsonify


# --------------------------------------------------------------------------
# ROOT RESOURCE OF THE API
# --------------------------------------------------------------------------
#
@app.route('/', methods=['GET'])
def get_api_root():
    return jsonify({
        "platform": "OSS API 1.0",
        "version": "1.0",
        "message": "OSS-MVS application is Live now!"
    })
