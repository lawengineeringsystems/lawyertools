from fastapi import FastAPI
from it.router import router as it_router

app = FastAPI()
app.include_router(it_router)
