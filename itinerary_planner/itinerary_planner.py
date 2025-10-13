from agency_swarm import Agent

itinerary_planner = Agent(
    name="Itinerary Planner",
    description="Generates structured, customized trip itineraries based on input and discoveries.",
    instructions="./instructions.md",
    tools_folder="./tools",
    model="gpt-5"
)
