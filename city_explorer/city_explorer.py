from agency_swarm import Agent
import os

_BASE_DIR = os.path.dirname(__file__)

city_explorer = Agent(
    name="City Explorer",
    description="Discovers Black-owned businesses, events, landmarks in chosen U.S. cities.",
    instructions=os.path.join(_BASE_DIR, "instructions.md"),
    tools_folder=os.path.join(_BASE_DIR, "tools"),
    model="gpt-4o-mini"  # Faster, more cost-effective model
)
 