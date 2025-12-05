"""
GenAI endpoints for waste management chatbot and quiz generation.

Provides:
- /chat: Interactive chatbot with conversation history
- /chat/clear: Clear user's conversation history
- /random-quiz: Generate random waste management quiz
- /random-quiz/score: Submit quiz score and update points
- /dashboard-analysis: Analyze user dashboard data
"""

import json
import requests
from urllib.parse import quote_plus
from collections import deque
from flask import Blueprint, request, jsonify, current_app
from app.core.security import token_required
from app.models import db

bp = Blueprint("genai", __name__)

# ============================================================================
# CONFIGURATION
# ============================================================================

# In-memory conversation history: {user_id: deque([messages], maxlen=10)}
# Stores last 5 conversation pairs (5 user + 5 model messages = 10 total)
conversation_history = {} 
MAX_HISTORY_PAIRS = 5

# SYSTEM_PROMPT = """You are the Wastewise GenAI Chatbot, a specialized assistant for Indian households focused on proper domestic waste management. Your primary goal is to promote adherence to the Solid Waste Management Rules 2016 and subsequent amendments.

# 1. Persona and Goal:
# - Name: Wastewise Guide
# - Persona: A knowledgeable, patient, eco-conscious waste management expert with a simple and friendly tone
# - Goal: Provide accurate, actionable, and policy-compliant guidance on household waste segregation, recycling, composting, and safe disposal

# 2. Core Constraints and Expertise:
# - Always follow the three-bin system: Green Bin (wet biodegradable), Blue Bin (dry non-biodegradable), Red Bin (domestic hazardous)
# - Follow Solid Waste Management Rules 2016 and Swachh Bharat Mission guidelines
# - Provide India-specific waste advice for milk pouches, oil packets, flowers, coconut shells, diapers, sanitary pads, CFL bulbs, batteries, medicine strips, e-waste, etc.

# 3. Response Guidelines:
# - For segregation: "X should be disposed in the [Colour] Bin ([Bin Type]) because it is [Reason], and it must be [Pre-treatment]"
# - For recycling: Give clear step-by-step instructions using one-sentence bullet points
# - For hazardous waste: Mention wrapping securely, marking if needed, and disposal in Red Bin or authorized collector
# - For composting: Give simple, practical, beginner-friendly steps
# - All advice must be actionable and easy for Indian households

# 4. Language and Style:
# - Use clear, simple English unless user requests Hindi
# - Do NOT use Markdown symbols (*, **, _, #)
# - Bullet points: start on new line, begin with hyphen + space, one concise sentence each
# - Maintain encouraging, non-judgmental tone

# 5. Personalization:
# - Consider previous conversation context only when relevant
# - Always prioritize accuracy, safety, and compliance with Indian waste management standards

# 6. WasteWise Points & Rewards System:
# - Daily Quiz: 10 points per correct answer
# - Campaign Registration: 20 points
# - Waste Disposal (when pickup accepted):
#   - +5 points for separating waste (Wet/Dry/Hazardous)
#   - +10 points for recycling
#   - Total possible per pickup: 15 points
# - Penalty: -5 points if pickup rejected
# - Encourage users to maintain streaks and climb the Community Leaderboard
# """

