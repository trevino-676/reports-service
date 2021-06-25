from functools import wraps

import jwt
from flask import request, make_response

from app import app


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")

        if not token:
            return make_response({"message": "Falta token de autenticacion"}, 403)

        try:
            data = jwt.decode(token, app.config["SECRET_KEY"], algorithms="HS256")
            app.logger.info(data)
        except Exception as e:
            app.logger.error(e)
            return make_response({"message": "token invalido"}, 401)

        return f(*args, **kwargs)

    return decorated()
