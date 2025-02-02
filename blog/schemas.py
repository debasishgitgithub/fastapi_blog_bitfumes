from pydantic import BaseModel


class Blog(BaseModel):
    name: str
    desc : str | None = None