SYSTEM_PROMPT = """
You are the Wastewise GenAI Chatbot, a specialized assistant for Indian households focused on proper domestic waste management. Your primary goal is to promote adherence to the Solid Waste Management Rules 2016 and subsequent amendments.

1. Persona and Goal:
- Name: Wastewise Guide.
- Persona: A knowledgeable, patient, eco-conscious waste management expert with a simple and friendly tone.
- Goal: Provide accurate, actionable, and policy-compliant guidance on household waste segregation, recycling, composting, and safe disposal for items commonly found in Indian homes.

2. Core Constraints and Expertise:
- Always follow the three-bin system used in India: Green Bin for wet biodegradable waste, Blue Bin for dry non-biodegradable waste, and Red Bin for domestic hazardous waste.
- Follow Solid Waste Management Rules 2016, Swachh Bharat Mission guidelines, and local municipal practices.
- Provide India-specific waste advice for items like milk pouches, oil packets, pooja materials, flowers, coconut shells, diapers, sanitary pads, CFL bulbs, batteries, medicine strips, e-waste, and more.

3. Response Guidelines:
- For segregation questions, always reply in this format: “X should be disposed in the [Colour] Bin ([Bin Type]) because it is [Reason], and it must be [Pre-treatment].”
- For recycling or reuse questions, give clear step-by-step instructions using one-sentence bullet points.
- For hazardous or sanitary waste, clearly mention that the item must be wrapped securely, marked if needed, and disposed of in the Red Bin or handed to an authorized collector.
- For composting or DIY queries, give simple, practical, beginner-friendly steps.
- All advice must be actionable and easy for Indian households to follow.

4. Language and Style:
- Use clear, simple English unless the user specifically requests Hindi.
- Do not use Markdown symbols like *, **, _, or # in any answer.
- Bullet points must always start on a new line, begin with a hyphen followed by a space, and contain only one concise sentence.
- Do not merge multiple bullet points into one paragraph.
- Maintain an encouraging, non-judgmental tone and acknowledge the user's effort toward sustainability.

5. Personalization:
- Consider previous conversation context and user preferences only when relevant.
- Always prioritize accuracy, safety, and compliance with Indian waste management standards.

6. Answer the user's query by taking previous chats and user details into account only when relevant to the query but reply with username first time or when required.

7. WasteWise Points & Rewards System (Internal Policy):
- If users ask about points or how to earn them, explain the following rules clearly:
    * Daily Quiz: Earn 10 points for every correct answer.
    * Campaign Registration: Earn 20 points for registering for a campaign.
    * Waste Disposal: Earn points when your pickup is accepted by a collector:
        - +5 points for separating waste (Wet/Dry/Hazardous).
        - +10 points for recycling (if marked as recycled).
        - Total possible per pickup: 15 points.
    * Penalty: -5 points if a pickup request is rejected by the collector.
- Encourage users to maintain a streak of logging waste and taking quizzes to climb the Community Leaderboard.

"""

RANDOM_QUIZ_PROMPT = """Generate exactly 5 MCQ quiz questions on Waste Management in India.
Return ONLY valid JSON (no markdown, no code fences):
{
  "questions": [
    {
      "question_text": "...",
      "options": [
        {"text": "...", "is_correct": false},
        {"text": "...", "is_correct": true},
        {"text": "...", "is_correct": false},
        {"text": "...", "is_correct": false}
      ]
    }
  ]
}
Do NOT add explanations or code fences."""

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================


def get_api_config():
    """
    Get Gemini API configuration from Flask app config.

    Returns:
        dict: API key, model name, and base URL
    """
    return {
        "key": current_app.config.get("GEMINI_API_KEY", ""),
        "model": current_app.config.get("GEMINI_API_MODEL", "gemini-1.5-flash"),
        "base_url": current_app.config.get(
            "GEMINI_API_BASE_URL",
            "https://generativelanguage.googleapis.com/v1beta/models",
        ),
    }


def get_user_context(user):
    """
    Build personalized user context string from database.

    Args:
        user: User model instance

    Returns:
        str: Formatted user context for LLM personalization
    """
    context_parts = []

    # User identification
    if user.username:
        context_parts.append(f"User Name: {user.username}")
    elif user.email:
        context_parts.append(f"User Email: {user.email}")

    # Location information
    location_info = []
    if user.house_number:
        location_info.append(f"House: {user.house_number}")
    if user.ward_number:
        location_info.append(f"Ward: {user.ward_number}")
    if user.pincode:
        location_info.append(f"Pincode: {user.pincode}")

    if location_info:
        context_parts.append(f"Location: {', '.join(location_info)}")

    # Household size
    if user.family_members_count:
        context_parts.append(f"Household Size: {user.family_members_count} members")

    # User category
    if user.user_category:
        context_parts.append(f"User Type: {user.user_category.label}")

    # Engagement points
    if user.points:
        context_parts.append(f"Eco Points: {user.points}")

    return "\n".join(context_parts) if context_parts else ""


def get_conversation_history(user_id):
    """
    Retrieve conversation history for a user.

    Args:
        user_id: User ID

    Returns:
        list: List of conversation messages in Gemini API format
    """
    if user_id not in conversation_history:
        return []
    return list(conversation_history[user_id])


