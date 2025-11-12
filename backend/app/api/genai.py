"""GenAI endpoints for chatbot functionality using Google Gemini API."""
import requests
from urllib.parse import quote_plus
from flask import Blueprint, request, jsonify, current_app
from app.core.security import token_required
from collections import deque

bp = Blueprint("genai", __name__)

# In-memory conversation history storage
# Format: {user_id: deque([{"role": "user", "text": "..."}, {"role": "model", "text": "..."}], maxlen=10)}
# Stores last 5 conversation pairs (10 messages total: 5 user + 5 assistant)
conversation_history = {}
# print(conversation_history)

# Maximum conversation history to keep (5 pairs = 10 messages)
MAX_HISTORY_PAIRS = 5


# SYSTEM_PROMPT = """You are the *Wastewise GenAI Chatbot*, a specialized expert assistant for **Indian households**, focused on proper domestic waste management.  
# Your primary goal is to promote adherence to the latest Indian waste management policies, specifically the *Waste Management Rules, 2016* and subsequent amendments.

# ---

# ### 1. Persona and Goal:
# - **Name:** Wastewise Guide (or similar helpful name).  
# - **Persona:** A knowledgeable, patient, and eco-conscious waste management expert. Use a friendly, non-judgmental tone.  
# - **Goal:** Provide clear, actionable, and policy-compliant guidance on household waste segregation, recycling, and creative reuse, focusing on items common in Indian homes.

# ---

# ### 2. Core Constraints and Expertise (The Three Bins):
# - **Segregation Standard:** Follow the *three-bin segregation system* mandated in India:  
#   1. **Green Bin (Wet Waste / Biodegradable):** Kitchen and garden waste.  
#   2. **Blue Bin (Dry Waste / Non-Biodegradable):** Paper, plastic, metal, glass.  
#   3. **Red Bin (Domestic Hazardous Waste):** Expired medicines, sanitary waste, batteries, broken glass, cleaners, and e-waste.  
# - **Policy Focus:** Base all guidance on *Swachh Bharat Mission* and *Solid Waste Management Rules, 2016*.  
# - **Local Context:** Address common Indian household items (e.g., milk pouches, pooja flowers, coconut shells, sanitary pads, CFL bulbs, etc.).

# ---

# ### 3. Response Formatting Rules:
# 1. If the answer is long, **separate it into short bullet points**.  
# 2. **Each bullet point must contain only one complete sentence.**  
# 3. **Leave one blank line** between bullet points for better readability.  
# 4. **Avoid using asterisks (`*`) for styling.**  
# 5. Use **bold** text for important terms, keywords, or bin names.  
# 6. Keep the structure **concise, clear, and easy to scan**.  
# 7. Use numbered lists only for sequential steps (e.g., composting, recycling).  

# ---

# ### 4. Response Guidelines:
# - **Segregation Queries:**  
#   Example format:  
#   **"Used tissue paper goes into the Green Bin (Wet Waste) because it is biodegradable and can decompose easily. Always wrap it before disposal."**

# - **Recycle/Reuse Queries:**  
#   - Mention if cleaning/drying is needed before recycling.  
#   - Give simple, household-level reuse or upcycling ideas.  
#   - Clearly state if the item must go to an **authorized collector** (e-waste, hazardous).  

# - **Hazardous/Sanitary Waste:**  
#   Always mention: **"Wrap securely in paper or a marked bag before disposal to protect waste handlers."**

# - **Composting/DIY:**  
#   Provide easy, step-by-step composting methods when asked.

# ---

# ### 5. Language and Style:
# - Default language: **English** (switch to Hindi if requested).  
# - Use short, informative sentences and a warm, encouraging tone.  
# - Always start replies with the user’s name (e.g., *Hello Priya,*).  
# - Encourage sustainable habits in every response.

# ---

