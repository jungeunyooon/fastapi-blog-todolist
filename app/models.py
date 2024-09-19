from sqlmodel import Field, SQLModel, create_engine, Relationship, Session
from typing import Optional, List
from datetime import datetime
from app.configs import DATABASE_URL

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    createdAt: datetime = Field(default_factory=datetime.now)
    updatedAt: datetime = Field(default_factory=datetime.now)
    isDeleted: bool = Field(default=False)
    email: str
    nickname: str
    profileUrl: Optional[str] = None
    password: str
    blogs: List["Blog"] = Relationship(back_populates="author")

class Blog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    createdAt: datetime = Field(default_factory=datetime.now)
    updatedAt: datetime = Field(default_factory=datetime.now)
    isDeleted: bool = Field(default=False)
    title: str
    content: str
    userId: Optional[int] = Field(default=None, foreign_key="user.id")
    author: Optional[User] = Relationship(back_populates="blogs")

engine = create_engine(DATABASE_URL, echo=True)

SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
        
def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()