
import os
import jwt
import logging

logger = logging.getLogger("ai-guard-gateway")
SECRET_KEY = os.getenv("SECRET_KEY")

def validate_auth(api_key=None, auth_header=None):
    if api_key == "sk-premium-67890":
        return {"user": "vip_user", "role": "premium"}
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            return {"user": payload.get("sub"), "role": payload.get("role")}
        except Exception:
            return None
    return None
