from agency_swarm.tools import BaseTool
from pydantic import Field
import pandas as pd
import os

class BuyBlackDirectorySearchSimple(BaseTool):
    """
    Search Oakland Black-owned businesses from the provided CSV file by category, keyword, or business type.
    Simplified version without Google Places API to avoid timeout issues.
    """
    category: str = Field(..., description="Business category or type to search (e.g. 'restaurant', 'bakery', 'accountant')")
    keyword: str = Field("", description="Optional search keyword for further refinement (name, address, subtypes, etc.)")
    limit: int = Field(10, description="Maximum number of results to return.")

    def run(self):
        try:
            # Load the CSV
            csv_path = os.path.join(os.path.dirname(__file__), '../data/Oakland_Identifies_as_Black_Owned_nominees.csv')
            df = pd.read_csv(csv_path, low_memory=False)

            # Filter by category
            mask = df['category'].str.contains(self.category, case=False, na=False) | df['type'].str.contains(self.category, case=False, na=False)
            filtered = df[mask]

            # If keyword provided, further filter
            if self.keyword and self.keyword.strip():
                search_cols = ['name', 'subtypes', 'full_address', 'description', 'about']
                search_mask = pd.Series(False, index=filtered.index)
                for col in search_cols:
                    if col in filtered.columns:
                        search_mask |= filtered[col].astype(str).str.contains(self.keyword, case=False, na=False)
                filtered = filtered[search_mask]

            # Sort by rating (if exists)
            if 'rating' in filtered:
                filtered = filtered.sort_values(by='rating', ascending=False)
            
            sample = filtered.head(self.limit)

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
