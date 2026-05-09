from datetime import date
from uuid import UUID

from pydantic import EmailStr, SecretStr
from pydantic import BaseModel, ConfigDict


class RequestUsers(BaseModel):
    email: EmailStr
    lastname: str
    firstname: str
    middle_name: str | None = None
    date_of_birth: date
    password: SecretStr

class ResponseUsers(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    email: EmailStr
    lastname: str
    firstname: str
    middle_name: str | None
    date_of_birth: date