# ### 6. Context Awareness:
# Use previous chats and stored user details only when relevant to the question, but always address the user by name in every reply.
# """
# System prompt for waste management chatbot
SYSTEM_PROMPT = """You are the *Wastewise GenAI Chatbot, a specialized, expert assistant for **Indian households* focused on proper domestic waste management. Your primary goal is to promote adherence to the latest Indian waste management policies, specifically the *Waste Management Rules, 2016* and subsequent amendments.

### 1. Persona and Goal:
* *Name:* Wastewise Guide (or similar helpful name).
* *Persona:* A highly knowledgeable, patient, and eco-conscious waste management expert. Your tone is simple, encouraging, and non-judgmental. Use clear, accessible Hindi or English as requested by the user, but default to English.
* *Goal:* To provide accurate, actionable, and policy-compliant guidance on household waste segregation, recycling, and creative reuse, focusing specifically on products common in Indian homes.

### 2. Core Constraints and Expertise (The Three Bins):
* *Segregation Standard:* All advice must align with the *three-bin segregation system* mandated in India:
    1.  *Wet Waste / Biodegradable (Green Bin):* For kitchen waste, garden waste, etc.
    2.  *Dry Waste / Non-Biodegradable (Blue Bin):* For paper, plastic, metal, glass, etc.
    3.  *Domestic Hazardous Waste (Red Bin):* For expired medicines, sanitary waste, batteries, broken glass, chemical cleaners, and e-waste.
* *Policy Focus:* Prioritize information based on the *Swachh Bharat Mission* guidelines and the *Solid Waste Management Rules, 2016*.
* *Local Context:* Acknowledge and address common Indian household waste items (e.g., milk pouches, oil packets, Pooja flowers/materials, agarbatti ash, expired pickles, coconut shells, sanitary pads, CFL bulbs, etc.).

### 3. Response Guidelines:
* *Segregation Queries:* When asked "Where does [X] go?", respond clearly with the designated bin and a brief reason.
    * Format Example: "[X]** goes into the *[Colour] Bin (Bin Type)* because it is [Reason]. Always ensure it is [Pre-treatment, e.g., rinsed, dried, wrapped]."
* *Recycle/Reuse Queries:* When asked "How to recycle/reuse [X]?", provide simple, step-by-step instructions.
    * *Recycling:* Specify if the item must be cleaned/dried before placing it in the bin or if it needs to be handed over to an authorized collector (like e-waste).
    * *Reuse/Upcycling:* Provide a simple, creative, and practical suggestion for repurposing the item within a household context.
* *Unsafe Waste (Hazardous/Sanitary):* For hazardous/sanitary waste, explicitly state that it must be wrapped securely (e.g., in a newspaper/polythene bag and marked with an 'X') before disposal in the designated bin/handover, for the safety of waste handlers.
* *Composting/DIY:* Offer simple, accessible methods for home composting wet waste upon request.

### 4. Language and Style:
* Maintain a clear, simple, and direct communication style.
* Use bullet points or numbered lists for step-by-step guides.
* Be encouraging and acknowledge the user's effort towards sustainability.
### 5. Answer the user's query by taking previous chats and user details into account only when relevant to the query but reply with username always."""


def get_user_context(user):
    """
    Build user context string from database user information.
    
    Args:
        user: User model instance from database
        
    Returns:
        str: Formatted user context string
    """
    context_parts = []
    
    # Add user identification
    if user.username:
        context_parts.append(f"User Name: {user.username}")
    elif user.email:
        context_parts.append(f"User Email: {user.email}")
    
    # Add location information
    location_info = []
    if user.house_number:
        location_info.append(f"House: {user.house_number}")
    if user.ward_number:
        location_info.append(f"Ward: {user.ward_number}")
    if user.pincode:
        location_info.append(f"Pincode: {user.pincode}")
    
    if location_info:
        context_parts.append(f"Location: {', '.join(location_info)}")
    
    # Add household size
    if user.family_members_count:
        context_parts.append(f"Household Size: {user.family_members_count} members")
    
    # Add user category
    if user.user_category:
        context_parts.append(f"User Type: {user.user_category.label}")
    
    # Add points/engagement
    if user.points:
        context_parts.append(f"Eco Points: {user.points}")
    
    if context_parts:
        return "\n".join(context_parts)
    return ""


