from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from api.core.security import create_access_token
from api.v1.schemas.user import Token, User
from api.v1.services.auth import authenticate_user, register_user


router = APIRouter()


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED
)
def register(user: User):
    """Register a new user"""
    
    result = register_user(user.username, user.password, user.role)
    
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result["message"]
        )
    
    return {
        "status": "success",
        "message": result["message"],
        "data": {
            "username": result["user"]["username"],
            "role": result["user"]["role"]
        }
    }


@router.post(
    "/login",
    response_model=Token
)
@router.post(
    "/login",
    response_model=Token
)
def login(
    username: str,
    password: str
):
    """Login with username and password"""

    user = authenticate_user(username, password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )

    access_token = create_access_token(
        data={
            "sub": user["username"]
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }