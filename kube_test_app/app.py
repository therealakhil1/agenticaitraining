import uvicorn
from fastapi import FastAPI
from DbConnector import DBConnector

app = FastAPI(title="Interview Agent API")
@app.get("/")
async def root():
    return {'hello':'world from akhil on 10th may'}

@app.get("/add_person")
async def add_person():
    DB_connector = DBConnector()
    conn = DB_connector.get_connection()
    cursor = conn.cursor()
    ensure_default_table(conn)

    cursor.execute(f"SELECT IFNULL(MAX(id), 0) FROM `people_table`")
    max_id = cursor.fetchone()[0]
    new_id = max_id + 1

    query = f'INSERT VALUES ({new_id}, person) INTO people_table;'
    cursor.execute(query)

    print(f'A new new row with id {new_id} was inserted into the database')

@app.get("/healthz", tags=["health"])
async def healthz():
    """
    Simple liveness/readiness check.
    Returns HTTP 200 if the app is up.
    """
    return {"status": "healthy"}

def ensure_default_table(conn):
    """
    If the database has no tables at all, create a default table with:
      - id (PK, auto-increment)
      - name (VARCHAR)
      - created_at (timestamp)
    """
    cursor = None
    try:
        cursor = conn.cursor()

        # 1. Check how many tables exist in this schema
        cursor.execute("SHOW TABLES")
        all_tables = cursor.fetchall()    # list of tuples

        if not all_tables:
            # 2. No tables found ⇒ create your default one
            create_sql = f"""
            CREATE TABLE `people_table` (
              id INT AUTO_INCREMENT PRIMARY KEY,
              name VARCHAR(255) NOT NULL,
            )
            """
            cursor.execute(create_sql)
            conn.commit()
            print(f" Created default table `people_table`")
        else:
            print("ℹTables already exist:", [t[0] for t in all_tables])

    except Exception as e:
        print("❌ Database error:", e)
        if conn:
            conn.rollback()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)