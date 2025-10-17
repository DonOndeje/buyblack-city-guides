from agency_swarm import Agent
from agents import ModelSettings

itinerary_planner = Agent(
    name="Itinerary Planner",
    description="Generates structured, customized trip itineraries based on input and discoveries.",
    instructions="./instructions.md",
    tools_folder="./tools",
    model="gpt-4o-mini",  # Faster, more cost-effective model
    model_settings=ModelSettings(
        max_tokens=1200,  # Limit response length for faster generation
        temperature=0.3   # More consistent, faster responses
    )
)