def add_to_history(user_id, user_message, assistant_message):
    """
    Add a user-assistant message pair to conversation history.

    Args:
        user_id: User ID
        user_message: User's message text
        assistant_message: Assistant's response text
    """
    if user_id not in conversation_history:
        conversation_history[user_id] = deque(maxlen=MAX_HISTORY_PAIRS * 2)

    conversation_history[user_id].append(
        {"role": "user", "parts": [{"text": user_message}]}
    )
    conversation_history[user_id].append(
        {"role": "model", "parts": [{"text": assistant_message}]}
    )


def extract_gemini_response(response_data):
    """
    Extract text from Gemini API response.

    Args:
        response_data: JSON response from Gemini API

    Returns:
        str: Extracted response text or None if not found
    """
    # Primary extraction path
    if "candidates" in response_data and len(response_data["candidates"]) > 0:
        candidate = response_data["candidates"][0]
        if "content" in candidate:
            parts = candidate["content"].get("parts", [])
            if parts:
                return "".join(
                    part.get("text", "") for part in parts if "text" in part
                ).strip()

    # Fallback paths
    for key in ["text", "response", "message"]:
        if key in response_data:
            return response_data[key].strip()

    return None


def check_api_key_configured(gemini_key):
    """
    Validate that API key is properly configured.

    Args:
        gemini_key: API key string

    Returns:
        tuple: (is_valid, error_message)
    """
    if not gemini_key or gemini_key == "your-gemini-api-key-here" or not gemini_key.strip():
        return False, "API key not configured"

    if not gemini_key.startswith("AIza"):
        current_app.logger.warning(
            f"API key format may be incorrect. Expected to start with 'AIza', got: {gemini_key[:5]}..."
        )

    return True, None


def handle_api_error(error):
    """
    Handle API errors and extract meaningful error messages.

    Args:
        error: Exception from requests library

    Returns:
        tuple: (error_message, error_details, status_code)
    """
    if isinstance(error, requests.exceptions.Timeout):
        return "Request timeout. Please try again.", None, 500

    if isinstance(error, requests.exceptions.HTTPError):
        error_message = f"API error: {error.response.status_code}"
        error_details = None

        try:
            error_data = error.response.json()
            current_app.logger.error(f"Gemini API error: {error_data}")

            if "error" in error_data:
                error_info = error_data["error"]
                error_message = error_info.get("message", error_message)
                error_details = error_info
            elif "message" in error_data:
                error_message = error_data["message"]
                error_details = error_data
        except Exception as parse_error:
            current_app.logger.error(f"Failed to parse error: {parse_error}")

        return error_message, error_details, 500

    if isinstance(error, requests.exceptions.RequestException):
        return f"Network error: {str(error)}", None, 500

    if isinstance(error, ValueError):
        return str(error), None, 400

    return f"Unexpected error: {str(error)}", None, 500


# ============================================================================
# ENDPOINTS
# ============================================================================


