def upload_to_s3(file):
    pass


def download_from_s3(file):
    pass



def validate_image(image):
    if not image.endswith('.png' or '.jpg') or image.size >500000:
        return None
    return image

def validate_book(book):
    if  not book.endswith('.pdf' or '.docx') or book.size > 500000:
        return None
    return book
