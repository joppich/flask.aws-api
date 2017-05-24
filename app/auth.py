import os
from uuid import uuid1
from flask_httpauth import HTTPTokenAuth
from flask import g


auth = HTTPTokenAuth(scheme='Token')

access_dict = {os.environ.get('APP_AUTH_TOKEN', 'toomanysecrets'):str(uuid1())}


@auth.verify_token
def verify_token(token):
    if token in access_dict:
        g.current_user = access_dict[token]
        return True
    else:
        return False
