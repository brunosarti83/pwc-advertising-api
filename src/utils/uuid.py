import uuid

def generate_prefixed_uuid(prefix: str) -> str:
    return f"{prefix}_{str(uuid.uuid4())}"