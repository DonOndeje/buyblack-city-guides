from agency_swarm import Agent
import os

_BASE_DIR = os.path.dirname(__file__)

cultural_curator = Agent(
    name="Cultural Curator",
    description="Adds context and storytelling for businesses, events, and trips.",
    instructions=os.path.join(_BASE_DIR, "instructions.md"),
    tools_folder=os.path.join(_BASE_DIR, "tools"),
    model="gpt-4o-mini"  # Faster, more cost-effective model
)
