"""GenAI endpoints for chatbot functionality using Google Gemini API."""
import requests
from urllib.parse import quote_plus
from flask import Blueprint, request, jsonify, current_app
from app.core.security import token_required

bp = Blueprint("genai", __name__)

# Get API configuration from environment or config (will be set per request via current_app)
def get_api_config():
    """Get API configuration from Flask app config."""
    return {
        "key": current_app.config.get("GEMINI_API_KEY", ""),
        "model": current_app.config.get("GEMINI_API_MODEL", "gemini-1.5-flash"),
        "base_url": current_app.config.get("GEMINI_API_BASE_URL", "https://generativelanguage.googleapis.com/v1beta/models")
    }

# System prompt for waste management chatbot
SYSTEM_PROMPT = """You are WasteWise, a helpful waste management assistant. 
Provide concise, practical answers about waste segregation, recycling, composting, and environmental sustainability.
Keep responses brief (2-3 sentences maximum) and actionable.
Focus on waste management best practices, recycling tips, and environmental conservation."""


@bp.route("/chat", methods=["POST"])
@token_required
def chat(user):
    """
    Chat endpoint that processes user messages and returns AI-generated responses using Google Gemini API.
    
    Expected request body:
    {
        "message": "user's question about waste management"
    }
    
    Returns:
    {
        "response": "AI-generated response",
        "error": null (if successful)
    }
    
    Errors:
    - 400: Missing message in request
    - 500: API error or configuration issue
    """
    try:
        # Validate request data
        data = request.get_json()
        if not data:
            return jsonify({"error": "Request body is required", "response": None}), 400
        
        user_message = data.get("message", "").strip()
        if not user_message:
            return jsonify({"error": "Message is required", "response": None}), 400
        
        # Get API configuration
        api_config = get_api_config()
        gemini_key = api_config["key"]
        gemini_model = api_config["model"]
        gemini_base_url = api_config["base_url"]
        current_app.logger.info("Gemini API configuration loaded")
        # Check if API key is configured
        if not gemini_key or gemini_key == "your-gemini-api-key-here" or gemini_key.strip() == "":
            # Return a fallback response if API key is not configured
            current_app.logger.warning("GEMINI_API_KEY not configured or using placeholder")
            return jsonify({
                "response": "I'm here to help with waste management! Please configure the GEMINI_API_KEY environment variable in the .env file with your actual Gemini API key from https://aistudio.google.com/app/apikey",
                "error": "API key not configured"
            }), 200
        
        # Validate API key format (Gemini API keys typically start with AIza)
        if not gemini_key.startswith("AIza"):
            current_app.logger.warning(f"API key format may be incorrect. Gemini keys usually start with 'AIza'. Key starts with: {gemini_key[:5] if len(gemini_key) > 5 else '***'}...")
        
        # Log API key status (masked for security)
        masked_key = gemini_key[:8] + "..." + gemini_key[-4:] if len(gemini_key) > 12 else "***"
        current_app.logger.info(f"Using Gemini API key: {masked_key}")
        
        # Build the Gemini API URL with model and API key (URL encode the key)
        # Properly encode the API key to handle special characters
        encoded_key = quote_plus(gemini_key)
        api_url = f"{gemini_base_url}/{gemini_model}:generateContent?key={encoded_key}"
        
        # Prepare the API request payload for Gemini API
        # Combine system prompt with user message for compatibility
        # Some Gemini API versions may not support systemInstruction in all models
        full_prompt = f"{SYSTEM_PROMPT}\n\nUser: {user_message}\nAssistant:"
        
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": full_prompt
                        }
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.7,  # Balance between creativity and consistency
                "maxOutputTokens": 150,  # Limit response length for concise answers (increased slightly)
                "topP": 0.8,
                "topK": 40
            }
        }
        
        # Try to use systemInstruction if supported (for newer models)
        # If the model doesn't support it, the prompt above will work
        try:
            # Only add systemInstruction for models that support it
            if "1.5" in gemini_model or "2.0" in gemini_model:
                payload["systemInstruction"] = {
                    "parts": [
                        {
                            "text": SYSTEM_PROMPT
                        }
                    ]
                }
                # If using systemInstruction, use only user message in contents
                payload["contents"][0]["parts"][0]["text"] = user_message
        except:
            # Fallback to prompt-based approach if there's an issue
            pass
        
        # Set request headers
        headers = {
            "Content-Type": "application/json"
        }
        
        # Make API request to Google Gemini API
        try:
            # Log the API URL (without key for security) and payload structure for debugging
            current_app.logger.info(f"Calling Gemini API: {gemini_base_url}/{gemini_model}:generateContent")
            current_app.logger.debug(f"Payload keys: {list(payload.keys())}")
            
            response = requests.post(
                api_url,
                json=payload,
                headers=headers,
                timeout=30  # 30 second timeout
            )
            
            # Log response status for debugging
            current_app.logger.info(f"Gemini API response status: {response.status_code}")
            
            # Check for errors before parsing
            if response.status_code != 200:
                current_app.logger.error(f"Gemini API error: Status {response.status_code}")
                try:
                    error_data = response.json()
                    current_app.logger.error(f"Error details: {error_data}")
                except:
                    current_app.logger.error(f"Error response text: {response.text[:500]}")
            
            response.raise_for_status()  # Raise exception for bad status codes
            
            # Parse response
            response_data = response.json()
            
            # Extract the response text from Gemini API response format
            # Gemini API response structure: candidates[0].content.parts[0].text
            ai_response = None
            if "candidates" in response_data and len(response_data["candidates"]) > 0:
                candidate = response_data["candidates"][0]
                if "content" in candidate:
                    content = candidate["content"]
                    if "parts" in content and len(content["parts"]) > 0:
                        ai_response = content["parts"][0].get("text", "").strip()
            
            # Fallback: try alternative response formats
            if not ai_response:
                if "text" in response_data:
                    ai_response = response_data["text"].strip()
                elif "response" in response_data:
                    ai_response = response_data["response"].strip()
                elif "message" in response_data:
                    ai_response = response_data["message"].strip()
            
            # Validate that we got a response
            if not ai_response:
                # Log the response structure for debugging if response is empty
                current_app.logger.warning(f"Unexpected API response format: {list(response_data.keys())}")
                # Check for blocking reasons
                if "candidates" in response_data and len(response_data["candidates"]) > 0:
                    candidate = response_data["candidates"][0]
                    if "finishReason" in candidate and candidate["finishReason"] != "STOP":
                        finish_reason = candidate.get("finishReason", "UNKNOWN")
                        current_app.logger.warning(f"Response blocked with finish reason: {finish_reason}")
                        raise ValueError(f"Response blocked by API. Reason: {finish_reason}")
                raise ValueError(f"Empty response from API. Response keys: {list(response_data.keys())}")
            
            # Return successful response
            return jsonify({
                "response": ai_response,
                "error": None
            }), 200
            
        except requests.exceptions.Timeout:
            # Handle timeout errors
            return jsonify({
                "error": "Request timeout. Please try again.",
                "response": None
            }), 500
            
        except requests.exceptions.HTTPError as e:
            # Handle HTTP errors (4xx, 5xx)
            error_message = f"API error: {e.response.status_code}"
            error_details = None
            try:
                error_data = e.response.json()
                current_app.logger.error(f"Gemini API error response: {error_data}")
                
                if "error" in error_data:
                    error_info = error_data["error"]
                    if "message" in error_info:
                        error_message = error_info["message"]
                        error_details = error_info
                    elif "status" in error_info:
                        error_message = f"{error_info.get('status', 'Unknown error')}: {error_info.get('message', '')}"
                        error_details = error_info
                # Gemini API might return error directly
                elif "message" in error_data:
                    error_message = error_data["message"]
                    error_details = error_data
            except Exception as parse_error:
                current_app.logger.error(f"Failed to parse error response: {parse_error}")
                # Try to get raw response text
                try:
                    error_text = e.response.text
                    current_app.logger.error(f"Raw error response: {error_text}")
                    error_message = f"API returned error: {error_text[:200]}"  # Limit length
                except:
                    pass
            
            return jsonify({
                "error": error_message,
                "error_details": error_details,
                "response": None
            }), 500
            
        except requests.exceptions.RequestException as e:
            # Handle other request errors (network issues, etc.)
            return jsonify({
                "error": f"Network error: {str(e)}",
                "response": None
            }), 500
            
    except ValueError as e:
        # Handle validation errors
        return jsonify({
            "error": str(e),
            "response": None
        }), 400
        
    except Exception as e:
        # Handle unexpected errors
        current_app.logger.error(f"Unexpected error in chat endpoint: {str(e)}")
        return jsonify({
            "error": f"Unexpected error: {str(e)}",
            "response": None
        }), 500
