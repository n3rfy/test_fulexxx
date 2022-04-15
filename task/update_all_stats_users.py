import sys
sys.path = ['', '..'] + sys.path[1:]

import asyncio
import sqlalchemy as sa

from src.database import DatabaseSettings, create_database_url
from src.tools.github_user import GitHub
from src import logger

engine = sa.create_engine(
        create_database_url(),
        future=True
)

async def update_stats_users():
    """Task update stats all users in database"""

    logger.info("Starting update repo!!!")
    github = GitHub(engine)
    users = github.get_all_login_users()
    for id_user, login in users.items():
        all_stats_rep = await github.get_stats_user_by_login(id_user, login)
        for stats_rep in all_stats_rep:
            github.push_stats_users_in_database(stats_rep)

    logger.info("Finish update repo!!!")

if __name__ == "__main__":
    asyncio.run(update_stats_users())
