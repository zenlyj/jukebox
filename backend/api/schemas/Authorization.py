from pydantic import BaseModel
from typing import Literal


class AuthorizationBase(BaseModel):
    pass


class AuthorizationCreate(AuthorizationBase):
    grant_type: Literal["authorization_code"]
    authorization_code: str


class AuthorizationRefresh(AuthorizationBase):
    grant_type: Literal["refresh_token"]
    access_token: str
    refresh_token: str
