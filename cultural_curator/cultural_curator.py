from agency_swarm import Agent
from agents import ModelSettings

cultural_curator = Agent(
    name="Cultural Curator",
    description="Adds context and storytelling for businesses, events, and trips.",
    instructions="./instructions.md",
    tools_folder="./tools",
    model="gpt-4o-mini",  # Faster, more cost-effective model
    model_settings=ModelSettings(
        max_tokens=800,   # Limit response length for faster generation
        temperature=0.3   # More consistent, faster responses
    )
)
