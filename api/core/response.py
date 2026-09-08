from typing import Any


def success_response(
    data: Any = None,
    message: str = "Request successful",
    status_code: int = 200
):
    return {
        "status": "success",
        "statusCode": status_code,
        "message": message,
        "data": data
    }


def error_response(
    message: str = "Something went wrong",
    status_code: int = 500,
    data: Any = None
):
    return {
        "status": "error",
        "statusCode": status_code,
        "message": message,
        "data": data
    }