from sqlalchemy.orm import Session
from app.models import Blog  # Blog 모델은 기존에 정의되어 있다고 가정
from app.blog.schemas import BlogBase
from datetime import datetime

# 블로그 생성
def create_blog(db: Session, blog_data: BlogBase, user_id: int):
    new_blog = Blog(
        title=blog_data.title,
        content=blog_data.content,
        userId=user_id,  # userId 저장
        createdAt=datetime.now()
    )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

# 모든 블로그 조회
def get_all_blogs(db: Session):
    return db.query(Blog).filter(Blog.isDeleted == False).all()  # 삭제되지 않은 블로그만 조회

# 사용자가 작성한 블로그 조회
def get_blogs_by_user(db: Session, user_id: int):
    return db.query(Blog).filter(Blog.userId == user_id, Blog.isDeleted == False).all()

# 블로그 수정
def update_blog(db: Session, blog_id: int, blog_data: BlogBase, user_id: int):
    blog = db.query(Blog).filter(Blog.id == blog_id, Blog.userId == user_id, Blog.isDeleted == False).first()
    if blog:
        blog.title = blog_data.title
        blog.content = blog_data.content
        blog.updatedAt = datetime.now()
        db.commit()
        db.refresh(blog)
        return blog
    return None

# 블로그 삭제 (논리적 삭제)
def delete_blog(db: Session, blog_id: int, user_id: int):
    blog = db.query(Blog).filter(Blog.id == blog_id, Blog.userId == user_id, Blog.isDeleted == False).first()
    if blog:
        blog.isDeleted = True  # 실제 삭제가 아닌 논리적 삭제 처리
        db.commit()
        return True
    return False
