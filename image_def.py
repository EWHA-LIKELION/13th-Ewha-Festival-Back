from django.conf import settings
import boto3
from PIL import Image as pil, ImageOps
from io import BytesIO
import os

class ImageProcessing:
    ## 이미지 압축 함수    
    ## S3 업로드 함수

    MAX_FILE_SIZE = 2 * 1024 * 1024  # 최대 파일 크기 2MB
    MAX_WIDTH = 1440  # 최대 해상도 너비
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
            compressed_file.seek(0)

        except Exception as e:
            print(f"이미지 압축 실패: {e}")
            upload_file.seek(0)
            compressed_file = upload_file #압축 실패 시 원본 파일 그대로 업로드

        s3 = boto3.resource('s3', 
                            region_name=region_name, 
                            aws_access_key_id=settings.AWS_S3_ACCESS_KEY_ID, 
                            aws_secret_access_key=settings.AWS_S3_SECRET_ACCESS_KEY)
        try: 
            s3.Bucket(bucket_name).put_object(
                Key=upload_file_path_name, 
                Body=compressed_file, 
                ContentType=content_type)
        
            return f"https://s3-{region_name}.amazonaws.com/{bucket_name}/{bucket_path}/{file_name}"
        
        except Exception as e:
            print(f"S3 업로드 실패: {e}")
            return None
    
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

            #코드 추가 -> 리사이징 수행(파일 크기 초과 또는 해상도 초과 시)
            src_width, src_height = img.size
            file_size = upload_file.size
            if file_size > ImageProcessing.MAX_FILE_SIZE or min(src_width, src_height) > ImageProcessing.MAX_WIDTH:
                if src_width > src_height:
                    dst_width = ImageProcessing.MAX_WIDTH
                    dst_height = int((src_height / src_width) * dst_width)
                else:
                    dst_height = ImageProcessing.MAX_WIDTH
                    dst_width = int((src_width / src_height) * dst_height)

                # LANCZOS 필터를 사용해 리사이징
                img = img.resize((dst_width, dst_height), pil.LANCZOS)

            output = BytesIO()

            if img_format == "PNG":
                img.save(output, format="PNG", optimize=True)
            elif img_format in ["JPEG", "JPG"]:
                img = img.convert("RGB")
                img.save(output, format="JPEG", quality=90, optimize=True, progressive=True)
                # 파일 크기 초과 시 압축 품질 동적 조정
                # 파일 크기가 크면 품질을 85로 낮춤 → 크기가 작으면 90 유지
                quality = 85 if file_size > ImageProcessing.MAX_FILE_SIZE else 90
                img.save(output, format="JPEG", quality=quality, optimize=True, progressive=True)

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