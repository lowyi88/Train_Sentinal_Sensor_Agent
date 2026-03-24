import operator
from typing import Annotated, TypedDict



class State(TypedDict):
    """
    Overall state of the entire LangGraph system.
    """
    volley_msg_left: Annotated[int, operator.add]
    train_status: str
    crowd_status: str

    
