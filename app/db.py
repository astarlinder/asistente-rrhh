import psycopg

from app.config import settings


def get_conn() -> psycopg.Connection:
    return psycopg.connect(settings.db_url)