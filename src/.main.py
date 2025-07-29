from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types
import json
import asyncio
# --- 1. Define Constants ---
APP_NAME = "agent_comparison_app"
USER_ID = "test_user_456"
SESSION_ID_TOOL_AGENT = "session_tool_agent_xyz"
SESSION_ID_SCHEMA_AGENT = "session_schema_agent_xyz"
MODEL_NAME = "ollama_chat/mistral"

def get_capital_city(country: str) -> str:
  """Retrieves the capital city for a given country."""
  # Replace with actual logic (e.g., API call, database lookup)
  capitals = {"france": "Paris", "japan": "Tokyo", "canada": "Ottawa"}
  return capitals.get(country.lower(), f"Sorry, I don't know the capital of {country}.")


# Example: Adding instructions
capital_agent = LlmAgent(
    # model="ollama_chat/gemma3",
    model=LiteLlm(model="ollama_chat/mistral"),
    name="capital_agent",
    description="Answers user questions about the capital city of a given country.",
    instruction="""You are an agent that provides the capital city of a country.
When a user asks for the capital of a country:
1. Identify the country name from the user's query.
2. Use the `get_capital_city` tool to find the capital.
3. Respond clearly to the user, stating the capital city.
Example Query: "What's the capital of {country}?"
Example Response: "The capital of France is Paris."
""",
    # tools will be added next
)

# --- 5. Set up Session Management and Runners ---
session_service = InMemorySessionService()

# Create separate sessions for clarity, though not strictly necessary if context is managed
session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID_TOOL_AGENT)
session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID_SCHEMA_AGENT)

# Create a runner for EACH agent
capital_runner = Runner(
    agent=capital_agent_with_tool,
    app_name=APP_NAME,
    session_service=session_service
)
structured_runner = Runner(
    agent=structured_info_agent_schema,
    app_name=APP_NAME,
    session_service=session_service
)

# --- 6. Define Agent Interaction Logic ---
async def call_agent_and_print(
    runner_instance: Runner,
    agent_instance: LlmAgent,
    session_id: str,
    query_json: str
):
    """Sends a query to the specified agent/runner and prints results."""
    print(f"\n>>> Calling Agent: '{agent_instance.name}' | Query: {query_json}")

    user_content = types.Content(role='user', parts=[types.Part(text=query_json)])

    final_response_content = "No final response received."
    async for event in runner_instance.run_async(user_id=USER_ID, session_id=session_id, new_message=user_content):
        # print(f"Event: {event.type}, Author: {event.author}") # Uncomment for detailed logging
        if event.is_final_response() and event.content and event.content.parts:
            # For output_schema, the content is the JSON string itself
            final_response_content = event.content.parts[0].text

    print(f"<<< Agent '{agent_instance.name}' Response: {final_response_content}")

    current_session = session_service.get_session(app_name=APP_NAME,
                                                  user_id=USER_ID,
                                                  session_id=session_id)
    stored_output = current_session.state.get(agent_instance.output_key)

    # Pretty print if the stored output looks like JSON (likely from output_schema)
    print(f"--- Session State ['{agent_instance.output_key}']: ", end="")
    try:
        # Attempt to parse and pretty print if it's JSON
        parsed_output = json.loads(stored_output)
        print(json.dumps(parsed_output, indent=2))
    except (json.JSONDecodeError, TypeError):
         # Otherwise, print as string
        print(stored_output)
    print("-" * 30)


# --- 7. Run Interactions ---
async def main():
    print("--- Testing Agent with Tool ---")
    asyncio.run(call_agent_and_print(capital_runner, capital_agent_with_tool, SESSION_ID_TOOL_AGENT, '{"country": "France"}'))
    asyncio.run(call_agent_and_print(capital_runner, capital_agent_with_tool, SESSION_ID_TOOL_AGENT, '{"country": "Canada"}'))

    print("\n\n--- Testing Agent with Output Schema (No Tool Use) ---")
    asyncio.run(call_agent_and_print(structured_runner, structured_info_agent_schema, SESSION_ID_SCHEMA_AGENT, '{"country": "France"}'))
    asyncio.run(call_agent_and_print(structured_runner, structured_info_agent_schema, SESSION_ID_SCHEMA_AGENT, '{"country": "Japan"}'))

if __name__ == "__main__":
    asyncio.run(main())