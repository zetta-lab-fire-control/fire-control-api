from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def health():
    return {"message": "Fire-Control-API is running!"}
