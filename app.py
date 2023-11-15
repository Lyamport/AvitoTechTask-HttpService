from flask import Flask, request, abort

from database import *
from service import check_valid_ip


app = Flask(__name__)


@app.route('/')
def index():
    user_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    if check_valid_ip(user_ip):
        if add_address(user_ip):
            return f"IP: {user_ip}"
        else:
            abort(429, 'Too Many Requests')


@app.errorhandler(429)
def handle_429_error(e):
    return "Error 429: Too Many Requests"


if __name__=="__main__":
    app.run(debug=True, threaded=False)