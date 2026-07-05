import jwt
import time
from typing import Optional, Dict, Any
from fastapi import HTTPException, status

# Secretos de seguridad (En producción, estos irían en variables de entorno o Vault)
import os
SECRET_KEY = os.getenv("AI_GUARD_SECRET")
if not SECRET_KEY:
    raise RuntimeError("CRITICAL ERROR: AI_GUARD_SECRET environment variable is not set. The gateway cannot start without a secure key.")
ALGORITHM = "HS256"

# Base de datos simulada de usuarios y API Keys
# Formato: { "api_key": {"user": "nombre", "role": "rol"} }
USER_DB = {
    "sk-free-12345": {"user": "usuario_gratis", "role": "free"},
    "sk-premium-67890": {"user": "usuario_vip", "role": "premium"},
    "sk-admin-00000": {"user": "admin_sil", "role": "admin"},
}

class AuthManager:
    @staticmethod
    def validate_api_key(api_key: str) -> Dict[str, Any]:
        """Valida una API Key contra la DB simulada."""
        if api_key in USER_DB:
            return USER_DB[api_key]
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="API Key inválida o inexistente."
        )

    @staticmethod
    def validate_jwt(token: str) -> Dict[str, Any]:
        """Decodifica y valida un JWT."""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            # Verificar que el token no haya expirado
            if "exp" in payload and time.time() > payload["exp"]:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, 
                    detail="El token JWT ha expirado."
                )
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expirado.")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token JWT inválido.")

    @staticmethod
    def create_access_token(data: dict, expires_in: int = 3600):
        """Crea un JWT para pruebas."""
        to_encode = data.copy()
        expire = time.time() + expires_in
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
