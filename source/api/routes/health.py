from fastapi import APIRouter, status

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK)
def home():
    return {"message": "Fire-Control-API is running!"}


@router.get("/health", status_code=status.HTTP_200_OK)
def health():
    return {"message": "Fire-Control-API is running!"}
