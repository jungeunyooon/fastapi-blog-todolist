from fastapi import APIRouter, HTTPException
from app.logger import logger
from app.bucket.s3_client import client_s3  # 분리한 S3 클라이언트 불러오기

router = APIRouter(
    prefix="/api/v1/s3",
    tags=["S3Bucket"],
)

@router.get("/test-s3")
async def test_s3_connection():
    try:
        response = client_s3.list_buckets()
        buckets = [bucket['Name'] for bucket in response['Buckets']]
        return {"buckets": buckets}
    except Exception as e:
        logger.error(f"Failed to connect to S3: {e}")
        raise HTTPException(status_code=500, detail="Failed to connect to S3")
