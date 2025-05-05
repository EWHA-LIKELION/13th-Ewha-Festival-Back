import logging
from django.conf import settings
import boto3
from PIL import Image as pil, ImageOps
from io import BytesIO
import re

class ImageProcessing:
    MAX_FILE_SIZE = 2 * 1024 * 1024  # 최대 파일 크기 2MB
    MAX_WIDTH = 1440  # 최대 해상도 너비

    @staticmethod
    def s3_file_upload_by_file_data(upload_file, bucket_path, file_name, content_type=None, extension=None):
        region_name = settings.AWS_S3_REGION_NAME
        bucket_name = settings.AWS_STORAGE_BUCKET_NAME
        file_name = re.sub(r'[^a-zA-Z0-9가-힣._-]', '', file_name)

        
        content_type = content_type or upload_file.content_type
        extension = extension or upload_file.name.split('.')[-1]
        upload_file_path_name = f"{bucket_path}/{file_name}"

        print(f"📂 파일 업로드 시작: {file_name}")
        print(f"▶ 원본 파일 크기: {upload_file.size / 1024:.2f} KB")
        print(f"▶ 원본 파일 타입: {content_type}")

        try:
            # 이미지 압축 (모든 포맷을 JPEG로 통일)
            compressed_file = ImageProcessing.compress_image(upload_file)
            compressed_file.seek(0)

            compressed_file_size = len(compressed_file.getvalue()) 
            print(f"압축 완료: 압축 후 파일 크기 {compressed_file_size / 1024:.2f} KB")

        except Exception as e:
            print(f"이미지 압축 실패: {e}")
            upload_file.seek(0)
            compressed_file = BytesIO(upload_file.read()) 

        s3 = boto3.resource('s3',
                            region_name=region_name,
                            aws_access_key_id=settings.AWS_S3_ACCESS_KEY_ID,
                            aws_secret_access_key=settings.AWS_S3_SECRET_ACCESS_KEY)
        try:
            s3.Bucket(bucket_name).put_object(
                Key=upload_file_path_name,
                Body=compressed_file,
                ContentType='image/jpeg'  # ✅ 통일된 포맷으로 저장
            )

            print(f"S3 업로드 성공: {file_name}")
            return f"https://{bucket_name}.s3.{region_name}.amazonaws.com/{bucket_path}/{file_name}"

        except Exception as e:
            print(f"S3 업로드 실패: {e}")
            return None
    
    @staticmethod
    def compress_image(upload_file):
        try:
            img = pil.open(upload_file)
            src_width, src_height = img.size
            file_size = upload_file.size
            
            print(f"원본 해상도: {src_width}x{src_height}")
            print(f"원본 파일 크기: {file_size / 1024:.2f} KB")

            # ✅ EXIF 회전 보정
            try:
                img = ImageOps.exif_transpose(img)
            except Exception:
                pass

            # ✅ 포맷이 None일 경우 확장자로 보완
            img_format = img.format or upload_file.name.split('.')[-1].upper()

            # ✅ PNG의 경우 JPEG로 변환 (투명도 제거)
            if img_format == "PNG":
                # 투명도를 흰색 배경으로 채움
                img = img.convert("RGBA")
                background = pil.new("RGB", img.size, (255, 255, 255))  # 흰색 배경 생성
                background.paste(img, mask=img.split()[3])  # 투명 부분 흰색 채우기
                img = background
                img_format = "JPEG"  # ✅ 포맷을 JPEG로 통일

            # ✅ 리사이징 수행 (파일 크기 초과 또는 해상도 초과 시)
            if file_size > ImageProcessing.MAX_FILE_SIZE or max(src_width, src_height) > ImageProcessing.MAX_WIDTH:
                if src_width > src_height:
                    dst_width = ImageProcessing.MAX_WIDTH
                    dst_height = int((src_height / src_width) * dst_width)
                else:
                    dst_height = ImageProcessing.MAX_WIDTH
                    dst_width = int((src_width / src_height) * dst_height)

                print(f"리사이징 수행: {src_width}x{src_height} → {dst_width}x{dst_height}")
                img = img.resize((dst_width, dst_height), pil.LANCZOS)

            output = BytesIO()

            # ✅ JPEG 저장 시 품질 고정 + 최적화 제거
            img = img.convert("RGB")
            img.save(output, format="JPEG", quality=70)  # ✅ 통일된 포맷으로 저장

            output.seek(0)

            compressed_size = len(output.getvalue())
            print(f"압축 후 파일 크기: {compressed_size / 1024:.2f} KB")

            return output

        except Exception as e:
            print(f"이미지 압축 실패: {e}")
            upload_file.seek(0)
            return BytesIO(upload_file.read())

    @staticmethod
    def s3_file_delete(bucket_path, file_name):
        s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_S3_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_S3_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME
        )
        key = f"{bucket_path}/{file_name}"
        try:
            s3_client.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=key)
            print(f"S3 파일 삭제 완료: {file_name}")
        except Exception as e:
            print(f"S3 파일 삭제 실패: {e}")
