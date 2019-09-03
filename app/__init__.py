import signal
import atexit
from app.utils.db import DBInit
from flask import Flask
from app.config import Config
from app.web.auth import bp_auth

app = Flask(__name__, static_folder=None)
app.config.from_object(Config)
app.secret_key = 'some secret key'
dbh = DBInit()
app.register_blueprint(bp_auth, url_prefix="/web")


def sig_handler(signum=None, frame=None):
    dbh.close_conn()
    print('*' * 10)


atexit.register(sig_handler)
signal.signal(signal.SIGINT, sig_handler)
signal.signal(signal.SIGTERM, sig_handler)


@app.route('/')
def root():
    return "App is running."

