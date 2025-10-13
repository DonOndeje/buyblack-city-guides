import asyncio
from agency import create_agency

async def test_my_questions():
    """Test the agency with your own questions"""
    agency = create_agency()
    
    # Your custom questions here
    questions = [
        "Find Black-owned restaurants in Oakland",
        "Plan a 2-day cultural trip to Oakland",
        "What are the best Black-owned bakeries in Oakland?",
        "Tell me about African American cultural landmarks in Oakland"
    ]
    
    print("🏙️ BuyBlack City Guide - Testing with Your Questions")
    print("=" * 60)
    
    for i, question in enumerate(questions, 1):
        print(f"\n❓ Question {i}: {question}")
        print("-" * 40)
        
        try:
            response = await agency.get_response(question)
            print(f"🤖 Response: {response}")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("\n" + "=" * 60)
        
        # Ask if you want to continue
        if i < len(questions):
            continue_test = input("Press Enter to continue or 'q' to quit: ")
            if continue_test.lower() == 'q':
                break

if __name__ == "__main__":
    asyncio.run(test_my_questions())

