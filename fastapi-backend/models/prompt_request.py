from pydantic import BaseModel

class PromptRequest(BaseModel):
    request : str