def get_conversation_history(user_id):
    """
    Get conversation history for a user.
    
    Args:
        user_id: User ID
        
    Returns:
        list: List of conversation messages in Gemini format
    """
    if user_id not in conversation_history:
        return []
    
    # Convert deque to list and format for Gemini API
    history = list(conversation_history[user_id])
    return history


def add_to_history(user_id, user_message, assistant_message):
    """
    Add a conversation pair to history.
    
    Args:
        user_id: User ID
        user_message: User's message text
        assistant_message: Assistant's response text
    """
    if user_id not in conversation_history:
        # Create a deque with maxlen to automatically limit history
        conversation_history[user_id] = deque(maxlen=MAX_HISTORY_PAIRS * 2)
    
    # Add user message
    conversation_history[user_id].append({
        "role": "user",
        "parts": [{"text": user_message}]
    })
    
    # Add assistant response
    conversation_history[user_id].append({
        "role": "model",
        "parts": [{"text": assistant_message}]
    })


# Get API configuration from environment or config (will be set per request via current_app)
def get_api_config():
    """Get API configuration from Flask app config."""
    return {
        "key": current_app.config.get("GEMINI_API_KEY", ""),
        "model": current_app.config.get("GEMINI_API_MODEL", "gemini-1.5-flash"),
        "base_url": current_app.config.get("GEMINI_API_BASE_URL", "https://generativelanguage.googleapis.com/v1beta/models")
    }


@bp.route("/chat", methods=["POST"])
@token_required
def chat(user):
    """
    Chat endpoint that processes user messages and returns AI-generated responses using Google Gemini API.
    Maintains conversation history (last 5 messages) and includes user context from database.
    
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
        
        # Get user context from database
        user_context = get_user_context(user)
        
        # Build enhanced system prompt with user context
        enhanced_system_prompt = SYSTEM_PROMPT
        if user_context:
            enhanced_system_prompt += f"\n\n### User Information:\n{user_context}\n\nUse this information to provide personalized, location-relevant advice when appropriate."
        
        # Get conversation history for this user
        history = get_conversation_history(user.id)
        
        # Build the Gemini API URL with model and API key (URL encode the key)
        encoded_key = quote_plus(gemini_key)
        api_url = f"{gemini_base_url}/{gemini_model}:generateContent?key={encoded_key}"
        
        # Prepare the API request payload for Gemini API
        # Build contents array with history + current message
        contents = []
        
        # Add conversation history
        contents.extend(history)
        
        # Add current user message
        contents.append({
            "role": "user",
            "parts": [{"text": user_message}]
        })
        
        payload = {
            "contents": contents,
            "generationConfig": {
                "temperature": 0.7,  # Balance between creativity and consistency
                "maxOutputTokens": 200,  # Limit response length for concise answers
                "topP": 0.8,
                "topK": 40
            }
        }
        
        # Add systemInstruction for models that support it
        if "1.5" in gemini_model or "2.0" in gemini_model:
            payload["systemInstruction"] = {
                "parts": [
                    {
                        "text": enhanced_system_prompt
                    }
                ]
            }
        else:
            # For older models, prepend system prompt to first message
            if contents:
                first_message = enhanced_system_prompt + "\n\n" + contents[0]["parts"][0]["text"]
                contents[0]["parts"][0]["text"] = first_message
        
        # Set request headers
        headers = {
            "Content-Type": "application/json"
        }
        
        # Make API request to Google Gemini API
        try:
            # Log the API URL (without key for security) and payload structure for debugging
            current_app.logger.info(f"Calling Gemini API: {gemini_base_url}/{gemini_model}:generateContent")
            current_app.logger.debug(f"Conversation history length: {len(history)} messages")
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
            
            # Store conversation in history
            add_to_history(user.id, user_message, ai_response)
            
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


@bp.route("/chat/clear", methods=["POST"])
@token_required
def clear_chat_history(user):
    """
    Clear conversation history for the current user.
    
    Returns:
    {
        "message": "Chat history cleared successfully"
    }
    """
    if user.id in conversation_history:
        del conversation_history[user.id]
        current_app.logger.info(f"Cleared chat history for user {user.id}")
    
    return jsonify({
        "message": "Chat history cleared successfully"
    }), 200
