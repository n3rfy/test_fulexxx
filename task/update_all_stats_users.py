import sys
sys.path = ['', '..'] + sys.path[1:]

import asyncio
import sqlalchemy as sa

from src.database import DatabaseSettings, create_database_url
from src.tools.github_user import GitHub

db_settings = DatabaseSettings()
engine = sa.create_engine(
        create_database_url(db_settings),
        future=True
)

async def main():
    """Task update stats all users in database"""

    github = GitHub(engine)
    users = github.get_all_login_users()
    for id_user, login in users.items():
        all_stats_rep = await github.get_stats_user_by_login(id_user, login)
        for stats_rep in all_stats_rep:
            github.push_stats_users_in_database(stats_rep)

if __name__ == "__main__":
    asyncio.run(main())
