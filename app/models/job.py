from pydantic import BaseModel

class JobRequest(BaseModel):
    filename: str
    operation: str

class UploadURLRequest(BaseModel):
    filename: str