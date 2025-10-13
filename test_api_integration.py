#!/usr/bin/env python3
"""
Test script for BuyBlack City Guide API integration
"""

import asyncio
import json
from agency import create_agency

async def test_agency_direct():
    """Test the agency directly"""
    print("🧪 Testing Agency Direct Integration...")
    
    try:
        agency = create_agency()
        
        # Test chat functionality
        result = await agency.get_response("Find Black-owned restaurants in Oakland")
        
        if hasattr(result, 'final_output'):
            response = str(result.final_output)
        else:
            response = str(result)
        
        print("✅ Agency Response (first 200 chars):")
        print(response[:200] + "..." if len(response) > 200 else response)
        print()
        
        return True
        
    except Exception as e:
        print(f"❌ Agency test failed: {e}")
        return False

def test_business_search():
    """Test business search tool directly"""
    print("🧪 Testing Business Search Tool...")
    
    try:
        from city_explorer.tools.BuyBlackDirectorySearch import BuyBlackDirectorySearch
        
        tool = BuyBlackDirectorySearch(
            category="restaurant",
            keyword="",
            limit=3
        )
        
        results = tool.run()
        
        if isinstance(results, list) and len(results) > 0:
            print("✅ Business Search Results:")
            for i, business in enumerate(results[:2], 1):
                print(f"  {i}. {business.get('name', 'N/A')} - {business.get('type', 'N/A')}")
            print()
            return True
        else:
            print("⚠️ No business results found")
            return False
            
    except Exception as e:
        print(f"❌ Business search test failed: {e}")
        return False

def test_itinerary_builder():
    """Test itinerary builder tool directly"""
    print("🧪 Testing Itinerary Builder Tool...")
    
    try:
        from itinerary_planner.tools.ItineraryBuilder import ItineraryBuilder
        
        tool = ItineraryBuilder(
            city="Oakland",
            duration_days=1,
            interests=["food", "culture"],
            budget_level="medium"
        )
        
        result = tool.run()
        
        if result:
            print("✅ Itinerary Builder Results:")
            itinerary = json.loads(result)
            print(f"  City: {itinerary.get('city', 'N/A')}")
            print(f"  Duration: {itinerary.get('duration_days', 'N/A')} days")
            print(f"  Activities planned: {len(itinerary.get('daily_plans', []))}")
            print()
            return True
        else:
            print("⚠️ No itinerary results found")
            return False
            
    except Exception as e:
        print(f"❌ Itinerary builder test failed: {e}")
        return False

async def main():
    """Run all tests"""
    print("🚀 BuyBlack City Guide - Integration Tests")
    print("=" * 50)
    print()
    
    tests_passed = 0
    total_tests = 3
    
    # Test 1: Agency Direct
    if await test_agency_direct():
        tests_passed += 1
    
    # Test 2: Business Search
    if test_business_search():
        tests_passed += 1
    
    # Test 3: Itinerary Builder
    if test_itinerary_builder():
        tests_passed += 1
    
    print("=" * 50)
    print(f"📊 Test Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! Your agency is ready for website integration.")
        print()
        print("🌐 Next Steps:")
        print("1. Start the API server: python api_server.py")
        print("2. Open the HTML example: website_integration_example.html")
        print("3. Or use the React component: react_integration_example.jsx")
        print("4. Deploy using the WEBSITE_INTEGRATION.md guide")
    else:
        print("⚠️ Some tests failed. Please check the error messages above.")
    
    return tests_passed == total_tests

if __name__ == "__main__":
    asyncio.run(main())
