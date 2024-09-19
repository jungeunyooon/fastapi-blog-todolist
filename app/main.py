from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from app import models
from contextlib import asynccontextmanager
from app.user import routes as user_routes
from fastapi.security import OAuth2PasswordBearer
from app.bucket import routes as  s3_routes
from app.blog import routes as blog_routes
@asynccontextmanager
async def lifespan(app: FastAPI):
    models.SQLModel.metadata.create_all(models.engine)
    yield

# OAuth2PasswordBearer 설정
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/token")

app = FastAPI(lifespan=lifespan)
router = APIRouter(prefix="/api/v1")
app.include_router(user_routes.router)
app.include_router(s3_routes.router)
app.include_router(blog_routes.router)

# CORS 설정
origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 기본 엔드포인트
@app.get("/")
async def root():
    return {"message": "Hello World"}
