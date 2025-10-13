import asyncio
from agency import create_agency

async def ask_your_questions():
    """Interactive script to ask your own questions"""
    agency = create_agency()
    
    print("🏙️ BuyBlack City Guide - Ask Your Own Questions!")
    print("=" * 50)
    print("Type 'quit' to exit")
    print("=" * 50)
    
    while True:
        question = input("\n❓ Your question: ").strip()
        
        if question.lower() in ['quit', 'exit', 'q']:
            print("👋 Goodbye!")
            break
            
        if not question:
            continue
            
        print("\n🤖 Thinking...")
        
        try:
            response = await agency.get_response(question)
            print(f"\n📝 Response:\n{response}")
        except Exception as e:
            print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(ask_your_questions())

