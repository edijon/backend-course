"""
This module provides basic authentication functionality using FastAPI.
It includes endpoints for user login and token verification. The login endpoint
validates user credentials and returns a fake access token. The token verification
endpoint decodes the token and retrieves the current user.

Note: This implementation uses hardcoded credentials and a fake token for demonstration
purposes. It is not secure and should not be used in production. Proper security measures,
such as hashing passwords and using a real token generation mechanism, should be implemented
"""
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
router = APIRouter()


def fake_decode_token(token: str):
    if token == "fake-super-secret-token":
        return {"sub": "user"}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    return fake_decode_token(token)


@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Handles user login and returns an access token.
    """
    if form_data.username == "user" and form_data.password == "password":
        return {"access_token": "fake-super-secret-token", "token_type": "bearer"}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