@bp.route("/chat", methods=["POST"])
@token_required
def chat(user):
    """
    Chat endpoint for interactive waste management guidance.

    Maintains conversation history (last 5 pairs) and personalizes responses
    based on user context from database.

    Request body:
        {
            "message": "user's question about waste management"
        }

    Response:
        {
            "response": "AI-generated response",
            "error": null (if successful)
        }

    Status codes:
        200: Success or API key not configured (fallback response)
        400: Invalid request (missing/empty message)
        500: API error or network issue
    """
    try:
        # Validate request
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

        # Check API key
        is_valid, error_msg = check_api_key_configured(gemini_key)
        if not is_valid:
            current_app.logger.warning(f"GenAI chat: {error_msg}")
            return jsonify(
                {
                    "response": "I'm here to help with waste management! Please configure the GEMINI_API_KEY environment variable in the .env file with your actual Gemini API key from https://aistudio.google.com/app/apikey",
                    "error": error_msg,
                }
            ), 200

        # Build enhanced system prompt with user context
        user_context = get_user_context(user)
        enhanced_prompt = SYSTEM_PROMPT
        if user_context:
            enhanced_prompt += f"\n\n### User Information:\n{user_context}\n\nUse this information to provide personalized, location-relevant advice when appropriate."

        # Get conversation history
        history = get_conversation_history(user.id)

        # Build API request
        encoded_key = quote_plus(gemini_key)
        api_url = f"{gemini_base_url}/{gemini_model}:generateContent?key={encoded_key}"

        contents = []
        contents.extend(history)
        contents.append({"role": "user", "parts": [{"text": user_message}]})

        payload = {
            "contents": contents,
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 200,
                "topP": 0.8,
                "topK": 40,
            },
        }

        # Add system instruction for supported models
        if "1.5" in gemini_model or "2.0" in gemini_model:
            payload["systemInstruction"] = {"parts": [{"text": enhanced_prompt}]}
        else:
            # Fallback for older models
            if contents:
                contents[0]["parts"][0]["text"] = (
                    enhanced_prompt + "\n\n" + contents[0]["parts"][0]["text"]
                )

        headers = {"Content-Type": "application/json"}

        # Call Gemini API
        current_app.logger.info(
            f"Calling Gemini API for user {user.id}: {gemini_model}"
        )

        response = requests.post(
            api_url,
            json=payload,
            headers=headers,
            timeout=30,
        )

        current_app.logger.info(f"Gemini API response: {response.status_code}")

        if response.status_code != 200:
            current_app.logger.error(f"Gemini API error: {response.status_code}")
            try:
                current_app.logger.error(f"Error details: {response.json()}")
            except:
                current_app.logger.error(f"Error text: {response.text[:500]}")

        response.raise_for_status()

        # Extract response
        response_data = response.json()
        ai_response = extract_gemini_response(response_data)

        if not ai_response:
            # Check for blocking reasons
            if "candidates" in response_data and len(response_data["candidates"]) > 0:
                candidate = response_data["candidates"][0]
                if candidate.get("finishReason") != "STOP":
                    finish_reason = candidate.get("finishReason", "UNKNOWN")
                    current_app.logger.warning(
                        f"Response blocked: {finish_reason}"
                    )
                    raise ValueError(f"Response blocked by API. Reason: {finish_reason}")

            raise ValueError("Empty response from API")

        # Store in history
        add_to_history(user.id, user_message, ai_response)

        return jsonify({"response": ai_response, "error": None}), 200

    except (requests.exceptions.Timeout, requests.exceptions.HTTPError, 
            requests.exceptions.RequestException, ValueError, Exception) as e:
        error_message, error_details, status_code = handle_api_error(e)
        
        if status_code == 500 and not isinstance(e, (requests.exceptions.Timeout, 
                                                       requests.exceptions.HTTPError,
                                                       requests.exceptions.RequestException)):
            current_app.logger.error(f"Unexpected error in chat: {str(e)}")
        
        response_data = {"error": error_message, "response": None}
        if error_details:
            response_data["error_details"] = error_details
        
        return jsonify(response_data), status_code


@bp.route("/chat/clear", methods=["POST"])
@token_required
def clear_chat_history(user):
    """
    Clear conversation history for the authenticated user.

    This endpoint is idempotent: it returns success whether or not
    the user had any history stored.

    Response:
        {
            "message": "Chat history cleared successfully"
        }

    Status codes:
        200: Success (always)
    """
    if user.id in conversation_history:
        del conversation_history[user.id]
        current_app.logger.info(f"Cleared chat history for user {user.id}")

    return jsonify({"message": "Chat history cleared successfully"}), 200


@bp.route("/random-quiz", methods=["POST"])
@token_required
def random_quiz(user):
    """
    Generate a random waste management quiz with 5 MCQ questions.

    Response:
        {
            "questions": [
                {
                    "question_text": "...",
                    "options": [
                        {"text": "...", "is_correct": false},
                        ...
                    ]
                },
                ...
            ]
        }

    Status codes:
        200: Success
        500: API error or invalid response format
    """
    try:
        api_config = get_api_config()
        gemini_key = api_config["key"]
        gemini_model = api_config["model"]
        gemini_base_url = api_config["base_url"]

        if not gemini_key:
            return jsonify({"error": "API key not configured"}), 500

        encoded_key = quote_plus(gemini_key)
        api_url = f"{gemini_base_url}/{gemini_model}:generateContent?key={encoded_key}"

        payload = {
            "contents": [
                {
                    "role": "user",
                    "parts": [{"text": RANDOM_QUIZ_PROMPT}]
                }
            ]
        }

        response = requests.post(api_url, json=payload, timeout=30)
        response.raise_for_status()

        response_data = response.json()
        text = extract_gemini_response(response_data)

        if not text:
            return jsonify({"error": "LLM returned empty response"}), 500

        # Clean code fences
        clean_text = text.replace("```json", "").replace("```", "").strip()

        try:
            quiz = json.loads(clean_text)
            return jsonify(quiz), 200
        except json.JSONDecodeError:
            current_app.logger.error(f"Invalid JSON from LLM: {clean_text[:200]}")
            return jsonify({
                "error": "Invalid JSON from LLM",
                "raw": clean_text[:500]
            }), 500

    except requests.exceptions.RequestException as e:
        current_app.logger.error(f"Random quiz API error: {str(e)}")
        return jsonify({"error": f"API error: {str(e)}"}), 500

    except Exception as e:
        current_app.logger.error(f"Random quiz error: {str(e)}")
        return jsonify({"error": str(e)}), 500


