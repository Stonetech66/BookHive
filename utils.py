import boto3
import uuid
from django.conf import settings
from django.core.validators import validate_image_file_extension

s3_resource='p'
def format_file_name(name):
    return str(uuid.uuid4().hex[:6]+ name)


def upload_to_s3(file):
    try:
        file_name=format_file_name(file.name)
        file.name=file_name
        s3_resource.Bucket(settings.AWS_BUCKET_NAME).upload_file(FIlename=file, Key=file)
        return True
    except:
        return False
    

def validate_image(image):
    try:
        validate_image_file_extension(image)
        if image.size > settings.IMAGE_FILE_MAX_SIZE:
            return False
        return image
    except:
        return False


def validate_book(book):
    if  not book.endswith('.pdf' or '.docx') or book.size > settings.BOOK_FILE_MAX_SIZE:
        return False
    return book
