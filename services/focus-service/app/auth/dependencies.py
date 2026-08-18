from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import InvalidTokenError
from jwt import decode
from jwt import PyJWKClient
from jwt.exceptions import PyJWKClientError

from app.config import (
    get_cognito_app_client_id,
    get_cognito_issuer,
)


bearer_scheme = HTTPBearer(auto_error=False)
issuer = get_cognito_issuer()
app_client_id = get_cognito_app_client_id()
jwks_client = PyJWKClient(
    f"{issuer}/.well-known/jwks.json",
)


def get_current_user_id(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> str:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise _unauthorized()

    try:
        signing_key = jwks_client.get_signing_key_from_jwt(credentials.credentials)
        claims = decode(
            credentials.credentials,
            signing_key.key,
            algorithms=["RS256"],
            issuer=issuer,
            options={"require": ["exp", "iss", "sub", "token_use", "client_id"]},
        )
    except (InvalidTokenError, PyJWKClientError, ValueError) as error:
        raise _unauthorized() from error

    if claims.get("token_use") != "access":
        raise _unauthorized()
    if claims.get("client_id") != app_client_id:
        raise _unauthorized()

    user_id = claims.get("sub")
    if not isinstance(user_id, str) or not user_id:
        raise _unauthorized()
    return user_id


def _unauthorized() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing Cognito access token.",
        headers={"WWW-Authenticate": "Bearer"},
    )
