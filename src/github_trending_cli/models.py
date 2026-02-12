from dataclasses import dataclass
from typing import Any

from pydantic import BaseModel, ConfigDict, HttpUrl, field_validator


# class for repos
@dataclass(frozen=True, slots=True)
class Repo:
    full_name: str
    stars: int
    url: str
    description: str | None = None
    language: str | None = None
    topics: tuple[str, ...] = ()


class RepoAPIModel(BaseModel):
    model_config = ConfigDict(extra="allow")
    full_name: str
    stargazers_count: int = 0
    html_url: HttpUrl
    description: str | None = None
    language: str | None = None
    topics: list[str] = []

    @field_validator("topics", mode="before")
    @classmethod
    def normalize_topics(cls, v):
        if v is None:
            return []
        if isinstance(v, (list, tuple)):
            return [str(x) for x in v if x is not None]
        return []


def repo_from_api(item: dict[str, Any]) -> Repo:
    m = RepoAPIModel.model_validate(item)

    return Repo(
        full_name=m.full_name,
        stars=m.stargazers_count,
        url=str(m.html_url),
        description=m.description,
        language=m.language,
        topics=tuple(m.topics),
    )
