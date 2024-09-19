from fastapi import APIRouter, Depends, HTTPException, status, UploadFile
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from .crud import get_user, create_user, create_tokens_in_body, authenticate_refresh_token, authenticate_user, authenticate_access_token, update_user_profile, check_email_duplicate, check_nickname_duplicate, delete_user_from_db
from .schemas import Token, UserBase, UpdateUserBase, LoginData
from .auth import AuthJWT
from app.logger import logger
from app.models import get_db
from app.bucket.s3_client import client_s3 
from app.bucket.crud import upload_file_to_s3

router = APIRouter(
    prefix="/api/v1/users",
    tags=["users"],
)

@router.post("/token", summary="새로운 엑세스 토큰 반환", status_code=200, response_model=Token)
async def get_token(Authorize: AuthJWT = Depends()):
    """
        새로운 엑세스 토큰 반환
    """
    token = authenticate_refresh_token(Authorize=Authorize)
    return JSONResponse({"access_token": token})

@router.post("/signup", summary="회원가입", status_code=201, response_model=None)
async def signup(
    signup_data: UserBase,  # JSON 데이터로 받음
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db),
):
    """
        회원가입
    """
    userForm = UserBase(email=signup_data.email, password=signup_data.password, nickname=signup_data.nickname)
    result = create_user(db, userForm)
    
    logger.info(result)
    if result != True:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=result)
    
    response_body = create_tokens_in_body(signup_data.email, Authorize)
    response_body["message"] = "유저 생성 및 로그인 성공"
    return JSONResponse(content=response_body, status_code=201)

@router.post("/login", summary="로그인", status_code=200, response_model=None)
async def login(
    login_data: LoginData,  # JSON 데이터로 받음
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db),
) -> Token:
    """
        로그인
    """
    user = authenticate_user(db, login_data.email, login_data.password)
    response_body = create_tokens_in_body(login_data.email, Authorize)
    logger.info(f"엑세스 토큰 기간 {Authorize._access_token_expires}")
    logger.info(f"디버깅용 유저 정보 {user.email}")
    return JSONResponse(status_code=200, content=response_body)

@router.get("/profile", summary="내 정보 조회", status_code=200)
async def get_profile(
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db)
):
    email = authenticate_access_token(Authorize=Authorize)
    user = get_user(db, email)
    if not user:
        raise HTTPException(status_code=400, detail="User not found.")
    
    user_profile = UpdateUserBase(
        nickname=user.nickname,
        profileUrl=user.profileUrl or ""
    )
    return JSONResponse(content=user_profile.dict(), status_code=200)

@router.patch("/profile", summary="내 정보 수정")
async def update_profile(
    profile_data: UpdateUserBase,  
    file: UploadFile = None, 
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db),
):
    email = authenticate_access_token(Authorize=Authorize)
    
    # 프로필 사진이 있는 경우 S3에 업로드하고 URL 받기
    profile_url = None
    if file:
        profile_url = await upload_file_to_s3(file, client_s3)
    
    # 프로필 업데이트 로직에 URL 전달
    result = update_user_profile(db, email, profile_data, profile_url)
    
    if not result:
        raise HTTPException(status_code=500, detail="프로필 수정 실패")

    return JSONResponse(content={"message": "프로필 수정 완료", "email": email}, status_code=201)

@router.get("/email", summary="이메일 중복체크", status_code=200)
async def check_email(email: str, db: Session = Depends(get_db)):
    """
    이메일 중복체크
    """
    is_duplicate = check_email_duplicate(db, email)
    if is_duplicate:
        return JSONResponse(content={"message": "이미 사용 중인 이메일입니다."}, status_code=400)
    return JSONResponse(content={"message": "사용 가능한 이메일입니다."}, status_code=200)

@router.get("/nickname", summary="닉네임 중복체크", status_code=200)
async def check_nickname(nickname: str, db: Session = Depends(get_db)):
    """
    닉네임 중복체크
    """
    is_duplicate = check_nickname_duplicate(db, nickname)
    if is_duplicate:
        return JSONResponse(content={"message": "이미 사용 중인 닉네임입니다."}, status_code=400)
    return JSONResponse(content={"message": "사용 가능한 닉네임입니다."}, status_code=200)

@router.delete("/delete", summary="회원 탈퇴", status_code=200)
async def delete_user(
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db)
):
    """
    사용자 삭제 (논리 삭제)
    """
    email = authenticate_access_token(Authorize=Authorize)
    result = delete_user_from_db(db, email)
    
    if result:
        return JSONResponse(content={"message": "유저 삭제 완료", "email": email}, status_code=200)
    else:
        raise HTTPException(status_code=500, detail="유저 삭제 실패")