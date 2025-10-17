from agency_swarm import Agent
from agents import ModelSettings

city_explorer = Agent(
    name="City Explorer",
    description="Discovers Black-owned businesses, events, landmarks in chosen U.S. cities.",
    instructions="./instructions.md",
    tools_folder="./tools",
    model="gpt-4o-mini",  # Faster, more cost-effective model
    model_settings=ModelSettings(
        max_tokens=1000,  # Limit response length for faster generation
        temperature=0.3   # More consistent, faster responses
    )
)
 