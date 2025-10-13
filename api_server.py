from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import asyncio
from agency import create_agency
import uvicorn

# Initialize FastAPI app
app = FastAPI(
    title="BuyBlack City Guide API",
    description="API for discovering Black-owned businesses and cultural experiences",
    version="1.0.0"
)

# Add CORS middleware to allow web requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize agency
agency = create_agency()

# Request/Response models
class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    agent_used: str

class BusinessSearchRequest(BaseModel):
    category: str
    keyword: Optional[str] = ""
    limit: Optional[int] = 10

class BusinessSearchResponse(BaseModel):
    businesses: List[dict]
    total_found: int

class ItineraryRequest(BaseModel):
    city: str
    duration_days: int
    interests: List[str]
    budget_level: str = "medium"

class ItineraryResponse(BaseModel):
    itinerary: dict
    city: str
    duration_days: int

# API Endpoints
@app.get("/")
async def root():
    return {
        "message": "BuyBlack City Guide API",
        "version": "1.0.0",
        "endpoints": {
            "chat": "/api/chat",
            "businesses": "/api/businesses/search",
            "itinerary": "/api/itinerary/create",
            "health": "/health"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "buyblack-city-guide-api"}

@app.post("/api/chat", response_model=ChatResponse)
async def chat_with_agency(request: ChatRequest):
    """Chat with the BuyBlack City Guide agency"""
    try:
        result = await agency.get_response(request.message)
        
        # Extract response
        if hasattr(result, 'final_output'):
            response_text = str(result.final_output)
        elif hasattr(result, 'output'):
            response_text = str(result.output)
        else:
            response_text = str(result)
        
        # Get agent info
        agent_used = "City Explorer"  # Default
        if hasattr(result, 'last_agent'):
            agent_used = result.last_agent.name
        
        return ChatResponse(
            response=response_text,
            conversation_id=request.conversation_id or "default",
            agent_used=agent_used
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

@app.post("/api/businesses/search", response_model=BusinessSearchResponse)
async def search_businesses(request: BusinessSearchRequest):
    """Search for Black-owned businesses by category"""
    try:
        # Import the tool directly
        from city_explorer.tools.BuyBlackDirectorySearch import BuyBlackDirectorySearch
        
        tool = BuyBlackDirectorySearch(
            category=request.category,
            keyword=request.keyword,
            limit=request.limit
        )
        
        results = tool.run()
        
        if isinstance(results, list):
            return BusinessSearchResponse(
                businesses=results,
                total_found=len(results)
            )
        else:
            return BusinessSearchResponse(
                businesses=[],
                total_found=0
            )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching businesses: {str(e)}")

@app.post("/api/itinerary/create", response_model=ItineraryResponse)
async def create_itinerary(request: ItineraryRequest):
    """Create a personalized itinerary"""
    try:
        # Import the tool directly
        from itinerary_planner.tools.ItineraryBuilder import ItineraryBuilder
        
        tool = ItineraryBuilder(
            city=request.city,
            duration_days=request.duration_days,
            interests=request.interests,
            budget_level=request.budget_level
        )
        
        itinerary_json = tool.run()
        
        import json
        itinerary_dict = json.loads(itinerary_json)
        
        return ItineraryResponse(
            itinerary=itinerary_dict,
            city=request.city,
            duration_days=request.duration_days
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating itinerary: {str(e)}")

@app.get("/api/businesses/categories")
async def get_business_categories():
    """Get available business categories"""
    return {
        "categories": [
            "restaurant", "bakery", "coffee", "barber", "beauty", "retail",
            "fitness", "art", "entertainment", "professional", "automotive",
            "health", "education", "technology", "real estate"
        ]
    }

@app.get("/api/cities")
async def get_supported_cities():
    """Get supported cities"""
    return {
        "cities": [
            "Oakland", "San Francisco", "Berkeley", "Richmond", "Fremont"
        ],
        "note": "Currently focused on Oakland with plans to expand to other Bay Area cities"
    }

if __name__ == "__main__":
    uvicorn.run(
        "api_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
