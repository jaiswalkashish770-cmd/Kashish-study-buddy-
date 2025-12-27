import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Study Partner", layout="centered")

# 🌸 PINK THEME (FORCE APPLY)
st.markdown("""
<style>
.stApp {
    background-color: #fff0f6;
}

h1, h2, h3 {
    color: #c2185b;
}

.stButton > button {
    background-color: #ff69b4;
    color: white;
    border-radius: 12px;
    padding: 10px 20px;
    border: none;
    font-weight: bold;
}

.stButton > button:hover {
    background-color: #ff85c1;
}
</style>
""", unsafe_allow_html=True)

# Title
st.title("🌸 Study Partner")

st.write("Focus on your goals. I'll track the rest 💗")

# Simple demo content
task = st.text_input("Task name")
if st.button("Add Task"):
    st.success("Task added 💖")
