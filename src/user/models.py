from datetime import date, datetime
from typing import List

from pydantic import BaseModel, Field, validator

class UserResponseV1(BaseModel):
    id: int = Field(..., ge=1)
    login: str
    name: str

class UserAddRequestV1(BaseModel):
    id: int = Field(..., ge=1)
    login: str
    name: str

class StatsResponseV1(BaseModel):
    repo_id: int
    date: str 
    stargazers: int
    forks: int 
    watchers: int 

    @validator("date", pre=True)
    def parse_date(cls, value):
        if type(value) is date:
            return datetime.strftime(value, "%Y-%m-%d")
        return value

class StatsAddV1(BaseModel):
    user_id: int
    repo_id: int
    date: date
    stargazers: int
    forks: int 
    watchers: int 

    @validator("date", pre=True)
    def parse_date(cls, value):
        if type(value) is datetime:
            return value.date()
        if type(value) is date:
            return value
        return datetime.strptime(
            value,
            "%Y-%m-%dT%H:%M:%SZ"
        ).date()

class UserStatsResponseV1(BaseModel):
    user: UserResponseV1
    stats: List[StatsResponseV1]
