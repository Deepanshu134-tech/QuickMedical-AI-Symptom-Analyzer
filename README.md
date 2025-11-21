An AI-Powered Web Assistant for Symptom Analysis
QuickMedical AI is a minimalist web application that uses the Google Gemini API to analyze patient-reported symptoms and provide structured, non-diagnostic guidance. It is designed to offer quick, preliminary insights into possible conditions, urgency level, and recommended actions, emphasizing the necessity of consulting a medical professional.

 Key Features
Symptom Analysis: Users input their symptoms into a text area for AI analysis.

Structured AI Output: The backend is configured to enforce a structured JSON response from the Gemini model.

Safety-First Design: The AI is strictly instructed not to provide a definitive diagnosis and always includes a clear medical disclaimer.

Urgency Scoring: Assigns an urgency level (1-5) based on the symptoms, with color-coded feedback (Green, Yellow, Red).

Actionable Advice: Provides three clear sections for users:

Possible Conditions (with likelihood estimates).

Immediate Recommended Actions.

Key Questions to ask a Doctor.

Modern Frontend: A clean, responsive user interface built with HTML/CSS and interactive JavaScript.

Technology Stack
AI/LLM: Google Gemini API

Role: Provides the core intelligence for symptom analysis and structured data generation.

Backend Framework: Python (Flask)

Role: Serves the application, defines the API endpoint (/analyze), and handles the interaction with the Gemini API.

Frontend Logic: JavaScript

Role: Manages UI interactivity, fetches data from the Flask API, and dynamically renders the results.

User Interface: HTML & CSS

Role: Provides the structure and modern styling (using Poppins font and responsive design).
