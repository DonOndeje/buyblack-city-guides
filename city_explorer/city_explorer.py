from agency_swarm import Agent

city_explorer = Agent(
    name="City Explorer",
    description="Discovers Black-owned businesses, events, landmarks in chosen U.S. cities.",
    instructions="./instructions.md",
    tools_folder="./tools",
    model="gpt-4o-mini"  # Faster, more cost-effective model
)
 