@bp.route("/random-quiz/score", methods=["POST"])
@token_required
def random_quiz_score(user):
    """
    Submit quiz score and update user points.

    Request body:
        {
            "score": 3  (number of correct answers)
        }

    Response:
        {
            "message": "Score updated successfully",
            "new_points": 150,
            "points_earned": 30
        }

    Status codes:
        200: Success
        400: Invalid score
        500: Database error
    """
    try:
        data = request.get_json()
        score = data.get("score", 0)

        # Validate score
        if not isinstance(score, int) or score < 0:
            return jsonify({"error": "Invalid score"}), 400

        # Update user points (10 points per correct answer)
        points_earned = score * 10
        user.points += points_earned
        db.session.commit()

        current_app.logger.info(
            f"User {user.id} earned {points_earned} points from quiz"
        )

        return jsonify({
            "message": "Score updated successfully",
            "new_points": user.points,
            "points_earned": points_earned
        }), 200

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error updating quiz score: {str(e)}")
        return jsonify({"error": str(e)}), 500


@bp.route("/dashboard-analysis", methods=["POST"])
@token_required
def dashboard_analysis(user):
    """
    Analyze user dashboard data and provide personalized insights.

    Request body:
        {
            "data": {...},  (dashboard data to analyze)
            "context": "Weekly"  (optional, default: "Dashboard Data")
        }

    Response:
        {
            "analysis": "<p>HTML formatted analysis</p>"
        }

    Status codes:
        200: Success
        400: Missing data
        500: API error or key not configured
    """
    try:
        data = request.get_json()
        dashboard_data = data.get("data")
        context = data.get("context", "Dashboard Data")

        if not dashboard_data:
            return jsonify({"error": "No data provided"}), 400

        api_config = get_api_config()
        gemini_key = api_config["key"]
        gemini_model = api_config["model"]
        gemini_base_url = api_config["base_url"]

        if not gemini_key:
            return jsonify({"error": "API key not configured"}), 500

        encoded_key = quote_plus(gemini_key)
        api_url = f"{gemini_base_url}/{gemini_model}:generateContent?key={encoded_key}"

        prompt = f"""Analyze this waste management data for a user.
Context: {context}
Data: {dashboard_data}

Please provide:
1. A brief, friendly summary (2-3 sentences)
2. 2-3 actionable suggestions based on their waste generation, engagement, and quiz performance

IMPORTANT: Return raw HTML without markdown code blocks. Structure:
<p><strong>Summary:</strong> [Summary text]</p>
<p><strong>Suggestions:</strong></p>
<ul>
<li>[Suggestion 1]</li>
<li>[Suggestion 2]</li>
<li>[Suggestion 3]</li>
</ul>

Do NOT use ```html or ``` tags. Keep it compact and professional."""

        payload = {
            "contents": [{
                "role": "user",
                "parts": [{"text": prompt}]
            }]
        }

        response = requests.post(api_url, json=payload, timeout=30)
        response.raise_for_status()

        response_data = response.json()
        analysis_text = extract_gemini_response(response_data)

        if not analysis_text:
            return jsonify({"error": "Empty response from API"}), 500

        # Clean code fences
        analysis_text = analysis_text.replace("```html", "").replace("```", "").strip()

        return jsonify({"analysis": analysis_text}), 200

    except requests.exceptions.RequestException as e:
        current_app.logger.error(f"Dashboard analysis API error: {str(e)}")
        return jsonify({"error": f"API error: {str(e)}"}), 500

    except Exception as e:
        current_app.logger.error(f"Dashboard analysis error: {str(e)}")
        return jsonify({"error": str(e)}), 500
