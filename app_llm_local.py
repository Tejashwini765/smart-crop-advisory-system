import streamlit as st
import pickle
import numpy as np
import requests
import os

# -------------------------------------------------
# Page Config
# -------------------------------------------------
st.set_page_config(
    page_title="Smart Crop Advisory",
    page_icon="🌾",
    layout="centered"
)

# -------------------------------------------------
# Custom UI Styling (UI ONLY - Logic untouched)
# -------------------------------------------------
st.markdown("""
<style>
    .main {
        background-color: #f4f8f5;
    }

    h1 {
        color: #1b5e20;
        text-align: center;
        font-weight: 700;
    }

    .subtitle {
        text-align: center;
        font-size: 16px;
        margin-bottom: 30px;
        color: #4e6e58;
    }

    .crop-card {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
        margin-bottom: 25px;
    }

    .crop-title {
        font-size: 22px;
        font-weight: 600;
        color: #2e7d32;
        margin-bottom: 10px;
    }

    .section-title {
        font-size: 20px;
        font-weight: 600;
        margin-top: 30px;
        color: #1b5e20;
    }

    .stButton>button {
        background-color: #2e7d32;
        color: white;
        border-radius: 10px;
        padding: 10px 20px;
        font-weight: 600;
        border: none;
    }

    .stButton>button:hover {
        background-color: #1b5e20;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# Load ML Model
# -------------------------------------------------
try:
    model = pickle.load(open("model.pkl", "rb"))
except:
    st.error("❌ model.pkl not found in project folder.")
    st.stop()

# -------------------------------------------------
# Local LLM (Ollama)
# -------------------------------------------------
def local_llm(prompt):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "phi3:mini",
                "prompt": prompt,
                "stream": False,
                "options": {
                    "num_predict": 150,
                    "temperature": 0.2
                }
            },
            timeout=60
        )
        return response.json()["response"]
    except:
        return "⚠ LLM not responding. Make sure Ollama is running."

# -------------------------------------------------
# Emoji Mapping
# -------------------------------------------------
crop_icons = {
    "mango": "🥭",
    "papaya": "🍈",
    "banana": "🍌",
    "apple": "🍎",
    "orange": "🍊",
    "grapes": "🍇",
    "watermelon": "🍉",
    "muskmelon": "🍈",
    "pomegranate": "🍎",
    "coconut": "🥥",
    "maize": "🌽",
    "rice": "🌾",
    "pigeonpeas": "🫘",
    "lentil": "🫘",
    "mungbean": "🫘",
    "blackgram": "🫘",
    "chickpea": "🧆",
    "mothbeans": "🫘",
    "kidneybeans": "🫘",
    "jute": "🧵",
    "cotton": "🧶",
    "coffee": "☕"
}

# -------------------------------------------------
# Local Image Loader
# -------------------------------------------------
def get_crop_image(crop):
    path = f"images/{crop.lower()}.jpg"
    return path if os.path.exists(path) else None

# -------------------------------------------------
# Header
# -------------------------------------------------
st.markdown("<h1>🌾 Smart Crop Advisory System</h1>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>AI-Powered Sustainable Crop Recommendation</div>", unsafe_allow_html=True)

st.markdown("---")

# -------------------------------------------------
# Input Section
# -------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    N = st.number_input("Nitrogen (N)", 0, 200, 50)
    P = st.number_input("Phosphorus (P)", 0, 200, 50)
    K = st.number_input("Potassium (K)", 0, 200, 50)
    ph = st.number_input("pH Level", 0.0, 14.0, 6.5)

with col2:
    temperature = st.number_input("Temperature (°C)", 0.0, 50.0, 25.0)
    humidity = st.number_input("Humidity (%)", 0.0, 100.0, 60.0)
    rainfall = st.number_input("Rainfall (mm)", 0.0, 500.0, 100.0)

# -------------------------------------------------
# Predict Button
# -------------------------------------------------
if st.button("🌿 Analyze Suitable Crops"):

    input_data = np.array([[N, P, K, temperature, humidity, ph, rainfall]])

    probabilities = model.predict_proba(input_data)[0]
    crop_labels = model.classes_

    top_indices = np.argsort(probabilities)[::-1][:3]

    st.session_state.top_indices = top_indices
    st.session_state.inputs = (N, P, K, temperature, humidity, ph, rainfall)

# -------------------------------------------------
# Display Results
# -------------------------------------------------
if "top_indices" in st.session_state:

    N, P, K, temperature, humidity, ph, rainfall = st.session_state.inputs
    input_data = np.array([[N, P, K, temperature, humidity, ph, rainfall]])
    probabilities = model.predict_proba(input_data)[0]
    crop_labels = model.classes_

    st.markdown("## 🏆 Top 3 Recommended Crops")

    for rank, idx in enumerate(st.session_state.top_indices, start=1):

        crop = crop_labels[idx]
        icon = crop_icons.get(crop.lower(), "🌱")
        image_path = get_crop_image(crop)

        st.markdown("<div class='crop-card'>", unsafe_allow_html=True)
        st.markdown(f"<div class='crop-title'>{rank}. {icon} {crop.upper()}</div>", unsafe_allow_html=True)

        if image_path:
            st.image(image_path, width=220)

        prompt = f"""
You are an agricultural advisor.

Explain why {crop} is suitable.

Rules:
- Give EXACTLY 2 bullet points.
- Each bullet must be one complete sentence.
- Do NOT explain what you are doing.
- Do NOT add extra commentary.
- Do NOT mention instructions.
- Keep it simple and farmer-friendly.
- No technical words.

Start directly with bullet points.
"""

        with st.spinner("Generating explanation..."):
            explanation = local_llm(prompt)

        st.write(explanation)

        st.markdown("</div>", unsafe_allow_html=True)

    # -------------------------------------------------
    # Follow-up Section
    # -------------------------------------------------
    st.markdown("<div class='section-title'>💬 Ask About These Crops</div>", unsafe_allow_html=True)

    follow_up = st.text_input("Ask your question:")

    if st.button("Ask AI") and follow_up:

        follow_prompt = f"""
You are an agricultural advisor.

Soil conditions:
N={N}, P={P}, K={K},
Temperature={temperature},
Humidity={humidity},
pH={ph},
Rainfall={rainfall}

Top recommended crops:
{[crop_labels[i] for i in st.session_state.top_indices]}

The user is asking about one of these crops.

User question:
{follow_up}

IMPORTANT RULES:
- If the user mentions a specific crop, ONLY talk about that crop.
- Do NOT suggest different crops unless the user clearly asks for alternatives.
- Give EXACTLY 2 short bullet points.
- Each bullet must be one complete sentence.
- No extra commentary.
- No explanation about what you are doing.
"""

        with st.spinner("Thinking..."):
            answer = local_llm(follow_prompt)

        st.markdown("### 🤖 AI Response")
        st.write(answer)