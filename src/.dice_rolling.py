import os
import re
import asyncio
from IPython.display import display, Markdown
import google.generativeai as genai
from google.adk.agents import Agent
from google.adk.tools import google_search
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService, Session
from google.genai.types import Content, Part
from getpass import getpass
from google.adk.models.lite_llm import LiteLlm

root_agent = Agent(
    model=LiteLlm(model="ollama_chat/mistral"),
    name="dice_agent",
    description=(
        "hello world agent that can roll a dice of 8 sides and check prime"
        " numbers."
    ),
    instruction="""
      You roll dice and answer questions about the outcome of the dice rolls.
    """,
    tools=[
        roll_die,
        check_prime,
    ],
)

