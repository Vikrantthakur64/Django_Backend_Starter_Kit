import uuid
from django.utils.crypto import get_random_string

def generate_unique_filename(filename):
    name, ext = os.path.splitext(filename)
    unique_filename = f"{uuid.uuid4()}{ext}"
    return unique_filename

def generate_otp(length=6):
    return get_random_string(length=length, allowed_chars='0123456789') 