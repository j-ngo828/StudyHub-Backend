# this is a middleware function that take a request and response to validate the token from the request to grant users access to protected resources that required authentication
from functools import wraps
from flask import request, jsonify, current_app
from login import login_app
import jwt
import pdb
from urllib.parse import urlparse, parse_qs

def token_required(permission):
 def decorator(f):
  @wraps(f)
  def decorated_function(*args, **kwargs):
   token = request.cookies.get('token')
   if not token:
    return jsonify({'message' : 'Token is missing!'}), 401
   try:
    data = jwt.decode(token, login_app.config['SECRET_KEY'], algorithms=['HS256'])
    if permission not in data['permissions']:
      return jsonify({'message' : 'Unauthorized access!'}), 403
   except:
    return jsonify({'message' : 'Token is invalid!'}), 401
   return f(*args, *kwargs)
  return decorated_function
 return decorator