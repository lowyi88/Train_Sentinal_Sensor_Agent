import psycopg2


def train_issue() -> str:
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="Password1",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()
    cursor.execute("select train_id, technical, expected_resolve, remarks from train order by id")
    rows = cursor.fetchall()
    results = [{"train_id": r[0], "technical": r[1], "expected_resolve":r[2], "remarks":r[3]} for r in rows]
    conn.close()
    return results



     
