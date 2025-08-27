def serialize_message(msg):
    return {
        "role": getattr(msg, "role", "unknown"),
        "content": getattr(msg, "content", str(msg))
    }