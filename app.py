import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

# Load Gemini API key from environment variable
GEMINI_API_KEY = os.getenv("AIzaSyD8xk5AOzwgj3hh4ViyTElBadqNFqkMrnQ")  # Set this in Railway or .env file

if not GEMINI_API_KEY:
    raise ValueError("Gemini API key is missing. Please set the GEMINI_API_KEY environment variable.")

app = Flask(__name__)
CORS(app)  # Allow frontend access

# Function to get disease prediction from Gemini API
def get_disease_prediction(symptoms):
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"

    prompt = f"Identify the possible disease based on these symptoms: {symptoms}. Provide only the disease name and a list of precautions as points separated in lines [[[[(Please don't show stars separated(*) again and again in result)]]]] ."

    headers = {"Content-Type": "application/json"}
    payload = {"contents": [{"parts": [{"text": prompt}]}]}

    response = requests.post(url, json=payload, headers=headers)
    data = response.json()

    try:
        response_text = data["candidates"][0]["content"]["parts"][0]["text"]
        parts = response_text.split("\n")
        disease = parts[0].strip()  # Disease name on the first line
        precautions = "\n".join(parts[1:]).strip()  # Remaining lines are precautions
        return disease, precautions
    except:
        return "Unknown", "Error extracting data from API"

# Function to get the doctor type based on the disease
def get_doctor_type(disease):
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"
    
    prompt = f"What type of doctor specializes in treating {disease}? Provide only the doctor type, such as 'Cardiologist', 'Dermatologist', etc."

    headers = {"Content-Type": "application/json"}
    payload = {"contents": [{"parts": [{"text": prompt}]}]}

    response = requests.post(url, json=payload, headers=headers)
    data = response.json()

    try:
        doctor_type = data["candidates"][0]["content"]["parts"][0]["text"].strip()
        return doctor_type
    except:
        return "General Physician"  # Default if Gemini fails

# Flask API Route for disease prediction
@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    symptoms = data.get("symptoms", "")

    if not symptoms:
        return jsonify({"error": "No symptoms provided"}), 400

    disease, precautions = get_disease_prediction(symptoms)
    doctor_type = get_doctor_type(disease)

    return jsonify({
        "prediction": disease,
        "precautions": precautions,
        "doctor_type": doctor_type
    })

if __name__ == "__main__":
    app.run(debug=False)  # Set debug=False for production deployment
