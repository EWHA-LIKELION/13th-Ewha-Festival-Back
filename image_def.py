from django.conf import settings
import boto3
#새롭게 추가한 패키지 
from PIL import Image as pil, ImageOps
from io import BytesIO
import os

'''
무손실 압축
- 압축 방식: 불필요한 데이터를 제거
- 파일 크기 감소율: 낮음
- 이미지 품질: 원본과 100% 동일
- PNG는 원래 손실압축을 지원하지 않는다고함 

비교
- jpeg이미지를 빠르게 로딩하는 것이(속도가 중요한것이) 먼저면 손실압축
- 선명해야하는 이미지면 무손실 압축이 good

JPEG는 본질적으로 손실 압축 포맷이기 때문에 완전한 무손실 압축은 불가능하지만,
PNG 같은 포맷이라면 완전한 무손실 압축이 가능
PNG → 무손실 압축 적용 (optimize=True만 사용)
JPEG → 품질을 유지하면서도 크기를 줄이려면 quality=100으로 설정
'''
class ImageProcessing:
    @staticmethod
    ## 이미지 리사이징, 압축 함수(1440px 이하, 2MB 이하 유지)
    def compress_image(upload_file, width=1440, max_file_size=2 * 1024 * 1024):
        try:
            img = pil.open(upload_file)
            #EXIF(Exchangeable Image File Format) 데이터-> 회전 방향을 자동으로 보정
            img = ImageOps.exif_transpose(img)  # EXIF 회전 보정(어떤 기기에서 보더라도 회전이 제대로 된 이미지)
            img_format = img.format  # 원본 포맷 유지

            output = BytesIO()

            # PNG는 무손실 압축 적용
            if img_format == "PNG":
                #progressive=True 사용 (JPEG)
                img.save(output, format="PNG", optimize=True)

            # JPEG는 최소한의 손실 압축 (quality=100)
            elif img_format == "JPEG":
                img = img.convert("RGB")  # RGB 변환
                #100: 거의 무손실에 가깝지만, 파일 크기가 크다
                #JPEG 이미지를 점진적으로 로드하도록 저장하는 방식-> 웹에서 빠르게 로드
                img.save(output, format="JPEG", quality=90, optimize=True, progressive=True)

            else:
                # 다른 포맷은 원본 유지 -> 이래도 되나?? 
                upload_file.seek(0)
                return upload_file

            output.seek(0)
            return output
        
        except Exception as e:
            print(f"이미지 압축 실패: {e}")
            upload_file.seek(0)  # 원본 사용
            return upload_file
        

    @staticmethod
    ## S3 업로드 함수
    def s3_file_upload_by_file_data(upload_file, bucket_path, file_name, content_type=None, extension=None):
        region_name = settings.AWS_S3_REGION_NAME
        bucket_name = settings.AWS_STORAGE_BUCKET_NAME
        
        if content_type:
            content_type = content_type
        else:
            content_type = upload_file.content_type
        if extension:
            extension = extension
        else:
            extension = upload_file.name.split('.')[-1]

        upload_file_path_name = f"{bucket_path}/{file_name}"

        try:
            upload_file.seek(0)
        except Exception:
            pass

        s3 = boto3.resource('s3', region_name=region_name, 
                            aws_access_key_id=settings.AWS_S3_ACCESS_KEY_ID, 
                            aws_secret_access_key=settings.AWS_S3_SECRET_ACCESS_KEY)

        if s3.Bucket(bucket_name).put_object(Key=upload_file_path_name, Body=upload_file, ContentType=content_type) is not None:
            return f"https://s3-{region_name}.amazonaws.com/{bucket_name}/{bucket_path}/{file_name}"

        return False
    
    def s3_file_delete(bucket_path, file_name):
        s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_S3_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_S3_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME
        )
        key = f"{bucket_path}/{file_name}"
        s3_client.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=key)