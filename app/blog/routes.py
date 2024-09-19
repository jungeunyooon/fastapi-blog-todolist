from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.blog.crud import create_blog, get_all_blogs, get_blogs_by_user, update_blog, delete_blog
from app.blog.schemas import BlogBase
from app.user.auth import AuthJWT
from app.models import get_db, User  # 데이터베이스 세션 가져오기
from fastapi.responses import JSONResponse

router = APIRouter(
    prefix="/api/v1/blogs",
    tags=["blogs"]
)

# 블로그 생성
@router.post("",summary="블로그 등록")
async def create_blog_route(
    blog_data: BlogBase,
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db)
):
    email = Authorize.get_jwt_subject()  # JWT 토큰에서 이메일 추출
    user = db.query(User).filter(User.email == email).first()  # 이메일로 유저 조회
    
    if not user:
        raise HTTPException(status_code=404, detail="유저를 찾을 수 없습니다.")
    
    new_blog = create_blog(db, blog_data, user.id)  # user.id를 전달하여 블로그 작성
    return JSONResponse(content={"message": "블로그가 등록되었습니다", "blog": new_blog.title}, status_code=201)

# 전체 블로그 조회
@router.get("",summary="블로그 전체 조회")
async def get_all_blogs_route(
    db: Session = Depends(get_db)
):
    blogs = get_all_blogs(db)
    if not blogs:
        raise HTTPException(status_code=404, detail="블로그가 없습니다.")
    return blogs

# 사용자가 작성한 블로그 조회
@router.get("/id", summary="내가 쓴 블로그 조회")
async def get_blogs_by_user_route(
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db)
):
    email = Authorize.get_jwt_subject()
    user = db.query(User).filter(User.email == email).first()  # 이메일로 유저 조회
    
    if not user:
        raise HTTPException(status_code=404, detail="유저를 찾을 수 없습니다.")
    
    blogs = get_blogs_by_user(db, user.id)  # user.id로 블로그 조회
    if not blogs:
        raise HTTPException(status_code=404, detail="작성한 블로그가 없습니다.")
    
    return blogs


# 블로그 수정
@router.patch("/{blog_id}", summary="블로그 수정")
async def update_blog_route(
    blog_id: int,
    blog_data: BlogBase,
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db)
):
    email = Authorize.get_jwt_subject()
    user = db.query(User).filter(User.email == email).first()  # 이메일로 유저 조회
    
    if not user:
        raise HTTPException(status_code=404, detail="유저를 찾을 수 없습니다.")
    
    updated_blog = update_blog(db, blog_id, blog_data, user.id)  # user.id를 사용
    if not updated_blog:
        raise HTTPException(status_code=404, detail="블로그를 수정할 수 없습니다.")
    
    return JSONResponse(content={"message": "블로그가 수정되었습니다", "blog": updated_blog.title}, status_code=200)

# 블로그 삭제
@router.delete("/{blog_id}", summary="블로그 삭제")
async def delete_blog_route(
    blog_id: int,
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db)
):
    email = Authorize.get_jwt_subject()
    user = db.query(User).filter(User.email == email).first()  # 이메일로 유저 조회
    
    if not user:
        raise HTTPException(status_code=404, detail="유저를 찾을 수 없습니다.")
    
    success = delete_blog(db, blog_id, user.id)  # user.id로 삭제
    if not success:
        raise HTTPException(status_code=404, detail="블로그를 삭제할 수 없습니다.")
    
    return JSONResponse(content={"message": "블로그가 삭제되었습니다"}, status_code=200)
