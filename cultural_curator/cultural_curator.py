from agency_swarm import Agent

cultural_curator = Agent(
    name="Cultural Curator",
    description="Adds context and storytelling for businesses, events, and trips.",
    instructions="./instructions.md",
    tools_folder="./tools",
    model="gpt-5"
)
