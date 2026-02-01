"""FastAPI routes (v1) - minimal scaffold"""
from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health():
    return {"status": "ok"}


@router.post("/query")
def query(q: dict):
    return {"answer": "TODO: implement query"}
