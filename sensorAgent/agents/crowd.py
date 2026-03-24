
from tools import singapore_time
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
import re

def execute_tool(tool_name, content = "No topic"):
    """
    Execute a specific tool and return its output.
    Returns Tool output as string
    """
    tool_name = tool_name.lower().strip()

    if tool_name == "time":
        return singapore_time()
    else:
        return f"Unknown tool: {tool_name}"


def Crowd(state) -> dict:
    # System prompt for ReAct
    system_prompt = f"""you are singapore train platform

You run in a loop of Thought, Action, Observation.

Use Thought to achieve the goals set below:
-you would randomly return a time of the day
-you would randomly return a number passenger count representing waiting passenger in station
-you would randomly return medical emergenices of passenger on board, sometimes there is no medical emergencies

Your available actions are:

time:
Returns current time in Singapore


Example session:

Thought: I should check what time it is to frame my response
Action: time

You will be called again with:
Observation: Time in Singapore now: [Actual time returned after you call the tool, THIS IS NOT THE RIGHT TIME, call Action: time to get the actual time]

You must never try to guess the time Rely on the Observation that you will be called later on for the answers. You MUST NOT answer with those.

You then continue thinking or output:
Message: time;passenger count;medical emergenices 


IMPORTANT:
- You can use multiple actions by continuing the loop
- Once you have enough information, output Message: followed by your response 
- Only output time follow by ; follow by passenger count follow by ; follow by medical emergencies, 'NA' if none
"""

    # Internal loop for ReAct
    max_iterations = 5  # Prevent infinite loops
    internal_context = f"Continue the operation.\n"

    for iteration in range(max_iterations):
        user_prompt = internal_context

        try:
            llm = ChatOpenAI(model="gpt-5-mini", temperature=1)
            response = llm.invoke([
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ])
            content = response.content.strip()

            # Check if the response contains Message:
            if "Message:" in content:
                # Extract the message
                message_match = re.search(r'Message:\s*(.*)', content, re.DOTALL)
                if message_match:
                    final_message = message_match.group(1).strip()
                   
                    # Return the message to state
                    return {
                        "crowd_status": final_message                   
                    }

            # Check if the response contains Action:
            if "Action:" in content:
                # Extract the action
                action_match = re.search(r'Action:\s*(\w+)', content)
                if action_match:
                    tool_name = action_match.group(1)

                    # Execute the tool
                    observation = execute_tool(tool_name, content)

                    # Add observation to internal context
                    internal_context += f"\n{content}\n\nObservation: {observation}\n"
                    continue

            # If we get here without action or message, add to context and continue
            internal_context += f"\n{content}\n"

        except Exception as e:
            # Fallback response if LLM fails
            print(e)