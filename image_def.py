from django.conf import settings
import boto3

class ImageProcessing:
    ## 이미지 압축 함수

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

        s3 = boto3.resource('s3', region_name=region_name, aws_access_key_id=settings.AWS_S3_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_S3_SECRET_ACCESS_KEY)

        if s3.Bucket(bucket_name).put_object(Key=upload_file_path_name, Body=upload_file, ContentType=content_type) is not None:
            return f"https://s3-{region_name}.amazonaws.com/{bucket_name}/{bucket_path}/{file_name}"

        return False