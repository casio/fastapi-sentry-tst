from pydantic import BaseModel, Field


class EntryResponse(BaseModel):
    api: str = Field(alias="API")
    description: str = Field(alias="Description")
    auth: str | None = Field("default", alias="Auth")
    https: bool = Field(alias="HTTPS")
    cors: str | None = Field("default", alias="Cors")
    link: str | None = Field("default", alias="Link")
    category: str | None = Field("default", alias="Category")


class PublicAPIsResponse(BaseModel):
    count: int
    entries: list[EntryResponse]
