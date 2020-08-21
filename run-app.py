import os
from oss_app import app


__author__ = "Sudhanshu Satyam (susatyam@in.ibm.com)"
__version__ = "1.0"


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run('127.0.0.1', port)
