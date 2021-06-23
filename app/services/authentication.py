import jwt
from flask import request

from app import app


def protected_route(func):
    def __validate_jwt(*args, **kwargs):
        token = request.headers.get('Authorization').split(" ")[1]
        try:
            token_data = jwt.decode(
                token, app.config.get("SECRET_KEY"), algorithms=["HS256"])
            if type(token_data) == dict:
                func()
            else:
                raise(Exception("Error en el token de autenticacion"))
        except jwt.ExpiredSignatureError:
            raise(Exception("El tiempo valido del token expiro"))
    return __validate_jwt
