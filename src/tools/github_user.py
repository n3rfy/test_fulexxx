from typing import List, Set
import sys

import aiohttp
import sqlalchemy as sa
from sqlalchemy import select, insert, delete
from sqlalchemy.future import Engine

from src.user.models import StatsResponseV1
from src.database import tables

URLGIT = "https://api.github.com/users/{login}/repos"

class GitHub:
    """Class for parsing"""
    
    def __init__(self, engine: Engine) -> None:
        self._engine = engine
  
    def get_all_login_users(self) -> Set[str]:
        """Get all github login in database"""
        query = select(tables.users.c.login)
        with self._engine.connect() as connection:
            users_login = connection.execute(query)
        return set([ login[0] for login in users_login ])

    @staticmethod
    async def get_stats_user_by_login(login: str) -> List[StatsResponseV1]:
        """Get all info about repos by user"""
        async with aiohttp.ClientSession() as session:
            async with session.get(URLGIT.format(login=login)) as r:
                return [ 
                            StatsResponseV1(
                                repo_id=res.pop('id'),
                                date=res.pop('created_at'),
                                stargazers=res.pop('stargazers_count'),
                                **res,
                            ) for res in await r.json()
                       ]
    
