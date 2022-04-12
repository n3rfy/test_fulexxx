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
    github = GitHub(engine)
    login_users = github.get_all_login_users()
    for login in login_users:
         print(await github.get_stats_user_by_login(login))

if __name__ == "__main__":
    try:
        asyncio.run(
            main()
        )
    except KeyboardInterrupt:
        pass
