from enum import Enum
import logging
logger = logging.getLogger(__name__)
from fastapi.exceptions import RequestValidationError
from fastapi import Request
from fastapi.responses import JSONResponse


class DataBaseError(Enum):
    ROLLBACK_ERROR = "DATABASE_ROLLBACK_ERROR"
    CONNECTION_ERROR = "DATABASE_CONNECTION_ERROR"

class PatchNoteError(Enum):
    MISSING_ERROR = "PATCHNOTE_MISSING_ERROR"

class ApiError(Enum):
    VALIDATION_ERROR = "API_VALIDATION_ERROR"

async def validation_exception_handler(request : Request, exception : RequestValidationError):
    logger.warning(f"Wrong format : {exception.errors()} : {request.url}.")
    return JSONResponse(status_code=422, content={"detail":{"code": ApiError.VALIDATION_ERROR.value}})