from fastapi import FastAPI

from app.core.exceptions import CustomException
from app.core.exception_handlers import custom_exception_handler

app = FastAPI()

app.add_exception_handler(CustomException, custom_exception_handler)


@app.get("/")
def index():
    return "Hello world!"
