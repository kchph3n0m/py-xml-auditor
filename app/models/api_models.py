from pydantic import BaseModel
from typing import List, Optional

class ErrorDetail(BaseModel):
        line: Optional[int]
        element: str
        path: str
        message: str

class ValidationResponse(BaseModel):
        status: str
        total_errors: int
        errors: List[ErrorDetail]

