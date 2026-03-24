import psycopg2
from typing import Literal
from state import State


def human_node(state: State) -> dict:
    user_input = int(input("\nvolley: ").strip())
    
    return {
        "volley_msg_left": user_input
    }


def check_exit_condition(state: State) -> Literal["Train", "END"]:
    volley_left = int(state.get("volley_msg_left", 0))

    if volley_left > 0:
        return "Train"
    else:
        return "END"

def check_train_exit_condition(state: State) -> Literal["Crowd", "END"]:
    volley_left = int(state.get("volley_msg_left", 0))

    if volley_left > 0:
        return "Crowd"
    else:
        return "END"

def check_crowd_exit_condition(state: State) -> Literal["Tech","END"]:
    volley_left = int(state.get("volley_msg_left", 0))

    if volley_left > 0:
        return "Tech"
    else:
        return "END"
    
def check_tech_exit_condition(state: State) -> Literal["DB", "END"]:
    volley_left = int(state.get("volley_msg_left", 0))

    if volley_left > 0:
        return "DB"
    else:
        return "END"
    
def check_DB_exit_condition(state: State) -> Literal["Train", "END"]:
    volley_left = int(state.get("volley_msg_left", 0))

    if volley_left > 0:
        return "Train"
    else:
        return "END"

def db_writer(state):
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="Password1",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()

    print (state)

    try:
        if "train_status" in state:
            if state["train_status"]:
                parts = state["train_status"].split(";")
                cursor.execute(
                    "INSERT INTO TRAIN (TECHNICAL, MEDICAL, ""TIME"") VALUES (%s, %s, %s)",
                    (parts[0], parts[1], parts[2])
                )
                conn.commit()

        if "crowd_status" in state:
            if state["crowd_status"]:
                parts = state["crowd_status"].split(";")
                cursor.execute(
                    "INSERT INTO PLATFORM (""TIME"", PASSENGER_COUNT, INCIDENT) VALUES (%s, %s, %s)",
                    (parts[0], parts[1], parts[2])
                )
                conn.commit()
        
    finally:
        conn.close()
    
    return {"volley_msg_left": -1}
