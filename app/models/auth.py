from pydantic import BaseModel


class login_request(BaseModel):
    username: str
    password: str


class auth_response(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str


class token_model(BaseModel):
    access_token: str
    token_type: str


class token_data(BaseModel):
    username: str
    roles: list
    scope: list[str] = []
