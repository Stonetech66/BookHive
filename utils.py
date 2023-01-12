



def validate_image(image):
    if not image.endswith('.png' or '.jpg') or image.size >500000:
        return None
    return image

def validate_book(book):
    if  not book.endswith('.pdf' or '.docx') or book.size > 500000:
        return None
    return book
