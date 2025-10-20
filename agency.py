from dotenv import load_dotenv
from agency_swarm import Agency
import hashlib
import json
import os
import time
from typing import Dict, Any, Optional

from city_explorer.city_explorer import city_explorer
from itinerary_planner.itinerary_planner import itinerary_planner
from cultural_curator.cultural_curator import cultural_curator

import asyncio

load_dotenv()

# Simple response cache for faster repeated queries
class ResponseCache:
    def __init__(self, cache_file="response_cache.json", max_age=3600):
        self.cache_file = cache_file
        self.max_age = max_age  # 1 hour default
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._load_cache()

    def _load_cache(self):
        """Load cache from file if it exists"""
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r') as f:
                    self._cache = json.load(f)
            except:
                self._cache = {}

    def _save_cache(self):
        """Save cache to file"""
        try:
            with open(self.cache_file, 'w') as f:
                json.dump(self._cache, f)
        except:
            pass

    def _get_cache_key(self, message: str) -> str:
        """Generate cache key from message"""
        return hashlib.md5(message.lower().encode()).hexdigest()[:16]

    def get(self, message: str) -> Optional[str]:
        """Get cached response if available and not expired"""
        key = self._get_cache_key(message)
        if key in self._cache:
            cached = self._cache[key]
            if time.time() - cached.get('timestamp', 0) < self.max_age:
                return cached.get('response')
            else:
                del self._cache[key]
        return None

    def set(self, message: str, response: str):
        """Cache a response"""
        key = self._get_cache_key(message)
        self._cache[key] = {
            'response': response,
            'timestamp': time.time()
        }
        self._save_cache()

# Global response cache
response_cache = ResponseCache()

# Optimized communication flows for faster responses
def create_agency(load_threads_callback=None):
    agency = Agency(
        city_explorer,  # Entry point
        itinerary_planner,
        cultural_curator,
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