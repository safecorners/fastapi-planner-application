from typing import Dict

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from planner.auth.hash_password import HashPassword
from planner.auth.jwt_handler import create_access_token
from planner.database.connection import Database
from planner.models.users import TokenResponse, User, UserSignIn

user_router = APIRouter(
    tags=["User"],
)

user_database = Database(User)
hash_password = HashPassword()


@user_router.post("/signup")
async def sign_new_user(user: User) -> Dict[str, str]:
    user_exist = await User.find_one(User.email == user.email)
    if user_exist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with suppled username exists",
        )

    hashed_password = hash_password.create_hash(user.password)
    user.password = hashed_password
    print(f"{user.email},{user.password}")
    await user_database.save(user)

    return {"message": "User created successfully."}


@user_router.post("/signin", response_model=TokenResponse)
async def sign_user_in(user: OAuth2PasswordRequestForm = Depends()) -> Dict[str, str]:
    user_exist = await User.find_one(User.email == user.username)
    if not user_exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist"
        )

    if hash_password.verify_hash(user.password, user_exist.password):
        access_token = create_access_token(user_exist.email)
        return {"access_token": access_token, "token_type": "Bearer"}

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials passed"
    )
