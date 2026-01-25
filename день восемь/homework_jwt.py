import time

import jwt


def create_jwt(uid: int, role: str, expires: int, secret: str) -> str:
    return jwt.encode({"id": uid, "role": role, "exp": time.time() + expires}, secret, algorithm="HS256")


def verify_jwt(token: str, secret: str) -> bool:
    try:
        jwt.decode(token, secret, algorithms=["HS256"])
        return True
    except jwt.ExpiredSignatureError:
        print("Token expired")
        return False
    except jwt.InvalidTokenError:
        return False

secret = "BIGSECRET"
myjwt = create_jwt(uid=1, role="user", expires=86400, secret=secret)
myjwt1 = create_jwt(uid=1, role="user", expires=1, secret=secret)
time.sleep(2)
print(verify_jwt(myjwt, secret))
print(verify_jwt(myjwt1, secret))
print(verify_jwt(myjwt + "1", secret))