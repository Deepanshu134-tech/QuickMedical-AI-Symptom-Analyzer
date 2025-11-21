import json
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

# --- FLASK SETUP ---
app = Flask(__name__)
CORS(app)  # Enable cross-origin requests for frontend

# --- GEMINI CONFIGURATION ---
# Add your Gemini API key directly here
GEMINI_API_KEY = "AIzaSyCsCQuZo6U3lLs-Kh_4ct8Z2GlkNnUTbqI"
genai.configure(api_key=GEMINI_API_KEY)

# --- RESPONSE SCHEMA ---
response_schema = {
    "type": "OBJECT",
    "properties": {
        "conditions": {
            "type": "ARRAY",
            "items": {
                "type": "OBJECT",
                "properties": {
                    "name": {"type": "STRING"},
                    "probability": {"type": "STRING"}
                },
                "required": ["name", "probability"]
            }
        },
        "urgency": {"type": "INTEGER"},
        "urgencyColor": {"type": "STRING"},
        "actions": {"type": "ARRAY", "items": {"type": "STRING"}},
        "triggers": {"type": "ARRAY", "items": {"type": "STRING"}},
        "questions": {"type": "ARRAY", "items": {"type": "STRING"}}
    },
    "required": ["conditions", "urgency", "urgencyColor", "actions", "triggers", "questions"]
}

# --- GEMINI MODEL ---
model = genai.GenerativeModel(
    "gemini-2.5-flash-preview-05-20",
    generation_config={
        "response_mime_type": "application/json",
        "response_schema": response_schema
    }
)

# --- HELPER FUNCTION FOR URGENCY COLOR ---
def get_urgency_color(score: int) -> str:
    if score >= 5:
        return "#d9534f"  # High
    elif score >= 3:
        return "#f0ad4e"  # Medium
    else:
        return "#5cb85c"  # Low

# --- API ENDPOINT ---
@app.route("/analyze", methods=["POST"])
def analyze_symptoms():
    data = request.get_json()
    if not data or "symptoms" not in data:
        return jsonify({"error": "Missing 'symptoms' in request body"}), 400

    symptoms = data["symptoms"].strip()
    if not symptoms:
        return jsonify({"error": "Symptoms cannot be empty"}), 400

    system_instruction = """
    You are an AI medical assistant. Analyze patient symptoms and return a structured response.
    RULES:
    - DO NOT give a definitive diagnosis.
    - Always prioritize safety.
    - Use clear language for non-medical users.
    - Highlight urgency: 1 (low) to 5 (high).
    - Generate exactly 3 possible conditions.
    """

    prompt = f"{system_instruction}\n\nPATIENT SYMPTOMS: {symptoms}"

    try:
        response = model.generate_content(prompt)
        analysis_result = json.loads(response.text)

        # If the AI doesn't provide urgencyColor, generate it
        if "urgencyColor" not in analysis_result:
            urgency_score = analysis_result.get("urgency", 1)
            analysis_result["urgencyColor"] = get_urgency_color(urgency_score)

        return jsonify(analysis_result)

    except Exception as e:
        print(f"[ERROR] AI Analysis failed: {e}")
        return jsonify({"error": "Failed to get analysis from AI service."}), 500

# --- RUN SERVER ---
if __name__ == "__main__":
    app.run(debug=True, port=5000)
