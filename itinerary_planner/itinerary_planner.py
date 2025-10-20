from agency_swarm import Agent
import os

_BASE_DIR = os.path.dirname(__file__)

itinerary_planner = Agent(
    name="Itinerary Planner",
    description="Generates structured, customized trip itineraries based on input and discoveries.",
    instructions=os.path.join(_BASE_DIR, "instructions.md"),
    tools_folder=os.path.join(_BASE_DIR, "tools"),
    model="gpt-4o-mini"  # Faster, more cost-effective model
)
