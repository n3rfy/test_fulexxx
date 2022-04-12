from datetime import datetime
from typing import List

from sqlalchemy import select, insert, delete
from sqlalchemy.future import Engine
from fastapi import HTTPException

from src.database import tables
from src.user.models import (
    UserResponseV1, 
    UserAddRequestV1,
    UserStatsResponseV1,
    StatsResponseV1,
)


class UserService:
    def __init__(self, engine: Engine) -> None:
        self._engine = engine

    def get_all_users(self) -> List[UserResponseV1]:
        query = select(tables.users)
        with self._engine.connect() as connection:
            users_data = connection.execute(query)
        users = []
        for user_data in users_data:
            user = UserResponseV1(
                id=user_data['id'],
                login=user_data['login'],
                name=user_data['name']
            )
            users.append(user)
        return users

    def get_user_by_id(self, id: int) -> UserResponseV1:
        query = select(tables.users).where(tables.users.c.id == id)
        with self._engine.connect() as connection:
            user_data = connection.execute(query)
        user = UserResponseV1(
            id=user_data['id'],
            login=user_data['login'],
            name=user_data['name']
        )
        return user

    def add_user(self, user: UserAddRequestV1) -> None:
        query = insert(tables.users).values(
            id=user.id,
            login=user.login,
            name=user.name
        )
        with self._engine.connect() as connection:
            connection.execute(query)
            connection.commit()

    def delete_user_by_id(self, id: int) -> None:
        query = delete(tables.users).where(tables.users.c.id == id)
        with self._engine.connect() as connection:
            connection.execute(query)
            connection.commit()

    def get_stats_user_by_id(
        self,
        id: int,
        date_from: datetime, 
        date_to: datetime,
    ) -> UserStatsResponseV1:
        query = select(
                    tables.users,
                    tables.stats,
                ).select_from(
                    tables.users.join(tables.stats)
                ).where(
                    tables.users.c.id == id and 
                    date_from < tables.stats.c.date < date_to
                )
        with self._engine.connect() as connection:
            user_data = connection.execute(query)
        user_data = [ dict(user) for user in user_data ]
        if not user_data:
            raise HTTPException(status_code=404, detail="Item not found")
        return UserStatsResponseV1(
            user=UserResponseV1(**user_data[0]),
            stats=[ 
                        StatsResponseV1(
                            date = str(stats.pop('date')),
                            **stats
                        ) for stats in user_data 
                  ],
        )
    
