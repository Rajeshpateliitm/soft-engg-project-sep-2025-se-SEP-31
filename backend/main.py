"""Application entry point."""
import os
from dotenv import load_dotenv
from app import create_app

# Load environment variables from .env file
load_dotenv()

# Validate that .env file is being loaded
gemini_key = os.getenv("GEMINI_API_KEY", "")
if gemini_key:
    print(" Gemini API key loaded successfully")
else:
    print(" Warning: GEMINI_API_KEY not found in .env file or using placeholder value")


app = create_app()
print("App created")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
