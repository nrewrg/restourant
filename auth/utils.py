from passlib.context import CryptContext

import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

from fastapi import HTTPException

from typing import Dict, TYPE_CHECKING

import time

from config import settings

if TYPE_CHECKING:
    from users import User

crypt_context: CryptContext = CryptContext(schemes=["bcrypt"])


def hash_password(password: str) -> str:
    return crypt_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return crypt_context.verify(password, hashed_password)


def create_access_token(user: "User") -> str:
    claims = {
        "sub": str(user.id),
        "iat": int(time.time()),
        "exp": int(time.time()) + settings.ACCESS_TOKEN_EXPIRATION_TIME,
    }

    return jwt.encode(
        headers={"alg": "HS256", "typ": "JWT"},
        payload=claims,
        key=settings.ACCESS_TOKEN_SIGNATURE_SECRET,
    )


def decode_token(token: str) -> Dict:
    try:
        token_data: Dict = jwt.decode(
            jwt=token, key=settings.ACCESS_TOKEN_SIGNATURE_SECRET, algorithms=["HS256"]
        )
    except ExpiredSignatureError:
        raise HTTPException(status_code=403, detail="Expired token")
    except InvalidTokenError:
        raise HTTPException(status_code=403, detail="Invalid token")

    return token_data
