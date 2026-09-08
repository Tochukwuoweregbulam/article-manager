from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from api.core.response import error_response


async def http_exception_handler(
    request: Request,
    exc: StarletteHTTPException
):
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response(
            message=str(exc.detail),
            status_code=exc.status_code
        )
    )


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    return JSONResponse(
        status_code=422,
        content=error_response(
            message="Validation error",
            status_code=422,
            data=exc.errors()
        )
    )


async def general_exception_handler(
    request: Request,
    exc: Exception
):
    return JSONResponse(
        status_code=500,
        content=error_response(
            message="Internal server error",
            status_code=500
        )
    )