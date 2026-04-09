from fastapi import APIRouter, status

router = APIRouter()


@router.post("/login", status_code=status.HTTP_200_OK)
def login():
    return True


@router.post("/logout", status_code=status.HTTP_200_OK)
def logout():
    return True


@router.post("/password-reset", status_code=status.HTTP_200_OK)
def reset_password():
    return True


@router.post("/password-request", status_code=status.HTTP_200_OK)
def request_password():
    return True
