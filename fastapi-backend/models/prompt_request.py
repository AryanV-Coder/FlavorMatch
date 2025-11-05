from pydantic import BaseModel

class PromptRequest(BaseModel):
    request : str
    family_name : str
    member_name : str