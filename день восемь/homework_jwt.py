import jwt
from datetime import datetime, timedelta, timezone

secret = "123"

def create_jwt(user_id, role, expires_in_hours=1):
    now = datetime.now(timezone.utc)
    payload = {
        'user_id': user_id,
        'role': role,
        'iat': now,
        'exp': now + timedelta(hours=expires_in_hours)
    }
    token = jwt.encode(payload, secret, algorithm='HS256')
    return token

def verify_jwt(token):
    try:
        jwt.decode(token, secret, algorithms=['HS256'])
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return False
    return True
