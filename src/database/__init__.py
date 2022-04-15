from src.core.settings import DatabaseSettings


def create_database_url(settings: DatabaseSettings = None) -> str:
    if not settings:
        settings = DatabaseSettings()
    return (f'postgresql+psycopg2://'
            f'{settings.username}:{settings.password}@'
            f'{settings.host}:{settings.port}/{settings.database}')
