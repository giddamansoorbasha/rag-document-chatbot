from pydantic import BaseModel
from datetime import datetime

class DocumentResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    filename: str
    collection_name: str
    created_at: datetime