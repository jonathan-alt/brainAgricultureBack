from datetime import datetime, timedelta
from typing import Optional, Tuple

from fastapi import Request
from fastapi.openapi.models import HTTPBearer as HTTPBearerModel
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.security.base import SecurityBase
from fastapi.security.utils import get_authorization_scheme_param
from jose import jwt
from passlib.context import CryptContext

from app.core.config import config
from app.core.exceptions import UnauthorizedError

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ALGORITHM = "HS256"


def create_access_token(subject: dict, expires_delta: timedelta = None) -> Tuple[str, str]:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"exp": expire, **subject}
    encoded_jwt = jwt.encode(payload, config.SECRET_KEY, algorithm=ALGORITHM)
    expiration_datetime = expire.strftime(config.DATETIME_FORMAT)
    return encoded_jwt, expiration_datetime


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def decode_jwt(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, config.SECRET_KEY, algorithms=ALGORITHM)
        return decoded_token if decoded_token["exp"] >= int(round(datetime.utcnow().timestamp())) else None
    except Exception as e:
        return {}


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise UnauthorizedError(detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise UnauthorizedError(detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise UnauthorizedError(detail="Invalid authorization code.")

    def verify_jwt(self, jwt_token: str) -> bool:
        is_token_valid: bool = False
        try:
            payload = decode_jwt(jwt_token)
        except Exception as e:
            payload = None
        if payload:
            is_token_valid = True
        return is_token_valid


class ApiToken(SecurityBase):
    def __init__(
        self,
        *,
        bearerFormat: Optional[str] = None,
        scheme_name: Optional[str] = None,
        description: Optional[str] = None,
        auto_error: bool = True,
    ):
        self.model = HTTPBearerModel(bearerFormat=bearerFormat, description=description)
        self.scheme_name = scheme_name or self.__class__.__name__
        self.auto_error = auto_error

    async def __call__(self, request: Request) -> Optional[HTTPAuthorizationCredentials]:
        authorization: str = request.headers.get("Authorization")
        scheme, credentials = get_authorization_scheme_param(authorization)
        if not (authorization and scheme and credentials):
            raise UnauthorizedError(detail="Invalid ApiKey or expired ApiKey.")

        if scheme.lower() != "apikey":
            raise UnauthorizedError(detail="Use ApiKey YOUR_API_KEY in Authorization header.")

        return HTTPAuthorizationCredentials(scheme=scheme, credentials=credentials)
