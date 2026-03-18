from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health():
    return {"message": "Fire-Control-API is running!"}


@router.get("/")
def home():
    return {"message": "Fire-Control-API is running!"}
