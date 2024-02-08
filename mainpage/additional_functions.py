import uuid

def generate_random_code():
    return uuid.uuid4().hex[:6].upper()