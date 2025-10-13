from agency_swarm.tools import BaseTool
from pydantic import Field
from typing import List, Dict, Any
import json
from datetime import datetime, timedelta

class ItineraryBuilder(BaseTool):
    """
    Generate structured, day-by-day trip itineraries based on user preferences and discovered businesses/landmarks.
    """
    city: str = Field(..., description="The city for the itinerary")
    days: int = Field(1, description="Number of days for the trip")
    interests: List[str] = Field(default=[], description="User interests (e.g., 'food', 'culture', 'shopping', 'history')")
    budget_level: str = Field("medium", description="Budget level: 'budget', 'medium', 'luxury'")
    selected_locations: List[Dict[str, Any]] = Field(default=[], description="Pre-selected businesses/landmarks to include")
    start_time: str = Field("09:00", description="Preferred start time for each day (24-hour format)")

    def run(self):
        """
        Build a comprehensive itinerary based on inputs.
        """
        try:
            # Create the itinerary structure
            itinerary = {
                "city": self.city,
                "duration_days": self.days,
                "interests": self.interests,
                "budget_level": self.budget_level,
                "created_at": datetime.now().isoformat(),
                "daily_plans": []
            }
            
            # Generate daily plans
            for day in range(1, self.days + 1):
                daily_plan = self._create_daily_plan(day)
                itinerary["daily_plans"].append(daily_plan)
            
            return itinerary
            
        except Exception as e:
            return f"Error creating itinerary: {str(e)}"

    def _create_daily_plan(self, day_number: int) -> Dict[str, Any]:
        """Create a plan for a single day"""
        # Sample activities based on interests and budget
        activities = self._generate_activities_for_day(day_number)
        
        daily_plan = {
            "day": day_number,
            "date": (datetime.now() + timedelta(days=day_number-1)).strftime("%Y-%m-%d"),
            "theme": self._get_day_theme(day_number),
            "activities": activities,
            "estimated_cost": self._estimate_daily_cost(activities),
            "transportation_notes": self._get_transportation_notes()
        }
        
        return daily_plan

    def _generate_activities_for_day(self, day_number: int) -> List[Dict[str, Any]]:
        """Generate activities for a specific day"""
        activities = []
        current_time = self.start_time
        
        # Morning activities (9:00-12:00)
        morning_activity = self._get_morning_activity(day_number)
        if morning_activity:
            activities.append({
                "time": current_time,
                "duration": "2-3 hours",
                "activity": morning_activity["name"],
                "type": morning_activity["type"],
                "location": morning_activity["location"],
                "description": morning_activity["description"],
                "cost_estimate": morning_activity["cost"]
            })
            current_time = self._add_time(current_time, 3)
        
        # Lunch (12:00-13:30)
        lunch_activity = self._get_lunch_activity()
        if lunch_activity:
            activities.append({
                "time": "12:00",
                "duration": "1.5 hours",
                "activity": lunch_activity["name"],
                "type": "Restaurant",
                "location": lunch_activity["location"],
                "description": lunch_activity["description"],
                "cost_estimate": lunch_activity["cost"]
            })
            current_time = "14:00"
        
        # Afternoon activities (14:00-17:00)
        afternoon_activity = self._get_afternoon_activity(day_number)
        if afternoon_activity:
            activities.append({
                "time": current_time,
                "duration": "2-3 hours",
                "activity": afternoon_activity["name"],
                "type": afternoon_activity["type"],
                "location": afternoon_activity["location"],
                "description": afternoon_activity["description"],
                "cost_estimate": afternoon_activity["cost"]
            })
            current_time = self._add_time(current_time, 3)
        
        # Evening activities (17:00-20:00)
        evening_activity = self._get_evening_activity(day_number)
        if evening_activity:
            activities.append({
                "time": "18:00",
                "duration": "2 hours",
                "activity": evening_activity["name"],
                "type": evening_activity["type"],
                "location": evening_activity["location"],
                "description": evening_activity["description"],
                "cost_estimate": evening_activity["cost"]
            })
        
        return activities

    def _get_day_theme(self, day_number: int) -> str:
        """Get the theme for a specific day"""
        themes = ["Cultural Discovery", "Food & Shopping", "History & Arts", "Community & Events"]
        return themes[(day_number - 1) % len(themes)]

    def _get_morning_activity(self, day_number: int) -> Dict[str, Any]:
        """Get morning activity based on interests and selected locations"""
        if "culture" in self.interests:
            return {
                "name": "African American Museum and Library at Oakland",
                "type": "Museum",
                "location": "659 14th St, Oakland, CA 94612",
                "description": "Explore African American history and culture",
                "cost": "$10-15" if self.budget_level == "budget" else "$15-25"
            }
        elif "food" in self.interests:
            return {
                "name": "Grand Lake Farmers Market",
                "type": "Market",
                "location": "Grand Ave & Lake Park Ave, Oakland, CA",
                "description": "Local farmers market with fresh produce and artisanal goods",
                "cost": "$20-40"
            }
        else:
            return {
                "name": "Lake Merritt",
                "type": "Nature",
                "location": "Oakland, CA",
                "description": "Beautiful urban lake for walking and bird watching",
                "cost": "Free"
            }

    def _get_lunch_activity(self) -> Dict[str, Any]:
        """Get lunch recommendation"""
        lunch_options = [
            {
                "name": "Miss Ollie's",
                "location": "901 Washington St, Oakland, CA 94607",
                "description": "Caribbean cuisine with Black-owned heritage",
                "cost": "$15-25"
            },
            {
                "name": "Brown Sugar Kitchen",
                "location": "2534 Mandela Pkwy, Oakland, CA 94607",
                "description": "Southern comfort food and soul food",
                "cost": "$12-20"
            }
        ]
        return lunch_options[0] if self.budget_level != "budget" else lunch_options[1]

    def _get_afternoon_activity(self, day_number: int) -> Dict[str, Any]:
        """Get afternoon activity"""
        if "shopping" in self.interests:
            return {
                "name": "Sami African Imports",
                "type": "Shopping",
                "location": "5600 Martin Luther King Jr Way #105, Oakland, CA 94609",
                "description": "African goods and cultural items",
                "cost": "$30-100"
            }
        else:
            return {
                "name": "Jack London Square",
                "type": "Historic District",
                "location": "Broadway, Oakland, CA 94607",
                "description": "Historic waterfront area with shops and restaurants",
                "cost": "$20-50"
            }

    def _get_evening_activity(self, day_number: int) -> Dict[str, Any]:
        """Get evening activity"""
        return {
            "name": "Fox Theater",
            "type": "Entertainment",
            "location": "1807 Telegraph Ave, Oakland, CA 94612",
            "description": "Historic Art Deco theater with live performances",
            "cost": "$25-75"
        }

    def _add_time(self, time_str: str, hours: int) -> str:
        """Add hours to a time string"""
        time_obj = datetime.strptime(time_str, "%H:%M")
        new_time = time_obj + timedelta(hours=hours)
        return new_time.strftime("%H:%M")

    def _estimate_daily_cost(self, activities: List[Dict[str, Any]]) -> str:
        """Estimate total daily cost"""
        if self.budget_level == "budget":
            return "$50-100"
        elif self.budget_level == "luxury":
            return "$200-400"
        else:
            return "$100-200"

    def _get_transportation_notes(self) -> str:
        """Get transportation recommendations"""
        return "Consider BART for public transit, rideshare for convenience, or walking in downtown areas"

if __name__ == "__main__":
    tool = ItineraryBuilder(
        city="Oakland",
        days=2,
        interests=["culture", "food"],
        budget_level="medium",
        selected_locations=[]
    )
    result = tool.run()
    print(json.dumps(result, indent=2))

