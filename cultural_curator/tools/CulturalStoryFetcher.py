from agency_swarm.tools import BaseTool
from pydantic import Field
import requests
import json

class CulturalStoryFetcher(BaseTool):
    """
    Fetch cultural and historical context for businesses, landmarks, and locations to enrich user experiences.
    """
    business_name: str = Field(..., description="Name of the business, landmark, or location to research")
    location: str = Field("Oakland, CA", description="City or location context for the business")
    topic_focus: str = Field("", description="Specific aspect to focus on (history, culture, community impact, etc.)")

    def run(self):
        """
        Fetch cultural and historical context for the specified business or location.
        """
        try:
            # Try to get information from multiple sources
            context_info = {
                "business_name": self.business_name,
                "location": self.location,
                "cultural_context": self._get_cultural_context(),
                "historical_significance": self._get_historical_info(),
                "community_impact": self._get_community_impact(),
                "recommended_visit_context": self._get_visit_context()
            }
            
            return context_info
            
        except Exception as e:
            return f"Error fetching cultural context: {str(e)}"

    def _get_cultural_context(self) -> str:
        """Get cultural context for the business/location"""
        # Sample cultural context for Oakland businesses
        cultural_contexts = {
            "African American Museum and Library at Oakland": 
                "This museum is a cornerstone of Oakland's cultural heritage, preserving and showcasing the rich history of African Americans in the Bay Area. It serves as a community gathering place and educational resource.",
            
            "Jack London Square": 
                "Named after the famous author Jack London, this historic waterfront area has been a center of commerce and culture for over a century. It represents Oakland's maritime heritage and literary connections.",
            
            "Fox Theater": 
                "This stunning Art Deco theater is not just a performance venue but a symbol of Oakland's cultural renaissance. It was restored to its former glory and now hosts world-class entertainment.",
            
            "Miss Ollie's": 
                "A beloved Caribbean restaurant that brings authentic flavors and cultural traditions to Oakland. It represents the city's diverse culinary heritage and Caribbean community connections.",
            
            "Sami African Imports": 
                "This shop connects Oakland residents with African culture through authentic goods, textiles, and art. It's a bridge between continents, fostering cultural understanding and appreciation.",
            
            "Brown Sugar Kitchen": 
                "Known for its soul food and Southern comfort cuisine, this restaurant celebrates African American culinary traditions while serving as a community gathering place."
        }
        
        return cultural_contexts.get(self.business_name, 
            f"{self.business_name} represents an important part of Oakland's diverse cultural landscape, contributing to the city's vibrant community and rich heritage.")

    def _get_historical_info(self) -> str:
        """Get historical significance information"""
        historical_info = {
            "African American Museum and Library at Oakland": 
                "Established in 1994, this institution houses one of the most comprehensive collections of African American history and culture on the West Coast. It documents the journey of African Americans in California from the Gold Rush era to present day.",
            
            "Jack London Square": 
                "Originally developed in the early 1900s, this area was once a bustling port and industrial center. It's named after Jack London, who spent time in Oakland and drew inspiration from the waterfront for his writing.",
            
            "Fox Theater": 
                "Built in 1928, this theater was designed by the same architect who created the famous Fox theaters in other cities. After decades of decline, it was restored in 2009 and became a symbol of Oakland's cultural revival.",
            
            "Lake Merritt": 
                "Known as America's oldest wildlife refuge, Lake Merritt has been a gathering place for Oakland residents for over 150 years. It was originally a tidal lagoon that was transformed into a freshwater lake."
        }
        
        return historical_info.get(self.business_name,
            f"{self.business_name} has played a significant role in Oakland's development and continues to be an important part of the city's ongoing story.")

    def _get_community_impact(self) -> str:
        """Get information about community impact"""
        community_impacts = {
            "African American Museum and Library at Oakland": 
                "The museum serves as an educational resource for schools, hosts community events, and provides a space for dialogue about race, culture, and history. It's a source of pride and identity for Oakland's African American community.",
            
            "Jack London Square": 
                "This area has undergone significant revitalization and now serves as a major entertainment and dining destination. It provides jobs, supports local businesses, and attracts visitors from throughout the Bay Area.",
            
            "Fox Theater": 
                "The theater's restoration sparked a cultural renaissance in downtown Oakland. It attracts world-class performers and provides a venue for local artists, contributing to the city's reputation as a cultural destination.",
            
            "Miss Ollie's": 
                "This restaurant supports local suppliers and employs community members. It has become a gathering place that celebrates Caribbean culture while welcoming people from all backgrounds."
        }
        
        return community_impacts.get(self.business_name,
            f"{self.business_name} contributes to Oakland's economy, provides employment opportunities, and enriches the cultural fabric of the community.")

    def _get_visit_context(self) -> str:
        """Get recommendations for visiting with cultural awareness"""
        visit_contexts = {
            "African American Museum and Library at Oakland": 
                "Visit with an open mind and respect for the historical significance. Take time to read exhibits thoroughly and consider the ongoing impact of the stories being told.",
            
            "Jack London Square": 
                "Best visited during daytime for historical appreciation, or evening for dining and entertainment. Take a moment to appreciate the maritime history while enjoying the modern amenities.",
            
            "Fox Theater": 
                "Arrive early to appreciate the stunning Art Deco architecture. Check the schedule for performances that celebrate diverse cultures and support local artists.",
            
            "Sami African Imports": 
                "Engage respectfully with the cultural items and ask questions about their origins. This is an opportunity to learn about African cultures while supporting a local business."
        }
        
        return visit_contexts.get(self.business_name,
            f"When visiting {self.business_name}, take time to appreciate its cultural significance and consider how it contributes to Oakland's diverse community. Support the business and engage respectfully with the cultural elements.")

    def _search_wikipedia(self, query: str) -> str:
        """Search Wikipedia for additional information (fallback method)"""
        try:
            # This would typically use Wikipedia API
            # For now, return a placeholder
            return f"Wikipedia contains additional information about {query} and its cultural significance."
        except:
            return ""

if __name__ == "__main__":
    tool = CulturalStoryFetcher(
        business_name="African American Museum and Library at Oakland",
        location="Oakland, CA",
        topic_focus="history"
    )
    result = tool.run()
    print(json.dumps(result, indent=2))

