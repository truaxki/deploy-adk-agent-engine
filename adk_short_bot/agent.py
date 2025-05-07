from google.adk.agents import Agent
import os

from adk_short_bot.prompt import ROOT_AGENT_INSTRUCTION
from adk_short_bot.tools import count_characters

# Set environment variables directly if not already set
if not os.getenv("GOOGLE_CLOUD_PROJECT"):
    os.environ["GOOGLE_CLOUD_PROJECT"] = "astra-v1-2025"
if not os.getenv("GOOGLE_CLOUD_LOCATION"):
    os.environ["GOOGLE_CLOUD_LOCATION"] = "us-central1"

# Use Vertex AI as the backend for Gemini
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"

# Try to initialize backend directly
try:
    from google.cloud import aiplatform
    aiplatform.init(
        project=os.environ["GOOGLE_CLOUD_PROJECT"],
        location=os.environ["GOOGLE_CLOUD_LOCATION"]
    )
    print(f"Initialized Vertex AI with project={os.environ['GOOGLE_CLOUD_PROJECT']}, location={os.environ['GOOGLE_CLOUD_LOCATION']}")
except Exception as e:
    print(f"Warning: Could not initialize Vertex AI: {e}")
    print("Continuing with default settings...")

root_agent = Agent(
    name="adk_short_bot",
    model="gemini-2.0-flash",
    description="A bot that shortens messages while maintaining their core meaning",
    instruction=ROOT_AGENT_INSTRUCTION,
    tools=[count_characters],
)
