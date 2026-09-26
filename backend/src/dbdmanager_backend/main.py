from fastapi import FastAPI
from .routers import patchnotes

app = FastAPI()

app.include_router(patchnotes.router)

@app.get("/")
async def health():
    return {"code":200,"message":"healthy !"}