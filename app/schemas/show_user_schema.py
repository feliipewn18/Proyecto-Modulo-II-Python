from pydantic import BaseModel
from datetime import datetime

class ShowTaskInformation(BaseModel):
    id: int
    title: str
    description: str | None = None
    is_completed: bool
    priority: str
    due_date: datetime
    created_at: datetime

    class Config:
        from_attributes = True

class ShowAllUserInformation(BaseModel):
    id: int
    name: str
    last_name: str
    email: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    tasks: list[ShowTaskInformation] = []

    class Config:
        from_attributes = True