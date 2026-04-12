from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str


class MessageRequest(BaseModel):
    name: str

class MessageResponse(BaseModel):
    message: str