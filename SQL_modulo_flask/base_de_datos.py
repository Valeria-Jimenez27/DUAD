import psycopg2

class PgManager:
    def __init__(self, db_name, user, password, host, port=5432):
        try:
            self.connection = psycopg2.connect(
                dbname=db_name,
                user=user,
                password=password,
                host=host,
                port=port
            )
            self.cursor = self.connection.cursor()
            print("Connection created successfully")
        except Exception as e:
            print("Error connecting to the database:", e)
            self.connection = None
            self.cursor = None

    def execute(self, query, params=None, fetch=False):
        if not self.cursor:
            print("No database connection")
            return None
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            result = self.cursor.fetchall() if fetch else None
            self.connection.commit()
            return result
        except Exception as e:
            print("Error executing query:", e)
            return None

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("Connection closed")

