from fastapi import APIRouter
from app.schemas.health import HealthResponse, MessageRequest, MessageResponse
from app.services.hello_service import generate_hello_message

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health_check():
    return {"status": "ok"}


@router.post("/hello", response_model=MessageResponse)
def say_hello(data: MessageRequest):
    message = generate_hello_message(data.name)

    return {
        "message": message
    }