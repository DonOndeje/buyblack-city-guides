"""
Railway deployment configuration for BuyBlack City Guide
"""
import os
from web_app import create_interface

# Railway automatically sets PORT environment variable
PORT = int(os.environ.get("PORT", 7860))

if __name__ == "__main__":
    demo = create_interface()
    demo.launch(
        server_name="0.0.0.0",
        server_port=PORT,
        share=False
    )

