from datetime import date
from uuid import UUID

from pydantic import BaseModel, EmailStr


class AuthorizedUser(BaseModel):
    id: UUID
    email: EmailStr
    lastname: str
    firstname: str
    middle_name: str | None
    date_of_birth: date
    role: str
