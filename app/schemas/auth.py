from pydantic import BaseModel, Field

class Token(BaseModel):
    access_token: str
    token_type: str


class LoginRequest(BaseModel):
    username: str = Field(
        ...,
        description="Nome de usuário para autenticação",
        json_schema_extra={"examples": ["medico_01"]},
    )
    password: str = Field(
        ...,
        description="Senha do usuário",
        json_schema_extra={"examples": ["SenhaSegura123!"]},
    )
