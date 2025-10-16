from agency_swarm.tools import BaseTool
from pydantic import Field
import pandas as pd
import os
import requests
import json

class BuyBlackDirectorySearch(BaseTool): 
    """
    Search Oakland Black-owned businesses from the provided CSV file by category, keyword, or business type.
    """
    category: str = Field(..., description="Business category or type to search (e.g. 'restaurant', 'bakery', 'accountant')")
    keyword: str = Field("", description="Optional search keyword for further refinement (name, address, subtypes, etc.)")
    limit: int = Field(10, description="Maximum number of results to return.")

    def run(self):
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

        # Format output and enhance with Google Places data
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
            
            # Try to enhance with Google Places data
            enhanced_data = self._enhance_with_google_places(business['name'], business['address'])
            if enhanced_data:
                business.update(enhanced_data)
            
            results.append(business)
        return results if results else f"No results found for category '{self.category}' with keyword '{self.keyword}'."

    def _enhance_with_google_places(self, business_name: str, address: str) -> dict:
        """Enhance business data with Google Places API information"""
        try:
            api_key = os.getenv('GOOGLE_PLACES_API_KEY')
            if not api_key:
                return {}
            
            # Try multiple search strategies
            search_queries = [
                f"{business_name} Oakland CA",  # Business name + Oakland
                f"{business_name} {address}",   # Business name + address
                business_name,                  # Just business name
                f"{business_name} bakery Oakland" if "bakery" in business_name.lower() else None,
                f"{business_name} restaurant Oakland" if "restaurant" in business_name.lower() else None
            ]
            
            # Remove None queries
            search_queries = [q for q in search_queries if q]
            
            url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
            
            for search_query in search_queries:
                params = {
                    'query': search_query,
                    'key': api_key,
                    'fields': 'place_id,name,formatted_address,rating,user_ratings_total,opening_hours,formatted_phone_number,website,photos'
                }
                
                response = requests.get(url, params=params, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if data.get('status') == 'OK' and data.get('results'):
                        place = data['results'][0]  # Get the first result
                        
                        enhanced_data = {}
                        
                        # Update rating if Google has a higher rating
                        if 'rating' in place:
                            enhanced_data['google_rating'] = place['rating']
                            enhanced_data['google_review_count'] = place.get('user_ratings_total', 0)
                        
                        # Add current hours if available
                        if 'opening_hours' in place:
                            enhanced_data['current_hours'] = place['opening_hours'].get('weekday_text', [])
                        
                        # Add phone number if missing
                        if 'formatted_phone_number' in place:
                            enhanced_data['google_phone'] = place['formatted_phone_number']
                        
                        # Add website if missing
                        if 'website' in place:
                            enhanced_data['google_website'] = place['website']
                        
                        # Add photos
                        if 'photos' in place:
                            photo_refs = [photo['photo_reference'] for photo in place['photos'][:3]]  # First 3 photos
                            enhanced_data['photo_references'] = photo_refs
                        
                        return enhanced_data
                
                # If this search didn't work, try the next one
                continue
            
            return {}
            
        except Exception as e:
            # If Google Places API fails, return empty dict (fallback to CSV data)
            return {}

if __name__ == "__main__":
    tool = BuyBlackDirectorySearch(category="bakery", keyword="", limit=3)
    print(tool.run())
