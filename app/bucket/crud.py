from botocore.exceptions import NoCredentialsError
from fastapi import UploadFile, HTTPException
import logging
from datetime import datetime
from app.bucket.s3_client import client_s3  # 분리한 S3 클라이언트 불러오기

async def upload_file_to_s3(file: UploadFile) -> str:
    try:
        file_name = f"{datetime.now().isoformat()}-{file.filename}"
        content_type = file.content_type

        # 파일을 S3에 업로드
        client_s3.upload_fileobj(
            file.file,
            "profileuserbucket",  # 버킷 이름을 직접 지정
            file_name,
            ExtraArgs={
                "ContentType": content_type
            }
        )

        # S3 파일 URL 생성
        location = client_s3.get_bucket_location(Bucket="profileuserbucket")['LocationConstraint']
        url = f"https://profileuserbucket.s3-{location}.amazonaws.com/{file_name}"
        return url
    except NoCredentialsError:
        logging.error("AWS 자격 증명이 제공되지 않았습니다.")
        raise HTTPException(status_code=500, detail="AWS 자격 증명이 제공되지 않았습니다.")
    except Exception as e:
        logging.error(f"오류 발생: {str(e)}")
        raise HTTPException(status_code=500, detail=f"오류 발생: {str(e)}")
