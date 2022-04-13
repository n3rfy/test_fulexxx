from datetime import date
from typing import List

from pydantic import BaseModel, Field

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

class StatsAddV1(BaseModel):
    user_id: int
    repo_id: int
    date: date
    stargazers: int
    forks: int 
    watchers: int 


class UserStatsResponseV1(BaseModel):
    user: UserResponseV1
    stats: List[StatsResponseV1]
