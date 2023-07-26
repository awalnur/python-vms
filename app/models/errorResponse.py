from pydantic import BaseModel



class ErrorResponse(BaseModel):
    """A class representing an error response.

        Attributes:
            detail (str): A detailed description of the error.
            code (int): The error code.
    """

    detail: str
    code: int
