import streamlit as st
import random
import os

# -----------------------------
# Sound Helper  ← PUT IT HERE
# -----------------------------
def play_sound(filename):
    path = f"assets/sounds/{filename}"
    audio_file = open(path, "rb").read()
    st.audio(audio_file, format="audio/mp3")

# -----------------------------
# Animal Data
# -----------------------------
animals = {
    ...
}
st.set_page_config(page_title="Animal Counting", page_icon="🐯", layout="centered")
# -----------------------------
# Animal Data
# -----------------------------
animals = {
    "🐶": "Dog",
    "🐱": "Cat",
    "🐰": "Rabbit",
    "🐵": "Monkey",
    "🦁": "Lion",
    "🐘": "Elephant",
    "🐢": "Turtle",
    "🐼": "Panda",
    "🦊": "Fox",
    "🐸": "Frog"
}

# -----------------------------
# Session State
# -----------------------------
if "correct_answer" not in st.session_state:
    st.session_state.correct_answer = None

if "stars" not in st.session_state:
    st.session_state.stars = 0

if "animal" not in st.session_state:
    st.session_state.animal = None

if "count" not in st.session_state:
    st.session_state.count = None

# -----------------------------
# Sound Helper
# -----------------------------
def play_sound(filename):
    path = os.path.join("assets", "sounds", filename)
    if os.path.exists(path):
        try:
            playsound(path)
        except:
            pass  # Streamlit Cloud may block audio, but local works fine

# -----------------------------
# New Question
# -----------------------------
def new_question():
    st.session_state.animal = random.choice(list(animals.keys()))
    st.session_state.count = random.randint(1, 10)
    st.session_state.correct_answer = st.session_state.count

# -----------------------------
# Reward Screen
# -----------------------------
def reward_screen():
    st.markdown("<h1 style='text-align:center;'>🎉 Great Job! 🎉</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center;'>You earned all 5 stars!</h2>", unsafe_allow_html=True)
    st.balloons()
    play_sound("cheer.mp3")

# -----------------------------
# UI
# -----------------------------
st.title("🐾 Animal Counting Game")
st.subheader("Tap the correct number!")

# Show stars
st.write("### ⭐ Rewards")
st.write("Stars earned: " + "⭐" * st.session_state.stars)

# If 5 stars → reward screen
if st.session_state.stars >= 5:
    reward_screen()
    if st.button("Play Again", use_container_width=True):
        st.session_state.stars = 0
        new_question()
    st.stop()

# Generate question if needed
if st.session_state.animal is None:
    new_question()

# Show animals
st.write("### Count the animals!")
st.markdown(
    f"<div style='font-size: 60px; text-align:center;'>{(st.session_state.animal + ' ') * st.session_state.count}</div>",
    unsafe_allow_html=True
)

# -----------------------------
# Big Toddler Buttons
# -----------------------------
st.write("### Choose the number:")

cols = st.columns(5)
for i in range(1, 11):
    col = cols[(i - 1) % 5]
    if col.button(str(i), use_container_width=True):
        if i == st.session_state.correct_answer:
            st.success("Great job! 🎉")
            play_sound("correct.mp3")
            st.session_state.stars += 1
        else:
            st.error("Try again!")
            play_sound("wrong.mp3")

        new_question()
        st.experimental_rerun()



