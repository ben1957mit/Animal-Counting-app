import streamlit as st
import random
import os
import time

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(page_title="Animal Counting", page_icon="🐯", layout="centered")

# -----------------------------
# Sound Helper
# -----------------------------
def play_sound(filename):
    path = f"assets/sounds/{filename}"
    if os.path.exists(path):
        with open(path, "rb") as f:
            audio_file = f.read()
        st.audio(audio_file, format="audio/mp3")

# -----------------------------
# Animal Data
# -----------------------------
animals = ["🐶", "🐱", "🐰", "🐵", "🦁", "🐘", "🐢", "🐼", "🦊", "🐸"]

# -----------------------------
# Session State Defaults
# -----------------------------
defaults = {
    "correct_answer": None,
    "animal": None,
    "count": None,
    "show_result": False,
    "stars": 0,
    "progress": 0,
    "score": 0,
    "game_complete": False
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# -----------------------------
# Generate New Question
# -----------------------------
def new_question():
    st.session_state.animal = random.choice(animals)
    st.session_state.count = random.randint(1, 5)
    st.session_state.correct_answer = st.session_state.count
    st.session_state.show_result = False

# First question
if st.session_state.animal is None:
    new_question()

# -----------------------------
# UI
# -----------------------------
st.title("🐯 Animal Counting Game")
st.write("### Count the animals and tap the right number!")

# Stars + Progress
st.write(f"### ⭐ Stars: **{st.session_state.stars}**")
st.progress(st.session_state.progress)

# Display animals
st.write("### How many do you see?")
st.write((st.session_state.animal + " ") * st.session_state.count)

# -----------------------------
# Big Toddler-Friendly Buttons
# -----------------------------
st.write("### Tap the number:")

cols = st.columns(5)

for i in range(1, 6):
    if cols[i-1].button(str(i), use_container_width=True):
        if i == st.session_state.correct_answer:
            st.session_state.show_result = "correct"
            st.session_state.stars += 1
            st.session_state.score += 10
            st.session_state.progress += 20
            play_sound("correct.mp3")
        else:
            st.session_state.show_result = "wrong"
            play_sound("wrong.mp3")

        # Check for game completion
        if st.session_state.progress >= 100:
            st.session_state.game_complete = True

        # 1-second delay
        time.sleep(1)

        # New question unless game is done
        if not st.session_state.game_complete:
            new_question()

# -----------------------------
# Result Message
# -----------------------------
if st.session_state.show_result == "correct":
    st.success("🎉 Correct!")
elif st.session_state.show_result == "wrong":
    st.error("❌ Try again!")

# -----------------------------
# Game Complete Screen
# -----------------------------
if st.session_state.game_complete:
    st.balloons()
    st.success("🎉 YOU DID IT!")
    st.write(f"🏆 Final Score: **{st.session_state.score}**")
    st.write(f"⭐ Total Stars: **{st.session_state.stars}**")

    if st.button("Play Again"):
        for key in defaults:
            st.session_state[key] = defaults[key]
        new_question()
