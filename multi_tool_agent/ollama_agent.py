# from litellm import LiteLlm
# from litellm import Agent
import litellm
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
# from litellm import roll_die, check_prime

# assert litellm.supports_function_calling(model="gemini/gemma-3-27b-it") == True

root_agent = LlmAgent(
    model=LiteLlm(model="ollama_chat/gemma3"),
    # api_base="http://10.0.0.254:11434",
    name="dice_agent",
    description=(
        "hello world agent that can roll a dice of 8 sides and check prime"
        " numbers."
    ),
    instruction="""
      You roll dice and answer questions about the outcome of the dice rolls.
    """,
    tools=[
        # roll_die,
        # check_prime,
    ],
)
