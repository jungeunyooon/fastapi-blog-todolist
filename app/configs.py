from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.environ.get("LOCAL_DATABASE_URL")  # 서버 로컬로 실행할 시의 DB 연동 URL
# DATABASE_URL = os.environ.get("DATABASE_URL")  
JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
JWT_ALGORITHM = os.environ.get('JWT_ALGORITHM')
JWT_ACCESS_EXPIRE_MINUTES = int(os.environ.get('JWT_ACCESS_TOKEN_EXPIRE_MINUTES'))
JWT_REFRESH_EXPIRE_DAYS = int(os.environ.get('JWT_REFRESH_TOKEN_EXPIRE_DAYS'))
CREDENTIALS_ACCESS_KEY = os.getenv("CREDENTIALS_ACCESS_KEY")
CREDENTIALS_SECRET_KEY = os.getenv("CREDENTIALS_SECRET_KEY")