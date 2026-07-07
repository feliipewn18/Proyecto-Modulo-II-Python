from pydantic import BaseModel, Field
from datetime import datetime

class TaskSchema(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = None
    priority: str = Field(pattern='^(low|medium|high)$')
    due_date: datetime

# YYYY-MM-DDTHH:MM:SS