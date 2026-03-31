from fastapi import APIRouter

router = APIRouter(tags=["status"], prefix="/health")


@router.get("/")
def health():
    return {"message": "Fire-Control-API is running!"}
