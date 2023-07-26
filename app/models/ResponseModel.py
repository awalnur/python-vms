from typing import Any

from pydantic import BaseModel


class success_response(BaseModel):
    status_code: int
    detail: str

class response_data(BaseModel):
    status_code: int
    data: Any | dict
