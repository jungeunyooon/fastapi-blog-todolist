from pydantic import BaseModel
from datetime import timedelta
from app.configs import JWT_ALGORITHM, JWT_SECRET_KEY, JWT_ACCESS_EXPIRE_MINUTES, JWT_REFRESH_EXPIRE_DAYS

class Token(BaseModel):
    access_token: str
    refresh_token: str

class Settings(BaseModel):
    authjwt_secret_key: str = JWT_SECRET_KEY
    access_expires: int = timedelta(minutes=JWT_ACCESS_EXPIRE_MINUTES)
    refresh_expires: int = timedelta(days=JWT_REFRESH_EXPIRE_DAYS)
    authjwt_token_location: set = {"headers"}
    authjwt_header_name: str = "Authorization"
    authjwt_header_type: str = "Bearer"
    authjwt_algorithm: str = JWT_ALGORITHM
    authjwt_decode_algorithms: list = [JWT_ALGORITHM]

class UserBase(BaseModel):
    email: str
    password: str
    nickname: str

class UpdateUserBase(BaseModel):
    nickname: str

class LoginData(BaseModel):
    email: str
    password: str