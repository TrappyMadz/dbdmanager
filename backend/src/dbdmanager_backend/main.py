from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from .config import get_settings
from .routers import patchnotes
from .errors import validation_exception_handler


app = FastAPI()

app.include_router(patchnotes.router)

app.add_exception_handler(RequestValidationError, validation_exception_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=get_settings().cors_origins,
    allow_methods=["GET", "POST", "PATCH", "DELETE"],
    allow_headers=["Content-Type"],
)

@app.get("/health", tags=["Health"])
async def health():
    return {"code":200,"message":"healthy !"}

