import psycopg2

DB_CONFIG = {
    'dbname': 'uchet_db',
    'user': 'postgres',
    'password': '223344',
    'host': 'localhost',
    'port': '5432'
}

def get_connection():
    """Устанавливает и возвращает соединение с базой данных."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except psycopg2.OperationalError as e:
        print(f"Ошибка подключения к базе данных: {e}")
        return None