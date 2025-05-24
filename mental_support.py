import streamlit as st
system_prompt = "You are a kind and supportive mental health chatbot. Give empathetic, safe advice for emotional support."

st.session_state['conversation_history'] = [
    {"role": "system", "content": system_prompt}
] + st.session_state['conversation_history']


import ollama
import base64
from voice_sentiment import record_voice, analyze_sentiment

# -------------------- Page Setup --------------------
st.set_page_config(page_title="Mental Health Chatbot")

def get_base64(background):
    with open(background, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

bin_str = get_base64("background.jpg")

st.markdown(f"""
    <style>
        [data-testid="stAppViewContainer"] > .main {{
            background-image: url("data:image/png;base64,{bin_str}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
    </style>
""", unsafe_allow_html=True)

# -------------------- Helpline Info --------------------
helplines = {
    "india": [
        "📞 iCall: +91 9152987821",
        "📞 AASRA: +91 9820466726",
        "📞 24x7 Helpline: 1800-599-0019"
    ],
    "usa": [
        "📞 988 Suicide & Crisis Lifeline: Call or text 988"
    ]
}

# -------------------- Risk Detection --------------------
suicide_phrases = [
    "kill myself", "want to die", "can't go on", "suicide",
    "end my life", "i'm done", "take my life", "no reason to live"
]
violence_phrases = [
    "kill someone", "kill somebody", "hurt others", "murder someone",
    "i want to kill", "plan to kill", "harm someone", "attack someone"
]

def detect_risk(message):
    text = message.lower()
    if any(p in text for p in suicide_phrases):
        return "suicide"
    if any(p in text for p in violence_phrases):
        return "violence"
    return None

# -------------------- Session State --------------------
if 'conversation_history' not in st.session_state:
    st.session_state['conversation_history'] = []

# -------------------- Generate Responses --------------------
def generate_response(user_input):
    risk = detect_risk(user_input)
    if risk == "suicide":
        support_msg = (
            "I'm really sorry you're feeling this way. You're not alone — there are people who care about you.\n\n"
            "Please consider talking to a mental health professional, a friend, or a family member. Your well-being matters.\n\n"
            "**If you're in India, here are some helplines you can reach out to:**\n"
            + "\n".join(helplines["india"]) +
            "\n\nYou can also let me know how you're feeling — I'm here to listen."
        )
        st.session_state['conversation_history'].append({"role": "assistant", "content": support_msg})
        return support_msg

    st.session_state['conversation_history'].append({"role": "user", "content": user_input})
    response = ollama.chat(model="tinyllama", messages=st.session_state['conversation_history'])
    ai_response = response['message']['content']
    st.session_state['conversation_history'].append({"role": "assistant", "content": ai_response})
    return ai_response

def generate_meditation_guide():
    prompt = "Provide a short guided meditation for relaxation."
    response = ollama.chat(model="tinyllama", messages=[{"role": "user", "content": prompt}])
    return response['message']['content']

def generate_affirmation():
    prompt = "Provide a positive affirmation to encourage someone who is feeling stressed or overwhelmed."
    response = ollama.chat(model="tinyllama", messages=[{"role": "user", "content": prompt}])
    return response['message']['content']

# -------------------- Interface --------------------
st.title("🧠 Mental Health Support Agent")

# Show conversation history
for msg in st.session_state['conversation_history']:
    role = "You" if msg['role'] == "user" else "AI"
    st.markdown(f"**{role}:** {msg['content']}")

# --- Input Section (Text or Voice) ---
col1, col2 = st.columns([3, 1])

with col1:
    user_message = st.text_input("How can I help you today?")

with col2:
    speak_clicked = st.button("🎤 Speak")

# --- Handle Voice Input ---
if speak_clicked:
    voice_message = record_voice()
    st.markdown(f"**You (via voice):** {voice_message}")

    mood, score = analyze_sentiment(voice_message)
    st.markdown(f"**Detected mood:** {mood} (polarity: {score:.2f})")

    with st.spinner("Thinking..."):
        ai_response = generate_response(voice_message)
        st.markdown(f"**AI:** {ai_response}")

# --- Handle Typed Input ---
elif user_message:
    mood, score = analyze_sentiment(user_message)
    st.markdown(f"**Detected mood:** {mood} (polarity: {score:.2f})")

    with st.spinner("Thinking..."):
        ai_response = generate_response(user_message)
        st.markdown(f"**AI:** {ai_response}")

# --- Optional Tools ---
col3, col4 = st.columns(2)

with col3:
    if st.button("🌤️ Positive Affirmation"):
        affirmation = generate_affirmation()
        st.markdown(f"**Affirmation:** {affirmation}")

with col4:
    if st.button("🧘‍♂️ Guided Meditation"):
        meditation_guide = generate_meditation_guide()
        st.markdown(f"**Guided Meditation:** {meditation_guide}")