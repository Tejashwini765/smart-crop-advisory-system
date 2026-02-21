🌾 Smart Crop Advisory System
An AI-powered crop recommendation system that helps farmers choose the most suitable crops based on soil nutrients and environmental conditions.

🚀 Project Overview
The Smart Crop Advisory System combines:
🌱 Machine Learning (Random Forest Classifier)
🤖 Local Large Language Model (LLM via Ollama)
📊 Soil & Climate Analysis

🖼 Visual Crop Cards with Images
The system recommends the Top 3 most suitable crops based on:
Nitrogen (N)
Phosphorus (P)
Potassium (K)
Temperature
Humidity
pH Level
Rainfall
It also allows users to ask follow-up questions powered by a local AI model.

🧠 How It Works
1️⃣ Machine Learning Model
Trained using crop nutrient dataset
RandomForestClassifier
Uses probability ranking to determine top 3 crops

2️⃣ Local LLM (Ollama)
Model: phi3:mini (can upgrade to gemma3:4b)
Generates farmer-friendly explanations
Handles follow-up agricultural queries

3️⃣ Fully Offline Architecture
Local ML model (model.pkl)
Local LLM via Ollama
Local crop images
No external API required

🖼 UI Features
Clean modern dashboard
Crop cards with images
Emoji mapping for visual clarity
Top 3 ranked recommendations
Follow-up question support
Styled interface with CSS

🛠 Tech Stack
Python
Streamlit
Scikit-learn
NumPy
Ollama (Local LLM)
HTML/CSS styling

📁 Project Structure
smart-crop-advisory-system/
│
├── app_llm_local.py
├── model.pkl
├── images/
│   ├── mango.jpg
│   ├── papaya.jpg
│   ├── ...
│
└── .gitignore

▶ How to Run Locally
Install dependencies:
pip install streamlit scikit-learn numpy requests

Install Ollama:
https://ollama.com

Pull model:
ollama pull phi3:mini

Run the app:
streamlit run app_llm_local.py

📌 Future Improvements
Real-time weather API integration
Soil testing device integration
Market price prediction
Deployment on cloud
Mobile-friendly UI

👩‍💻 Author
Tejashwini Dasu
AI & Machine Learning Enthusiast
