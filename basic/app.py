from flask import Flask, request, Response
from functools import wraps

app = Flask(__name__)


def auth(fn):
    wraps(fn)
    def decorated(*args, **wargs):
        auth = request.authorization
        if not auth or not (auth.username == 'admin' and auth.password == 'admin'):
            return Response('You are not authorized', 401, { 'WWW-Authenticate': 'Basic realm="Login Required"' })
        return fn(*args, **wargs)
    return decorated

@app.route('/')
@auth
def secret_router():
    return 'This is my authenticated router'

if __name__ == '__main__':
    app.run()