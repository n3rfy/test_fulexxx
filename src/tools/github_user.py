from typing import List, Dict 
import sys
from datetime import time, datetime

import aiohttp
import sqlalchemy as sa
from sqlalchemy import select, insert, delete, update
from sqlalchemy.future import Engine

from src.user.models import StatsAddV1
from src.database import tables
from src import logger

URLGIT = "https://api.github.com/users/{login}/repos"

class GitHub:
    """Class for parsing"""
    
    def __init__(self, engine: Engine) -> None:
        self._engine = engine
  
    def get_all_login_users(self) -> Dict:
        """Get all github {id: login} in database"""

        query = select(tables.users.c.login, tables.users.c.id)
        with self._engine.connect() as connection:
            users_login = connection.execute(query)
        return { t_login[1]: t_login[0] for t_login in users_login }
    
    def push_stats_users_in_database(self, stats_r: StatsAddV1) -> None:
        """Create and update stats repo"""

        instance_q = select(tables.stats).where(
                    tables.stats.c.repo_id==stats_r.repo_id,
                    tables.stats.c.user_id==stats_r.user_id,
                )
        with self._engine.connect() as connection:
            repo = connection.execute(instance_q).fetchall()
        if repo:
            # update repo if new stats
            if StatsAddV1(**repo[0]) == stats_r:
                logger.info(f"repo_id({stats_r.repo_id}) is defoult)")
                return
            query = update(tables.stats).where(
                    tables.stats.c.repo_id == stats_r.repo_id
                    ).values(**stats_r.dict())
            with self._engine.connect() as connection:
                connection.execute(query)
                connection.commit()
            logger.info(f"repo_id({stats_r.repo_id}) is update)")
            return     
        # else create stats
        query = insert(tables.stats).values(**stats_r.dict())
        with self._engine.connect() as connection:
            connection.execute(query)
            connection.commit()
        logger.info(f"repo_id({stats_r.repo_id}) is add)")

    @staticmethod
    async def get_stats_user_by_login(id_user, login: str) -> List[StatsAddV1]:
        """Get all info about repos by user"""

        async with aiohttp.ClientSession() as session:
            async with session.get(URLGIT.format(login=login)) as r:
                return [ 
                            StatsAddV1(
                                user_id=id_user,
                                repo_id=res.pop('id'),
                                date=res.pop('created_at'),
                                stargazers=res.pop('stargazers_count'),
                                **res,
                            ) for res in await r.json()
                       ]
    
