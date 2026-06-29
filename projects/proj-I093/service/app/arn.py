import uuid


def generate_arn() -> str:
    # Simple short ARN using uuid4 hex
    return f"ARN-{uuid.uuid4().hex[:12].upper()}"
