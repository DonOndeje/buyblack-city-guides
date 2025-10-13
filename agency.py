from dotenv import load_dotenv
from agency_swarm import Agency

from city_explorer.city_explorer import city_explorer
from itinerary_planner.itinerary_planner import itinerary_planner
from cultural_curator.cultural_curator import cultural_curator

import asyncio

load_dotenv()

# do not remove this method, it is used in the main.py file to deploy the agency (it has to be a method)
def create_agency(load_threads_callback=None):
    agency = Agency(
        city_explorer,  # Entry point for user communication
        itinerary_planner,
        cultural_curator,
        communication_flows=[
            # City Explorer can communicate with both other agents
            (city_explorer, itinerary_planner),
            (city_explorer, cultural_curator),
            # Itinerary Planner can communicate with Cultural Curator
            (itinerary_planner, cultural_curator),
            # Cultural Curator can provide feedback to Itinerary Planner
            (cultural_curator, itinerary_planner)
        ],
        name="BuyBlackCityGuide",
        shared_instructions="shared_instructions.md",
        load_threads_callback=load_threads_callback,
    )

    return agency

if __name__ == "__main__":
    agency = create_agency()

    # test 1 message
    # async def main():
    #     response = await agency.get_response("Hello, how are you?")
    #     print(response)
    # asyncio.run(main())

    # run in terminal
    agency.terminal_demo()