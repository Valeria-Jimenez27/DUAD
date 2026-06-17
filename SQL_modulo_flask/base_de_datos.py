import psycopg2
from psycopg2.extras import RealDictCursor


class PgManager:
    def __init__(self, db_name, user, password, host, port=5432):
        self.db_config = {
            "dbname": db_name,
            "user": user,
            "password": password,
            "host": host,
            "port": port
        }

    def get_connection(self):
        return psycopg2.connect(**self.db_config)

    def execute(self, query, params=None, fetch=False):
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute(query, params)
            result = cursor.fetchall() if fetch else None
            conn.commit()
            cursor.close()
            return result
        except Exception as e:
            if conn:
                conn.rollback()
            raise e
        finally:
            if conn:
                conn.close()

db = PgManager(
    db_name="postgres",
    user="postgres",
    password="postgres",
    host="localhost"
)





