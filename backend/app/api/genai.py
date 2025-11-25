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

# System prompt for waste management chatbot

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
    conversation_history[user_id].append(
        {"role": "user", "parts": [{"text": user_message}]}
    )

    # Add assistant response
    conversation_history[user_id].append(
        {"role": "model", "parts": [{"text": assistant_message}]}
    )


# Get API configuration from environment or config (will be set per request via current_app)
def get_api_config():
    """Get API configuration from Flask app config."""
    return {
        "key": current_app.config.get("GEMINI_API_KEY", ""),
        "model": current_app.config.get("GEMINI_API_MODEL", "gemini-1.5-flash"),
        "base_url": current_app.config.get(
            "GEMINI_API_BASE_URL",
            "https://generativelanguage.googleapis.com/v1beta/models",
        ),
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
        if (
            not gemini_key
            or gemini_key == "your-gemini-api-key-here"
            or gemini_key.strip() == ""
        ):
            # Return a fallback response if API key is not configured
            current_app.logger.warning(
                "GEMINI_API_KEY not configured or using placeholder"
            )
            return jsonify(
                {
                    "response": "I'm here to help with waste management! Please configure the GEMINI_API_KEY environment variable in the .env file with your actual Gemini API key from https://aistudio.google.com/app/apikey",
                    "error": "API key not configured",
                }
            ), 200

        # Validate API key format (Gemini API keys typically start with AIza)
        if not gemini_key.startswith("AIza"):
            current_app.logger.warning(
                f"API key format may be incorrect. Gemini keys usually start with 'AIza'. Key starts with: {gemini_key[:5] if len(gemini_key) > 5 else '***'}..."
            )

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
        contents.append({"role": "user", "parts": [{"text": user_message}]})

        payload = {
            "contents": contents,
            "generationConfig": {
                "temperature": 0.7,  # Balance between creativity and consistency
                "maxOutputTokens": 200,  # Limit response length for concise answers
                "topP": 0.8,
                "topK": 40,
            },
        }

        # Add systemInstruction for models that support it
        if "1.5" in gemini_model or "2.0" in gemini_model:
            payload["systemInstruction"] = {"parts": [{"text": enhanced_system_prompt}]}
        else:
            # For older models, prepend system prompt to first message
            if contents:
                first_message = (
                    enhanced_system_prompt + "\n\n" + contents[0]["parts"][0]["text"]
                )
                contents[0]["parts"][0]["text"] = first_message

        # Set request headers
        headers = {"Content-Type": "application/json"}

        # Make API request to Google Gemini API
        try:
            # Log the API URL (without key for security) and payload structure for debugging
            current_app.logger.info(
                f"Calling Gemini API: {gemini_base_url}/{gemini_model}:generateContent"
            )
            current_app.logger.debug(
                f"Conversation history length: {len(history)} messages"
            )
            current_app.logger.debug(f"Payload keys: {list(payload.keys())}")

            response = requests.post(
                api_url,
                json=payload,
                headers=headers,
                timeout=30,  # 30 second timeout
            )

            # Log response status for debugging
            current_app.logger.info(
                f"Gemini API response status: {response.status_code}"
            )

            # Check for errors before parsing
            if response.status_code != 200:
                current_app.logger.error(
                    f"Gemini API error: Status {response.status_code}"
                )
                try:
                    error_data = response.json()
                    current_app.logger.error(f"Error details: {error_data}")
                except:
                    current_app.logger.error(
                        f"Error response text: {response.text[:500]}"
                    )

            response.raise_for_status()  # Raise exception for bad status codes

            # Parse response
            response_data = response.json()

            # Extract the response text from Gemini API response format
            # Gemini API response structure: candidates[0].content.parts[0].text
            ai_response = None
            if "candidates" in response_data and len(response_data["candidates"]) > 0:
                candidate = response_data["candidates"][0]
                # if "content" in candidate:
                #     content = candidate["content"]
                #     if "parts" in content and len(content["parts"]) > 0:
                #         ai_response = content["parts"][0].get("text", "").strip()
                if "content" in candidate:
                    content = candidate["content"]
                    parts = content.get("parts", [])
                    if parts:
                        ai_response = "".join(
                            part.get("text", "") for part in parts if "text" in part
                        ).strip()

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
                current_app.logger.warning(
                    f"Unexpected API response format: {list(response_data.keys())}"
                )
                # Check for blocking reasons
                if (
                    "candidates" in response_data
                    and len(response_data["candidates"]) > 0
                ):
                    candidate = response_data["candidates"][0]
                    if (
                        "finishReason" in candidate
                        and candidate["finishReason"] != "STOP"
                    ):
                        finish_reason = candidate.get("finishReason", "UNKNOWN")
                        current_app.logger.warning(
                            f"Response blocked with finish reason: {finish_reason}"
                        )
                        raise ValueError(
                            f"Response blocked by API. Reason: {finish_reason}"
                        )
                raise ValueError(
                    f"Empty response from API. Response keys: {list(response_data.keys())}"
                )

            # Store conversation in history
            add_to_history(user.id, user_message, ai_response)

            # Return successful response
            return jsonify({"response": ai_response, "error": None}), 200

        except requests.exceptions.Timeout:
            # Handle timeout errors
            return jsonify(
                {"error": "Request timeout. Please try again.", "response": None}
            ), 500

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
                current_app.logger.error(
                    f"Failed to parse error response: {parse_error}"
                )
                # Try to get raw response text
                try:
                    error_text = e.response.text
                    current_app.logger.error(f"Raw error response: {error_text}")
                    error_message = (
                        f"API returned error: {error_text[:200]}"  # Limit length
                    )
                except:
                    pass

            return jsonify(
                {
                    "error": error_message,
                    "error_details": error_details,
                    "response": None,
                }
            ), 500

        except requests.exceptions.RequestException as e:
            # Handle other request errors (network issues, etc.)
            return jsonify({"error": f"Network error: {str(e)}", "response": None}), 500

    except ValueError as e:
        # Handle validation errors
        return jsonify({"error": str(e), "response": None}), 400

    except Exception as e:
        # Handle unexpected errors
        current_app.logger.error(f"Unexpected error in chat endpoint: {str(e)}")
        return jsonify({"error": f"Unexpected error: {str(e)}", "response": None}), 500


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

    return jsonify({"message": "Chat history cleared successfully"}), 200

# quiz generator
@bp.route("/random-quiz", methods=["POST"])
@token_required
def random_quiz(user):
    import json
    import requests

    try:
        api = get_api_config()
        key = api["key"]
        model = api["model"]
        url = f"{api['base_url']}/{model}:generateContent?key={key}"

        prompt = """
        Generate exactly 5 MCQ quiz questions on Waste Management in India.
        Return ONLY valid JSON:
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
        Do NOT add explanation.
        """

        payload = {
            "contents": [
                {
                    "role": "user",
                    "parts": [{"text": prompt}]
                }
            ]
        }

        res = requests.post(url, json=payload)
        res.raise_for_status()

        data = res.json()

        # Extract text safely
        text = (
            data.get("candidates", [{}])[0]
                .get("content", {})
                .get("parts", [{}])[0]
                .get("text", "")
                .strip()
        )

        # If empty → LLM refused / blocked
        if not text:
            return jsonify({"error": "LLM returned empty response"}), 500

        # Try to parse JSON output
        # Clean code fences: ```json ... ```
        clean_text = text.replace("```json", "").replace("```", "").strip()

        try:
           quiz = json.loads(clean_text)
        except Exception:
           return jsonify({
        "error": "Invalid JSON after cleaning code fences",
        "raw": clean_text
           }), 500


        return jsonify(quiz), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route("/random-quiz/score", methods=["POST"])
@token_required
def random_quiz_score(user):
    """
    Update user points from random quiz.
    """
    try:
        data = request.get_json()
        score = data.get("score", 0)
        
        if not isinstance(score, int) or score < 0:
             return jsonify({"error": "Invalid score"}), 400

        # Update user points
        from app.models import db
        points_earned = score * 10
        user.points += points_earned
        db.session.commit()

        return jsonify({
            "message": "Score updated successfully",
            "new_points": user.points,
            "points_earned": points_earned
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route("/dashboard-analysis", methods=["POST"])
@token_required
def dashboard_analysis(user):
    """
    Analyze dashboard data using Gemini.
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

        prompt = f"""
        Analyze this waste management data for a user.
        Context: {context}
        Data: {dashboard_data}

        Please provide:
        1. A brief, friendly summary (2-3 sentences).
        2. 2-3 actionable suggestions (including specific campaign ideas or initiatives) based on their waste generation, engagement, and quiz performance.
        
        IMPORTANT FORMATTING INSTRUCTIONS:
        - Return raw HTML without markdown code blocks.
        - Structure:
            <p><strong>Summary:</strong> [Summary text]</p>
            <p><strong>Suggestions:</strong></p>
            <ul>
                <li>[Suggestion 1]</li>
                <li>[Suggestion 2]</li>
                <li>[Suggestion 3]</li>
            </ul>
        - Do NOT use ```html or ``` tags.
        - Keep it compact and professional.
        """

        payload = {
            "contents": [{
                "role": "user",
                "parts": [{"text": prompt}]
            }]
        }

        response = requests.post(api_url, json=payload)
        response.raise_for_status()
        
        response_data = response.json()
        
        # Extract text safely
        analysis_text = (
            response_data.get("candidates", [{}])[0]
                .get("content", {})
                .get("parts", [{}])[0]
                .get("text", "")
                .strip()
        )
        
        # Clean up any potential markdown code fences
        analysis_text = analysis_text.replace("```html", "").replace("```", "").strip()

        return jsonify({"analysis": analysis_text}), 200

    except Exception as e:
        current_app.logger.error(f"Dashboard analysis error: {str(e)}")
        return jsonify({"error": str(e)}), 500
