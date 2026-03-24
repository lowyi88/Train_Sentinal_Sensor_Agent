
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END

from agents.tech import Tech
from state import State
from agents import Train, Crowd
from nodes import (
    check_DB_exit_condition,
    check_crowd_exit_condition,
    check_tech_exit_condition,
    check_train_exit_condition,
    db_writer,
    human_node,
    check_exit_condition
)

#load_dotenv(override=True)  # Override, so it would use your local .env file
load_dotenv(dotenv_path="C:\\Users\\yi_li\\OneDrive\\Desktop\\sensorAgent\\.env_template")

def build_graph():
    """
    Build the LangGraph workflow.
    """

    builder = StateGraph(State)

    builder.add_node("human", human_node)
    builder.add_node("Train", Train)
    builder.add_node("Crowd", Crowd)
    builder.add_node("Tech", Tech)
    builder.add_node("DB", db_writer)

    # Edges
    builder.add_edge(START, "human")

    builder.add_conditional_edges(
        "human",
        check_exit_condition,
        {
            "Train": "Train",
            "END": END
        }
    )

    builder.add_conditional_edges(
        "Train",
        check_train_exit_condition,
        {
            "Crowd": "Crowd",
            "END": END  
        }
    )

    builder.add_conditional_edges(
        "Crowd",
        check_crowd_exit_condition,
        {
            "Tech": "Tech",
            "END": END
        }
    )

    builder.add_conditional_edges(
        "Tech",
        check_tech_exit_condition,
        {
            "DB": "DB",
            "END": END 
        }
    )

    builder.add_conditional_edges(
        "DB",
        check_DB_exit_condition,
        {
            "Train": "Train",
            "END": END 
        }
    )

    return builder.compile()

def main():
    print("=== SINGAPORE train management system ===")
    graph = build_graph()

    print(graph.get_graph().draw_mermaid())

    initial_state = State(
        volley_msg_left=0,
        train_status = "",
        crowd_status = ""
    )

    try:
        graph.invoke(initial_state)
    except KeyboardInterrupt:
        print("\n\nSystem interrupted. Goodbye!")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        print("Ending System...")

if __name__ == "__main__":
    main()
