import json

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from src.container import MainContainer
from src.routes.accounts import router as account_router
from src.routes.documents import router as document_router
from src.routes.structures import router as structure_router
from src.settings import settings

main_container = MainContainer()


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOW_ORIGINS,
    allow_methods=["*"],
    allow_headers=["Authorization", "Content-Type", "Range"],
    allow_credentials=True,
    expose_headers=["Content-Range"],
)


@app.get("/health")
def health():
    return {"message": "OK"}


app.container = main_container
app.include_router(structure_router)
app.include_router(document_router)
app.include_router(account_router)
