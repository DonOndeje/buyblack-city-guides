from agency_swarm.tools import BaseTool
from pydantic import Field
import pandas as pd
import os
import hashlib
import json
from functools import lru_cache

# Global cache for loaded data
_data_cache = None
_cache_file = None

@lru_cache(maxsize=32)
def _get_filtered_data(category: str, keyword: str, limit: int):
    """Cached search function"""
    global _data_cache

    if _data_cache is None:
        # Load data once and cache it
        csv_path = os.path.join(os.path.dirname(__file__), '../data/Oakland_Identifies_as_Black_Owned_nominees.csv')
        _data_cache = pd.read_csv(csv_path, low_memory=False)

    df = _data_cache

    # Filter by category
    mask = df['category'].str.contains(category, case=False, na=False) | df['type'].str.contains(category, case=False, na=False)
    filtered = df[mask]

    # If keyword provided, further filter
    if keyword and keyword.strip():
        search_cols = ['name', 'subtypes', 'full_address', 'description', 'about']
        search_mask = pd.Series(False, index=filtered.index)
        for col in search_cols:
            if col in filtered.columns:
                search_mask |= filtered[col].astype(str).str.contains(keyword, case=False, na=False)
        filtered = filtered[search_mask]

    # Sort by rating (if exists)
    if 'rating' in filtered.columns:
        filtered = filtered.sort_values(by='rating', ascending=False)

    sample = filtered.head(limit)
    return sample

class BuyBlackDirectorySearchSimple(BaseTool):
    """
    Search Oakland Black-owned businesses from the provided CSV file by category, keyword, or business type.
    Optimized with caching for faster responses.
    """
    category: str = Field(..., description="Business category or type to search (e.g. 'restaurant', 'bakery', 'accountant')")
    keyword: str = Field("", description="Optional search keyword for further refinement (name, address, subtypes, etc.)")
    limit: int = Field(5, description="Maximum number of results to return (reduced for faster responses).")

    def run(self):
        try:
            # Use cached search function for faster responses
            sample = _get_filtered_data(self.category, self.keyword, self.limit)

            # Format output
            results = []
            for _, row in sample.iterrows():
                business = {
                    'name': row.get('name', ''),
                    'type': row.get('category', ''),
                    'address': row.get('full_address', ''),
                    'phone': row.get('phone', ''),
                    'website': row.get('site', ''),
                    'hours': row.get('working_hours', ''),
                    'rating': row.get('rating', ''),
                    'reviews': row.get('reviews', ''),
                    'description': row.get('description', ''),
                    'google_maps': row.get('location_link', '')
                }
                results.append(business)
            
            return results if results else f"No results found for category '{self.category}' with keyword '{self.keyword}'."
            
        except Exception as e:
            return f"Error searching businesses: {str(e)}"

if __name__ == "__main__":
    tool = BuyBlackDirectorySearchSimple(category="bakery", keyword="", limit=3)
    print(tool.run())
