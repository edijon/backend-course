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
    Args:
        form_data (OAuth2PasswordRequestForm): The form data containing the username and password.
    Returns:
        dict: A dictionary containing the access token and token type if the credentials are valid.
    HTTP Status Codes:
        200 OK: If the login is successful and the credentials are valid.
        401 Unauthorized: If the login fails due to invalid credentials.
    """
    if form_data.username == "user" and form_data.password == "password":
        return {"access_token": "fake-super-secret-token", "token_type": "bearer"}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
