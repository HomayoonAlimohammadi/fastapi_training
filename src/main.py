from typing import Union
import pydantic
from fastapi import FastAPI

app = FastAPI()


class UserIn(pydantic.BaseModel):
    username: str
    password: str
    email: pydantic.EmailStr
    full_name: str


class UserOut(pydantic.BaseModel):
    username: str
    email: pydantic.EmailStr
    full_name: str


class UserInDB(pydantic.BaseModel):
    username: str
    hashed_password: str
    email: pydantic.EmailStr
    full_name: str


@app.post(
    "/users/register", response_model=dict[str, UserInDB | UserOut], status_code=201
)
async def register_user(user_data: UserIn):
    hashed_password = hash(user_data.password)
    return {
        "user_in_db": UserInDB(**user_data.dict(), hashed_password=hashed_password),
        "user_out": UserOut(**user_data.dict()),
    }


@app.post("/users/register/out", response_model=UserInDB)
async def register_user_out(user_data: UserIn):
    user_in_db = UserInDB(**user_data.dict(), hashed_password="123")
    return user_in_db
