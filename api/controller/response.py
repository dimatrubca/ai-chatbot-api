from pydantic import BaseModel

class ModelDetails(BaseModel):
    id_model: str
    type_model: str