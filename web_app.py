import gradio as gr
import asyncio
from agency import create_agency
import json

# Initialize the agency
agency = create_agency()

def chat_with_agency(message, history):
    """Handle chat interactions with the agency"""
    try:
        # Run the async agency response
        result = asyncio.run(agency.get_response(message))
        
        # Extract the final output from the RunResult
        if hasattr(result, 'final_output'):
            return str(result.final_output)
        elif hasattr(result, 'output'):
            return str(result.output)
        else:
            return str(result)
            
    except Exception as e:
        return f"Error getting response: {str(e)}"

def create_interface():
    """Create the Gradio interface"""
    
    with gr.Blocks(title="BuyBlack City Guide", theme=gr.themes.Soft()) as demo:
        gr.Markdown("""
        # 🏙️ BuyBlack City Guide
        
        Discover Black-owned businesses, cultural landmarks, and create personalized itineraries for Oakland, CA.
        
        **Try asking:**
        - "Find Black-owned restaurants in Oakland"
        - "Plan a 2-day cultural trip to Oakland"
        - "What are the best Black-owned bakeries?"
        - "Tell me about African American cultural sites in Oakland"
        """)
        
        # Chat interface
        chatbot = gr.Chatbot(
            label="Chat with BuyBlack City Guide",
            height=500,
            show_label=True,
            type="messages"  # Fix deprecation warning
        )
        
        msg = gr.Textbox(
            label="Your message",
            placeholder="Ask about Black-owned businesses, cultural sites, or trip planning...",
            lines=2
        )
        
        with gr.Row():
            send_btn = gr.Button("Send", variant="primary")
            clear_btn = gr.Button("Clear")
        
        # Example queries
        gr.Markdown("### 💡 Quick Start Examples:")
        
        with gr.Row():
            example1 = gr.Button("🍽️ Find Restaurants", size="sm")
            example2 = gr.Button("🧳 Plan Trip", size="sm")
            example3 = gr.Button("🏛️ Cultural Sites", size="sm")
            example4 = gr.Button("🥖 Find Bakeries", size="sm")
        
        # Event handlers
        def respond(message, history):
            if not message.strip():
                return history, ""
            
            response = chat_with_agency(message, history)
            # For messages type, format as [{"role": "user", "content": message}, {"role": "assistant", "content": response}]
            history.append({"role": "user", "content": message})
            history.append({"role": "assistant", "content": response})
            return history, ""
        
        def clear():
            return [], ""
        
        # Connect events
        msg.submit(respond, [msg, chatbot], [chatbot, msg])
        send_btn.click(respond, [msg, chatbot], [chatbot, msg])
        clear_btn.click(clear, outputs=[chatbot, msg])
        
        # Example button handlers
        example1.click(lambda: "Find Black-owned restaurants in Oakland", outputs=msg)
        example2.click(lambda: "Plan a 2-day cultural trip to Oakland focusing on Black history and food", outputs=msg)
        example3.click(lambda: "What are the most important cultural landmarks in Oakland related to Black history?", outputs=msg)
        example4.click(lambda: "Find Black-owned bakeries in Oakland", outputs=msg)
    
    return demo

if __name__ == "__main__":
    demo = create_interface()
    demo.launch(
        server_name="0.0.0.0",  # Allow external access
        server_port=7860,       # Default Gradio port
        share=False,            # Set to True for public sharing
        debug=True
    )

