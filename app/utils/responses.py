from fastapi import Response


def created_response(data: dict) -> Response:
    return {"status": "created", "data": data}
