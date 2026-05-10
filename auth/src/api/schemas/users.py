from datetime import date
import re
from uuid import UUID

from pydantic import EmailStr, SecretStr, field_validator
from pydantic import BaseModel, ConfigDict

from database.postgres.models.user_roles import UserRoles

ALLOWED_EMAIL_DOMAINS = {
    "gmail.com",
    "yandex.ru",
    "mail.ru",
    "icloud.com",
}


class RequestUsers(BaseModel):
    email: EmailStr
    lastname: str
    firstname: str
    middle_name: str | None = None
    date_of_birth: date
    password: SecretStr

    @field_validator("email")
    @classmethod
    def validate_email_domain(cls, value: EmailStr) -> EmailStr:
        domain = str(value).split("@")[-1].lower()

        if domain not in ALLOWED_EMAIL_DOMAINS:
            raise ValueError(
                "Домен электронной почты должен быть одним из следующих: "
                "gmail.com, yandex.ru, mail.ru, icloud.com"
            )

        return value

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: SecretStr) -> SecretStr:
        password = value.get_secret_value()

        if len(password) < 8:
            raise ValueError("Пароль должен содержать минимум 8 символов")

        if not re.search(r"[A-Z]", password):
            raise ValueError("Пароль должен содержать хотя бы одну заглавную букву")

        if not re.search(r"[a-z]", password):
            raise ValueError("Пароль должен содержать хотя бы одну строчную букву")

        if not re.search(r"\d", password):
            raise ValueError("Пароль должен содержать хотя бы одну цифру")

        if not re.search(r"[!@#$%^&*()_+{}\[\]:;<>,.?~\\/-]", password):
            raise ValueError("Пароль должен содержать хотя бы один специальный символ")

        return value


class ResponseUsers(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    email: EmailStr
    lastname: str
    firstname: str
    middle_name: str | None
    date_of_birth: date
    role: UserRoles

class UpdateUserRoleRequest(BaseModel):
    role: UserRoles
