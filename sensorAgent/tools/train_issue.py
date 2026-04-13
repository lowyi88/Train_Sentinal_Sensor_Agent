import json

import psycopg2
from pydantic import BaseModel, ValidationError


class Record(BaseModel):
    train_id: str
    technical: str
    expected_resolve: str
    remarks: str


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
    safe_records = []
    for r in rows:
        try:
            rec = Record(train_id=r[0], technical=r[1], expected_resolve=r[2], remarks=r[3])
            safe_records.append(rec.dict())
        except ValidationError:
            continue  # skip unsafe rows


    conn.close()
    return json.dumps(safe_records, indent=2)



     
