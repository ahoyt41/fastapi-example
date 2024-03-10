from fastapi import FastAPI
from fastapi_example.router import user_router, score_router

app = FastAPI()

app.include_router(user_router)
app.include_router(score_router)
