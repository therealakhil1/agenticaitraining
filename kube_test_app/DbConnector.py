import os
from mysql.connector import pooling, Error

class DBConnector:
    def __init__(self):
        # Base config
        db_config = {
            "host":     os.getenv("DB_HOST", "127.0.0.1"),
            "port":     int(os.getenv("DB_PORT", 8080)),
            "user":     os.getenv("DB_USER", "root"),
            "database": os.getenv("DB_NAME", "kube_test_app_db"),
        }

        # Only include a password if one was provided
        pwd = os.getenv("DB_PASSWORD")
        if pwd is not None and pwd != "":
            db_config["password"] = pwd

        # Create the pool exactly as before
        try:
            self.pool = pooling.MySQLConnectionPool(
                pool_name    = "mypool",
                pool_size    = int(os.getenv("DB_POOL_SIZE", 5)),
                **db_config
            )
        except Error as e:
            raise RuntimeError(f"Error creating MySQL connection pool: {e}")

    def get_connection(self):
        return self.pool.get_connection()

    def close_connection(self, conn):
        conn.close()