from django.conf import settings
import boto3
from PIL import Image as pil, ImageOps
from io import BytesIO
import os

class ImageProcessing:
    ## 이미지 압축 함수    
    ## S3 업로드 함수
    @staticmethod
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
            # 이미지 압축 (JPEG, PNG만 해당)
            compressed_file = ImageProcessing.compress_image(upload_file)

            upload_file.seek(0)
        except Exception:
            pass

        s3 = boto3.resource('s3', region_name=region_name, aws_access_key_id=settings.AWS_S3_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_S3_SECRET_ACCESS_KEY)

        if s3.Bucket(bucket_name).put_object(Key=upload_file_path_name, Body=upload_file, ContentType=content_type) is not None:
            return f"https://s3-{region_name}.amazonaws.com/{bucket_name}/{bucket_path}/{file_name}"

        return False
    
    @staticmethod
    def compress_image(upload_file):
        """
        이미지 압축 함수 (JPEG, PNG 지원)
        :param upload_file: 업로드할 파일
        :return: 압축된 이미지 데이터 (BytesIO)
        """
        try:
            img = pil.open(upload_file)

            # EXIF 회전 보정 (EXIF 데이터가 없으면 무시)
            try:
                img = ImageOps.exif_transpose(img)
            except Exception:
                pass

            img_format = img.format
            if img_format not in ["PNG", "JPEG", "JPG"]:
                raise ValueError("지원하지 않는 이미지 포맷입니다.")

            output = BytesIO()

            if img_format == "PNG":
                img.save(output, format="PNG", optimize=True)
            elif img_format in ["JPEG", "JPG"]:
                img = img.convert("RGB")
                img.save(output, format="JPEG", quality=90, optimize=True, progressive=True)

            output.seek(0)
            return output

        except Exception as e:
            print(f"이미지 압축 실패: {e}")
            upload_file.seek(0)
            return upload_file
    
    @staticmethod
    def s3_file_delete(bucket_path, file_name):
        s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_S3_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_S3_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME
        )
        key = f"{bucket_path}/{file_name}"
        s3_client.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=key)