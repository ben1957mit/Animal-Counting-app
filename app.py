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
defaults = {
    "correct_answer": None,
    "animal": None,
    "count": None,
    "show_result": False,
    "stars": 0,
    "progress": 0,
    "level": "Easy",
    "score": 0,
    "questions_answered": 0,
    "game_complete": False
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# -----------------------------
# Level Settings
# -----------------------------
level_ranges = {
    "Easy": (1, 5),
    "Medium": (3, 8),
    "Hard": (5, 12)
}

# -----------------------------
# Generate New Question
# -----------------------------
def new_question():
    min_n, max_n = level_ranges[st.session_state.level]
    st.session_state.animal = random.choice(list(animals.keys()))
    st.session_state.count = random.randint(min_n, max_n)
    st.session_state.correct_answer = st.session_state.count
    st.session_state.show_result = False

# First question
if st.session_state.animal is None:
    new_question()

# -----------------------------
# UI
# -----------------------------
st.title("🐯 Animal Counting Game")
st.write(f"### Level: **{st.session_state.level}**")
st.write(f"### ⭐ Stars: **{st.session_state.stars}**")
st.progress(st.session_state.progress)

# Display animals
st.write("### How many do you see?")
st.write((st.session_state.animal + " ") * st.session_state.count)

# Number buttons
st.write("### Choose the number:")
cols = st.columns(6)

# Generate number range based on level
min_n, max_n = level_ranges[st.session_state.level]
numbers = list(range(min_n, max_n + 1))

for idx, num in enumerate(numbers):
    if cols[idx % 6].button(str(num)):
        if num == st.session_state.correct_answer:
            st.session_state.show_result = "correct"
            st.session_state.stars += 1
            st.session_state.score += 10
            st.session_state.progress += 10
            play_sound("correct.mp3")
        else:
            st.session_state.show_result = "wrong"
            play_sound("wrong.mp3")

        st.session_state.questions_answered += 1

        # Level progression
        if st.session_state.progress >= 100:
            if st.session_state.level == "Easy":
                st.session_state.level = "Medium"
                st.session_state.progress = 0
            elif st.session_state.level == "Medium":
                st.session_state.level = "Hard"
                st.session_state.progress = 0
            else:
                st.session_state.game_complete = True

        # Delay before next question
        time.sleep(1)

        # New question unless game is complete
        if not st.session_state.game_complete:
            new_question()

# -----------------------------
# Result Message
# -----------------------------
if st.session_state.show_result == "correct":
    st.success("✅ Correct!")
elif st.session_state.show_result == "wrong":
    st.error("❌ Oops! Try again!")

# -----------------------------
# Game Complete Screen
# -----------------------------
if st.session_state.game_complete:
    st.balloons()
    st.success("🎉 YOU DID IT! You finished all levels!")
    st.write(f"🏆 Final Score: **{st.session_state.score}**")
    st.write(f"⭐ Total Stars: **{st.session_state.stars}**")

    if st.button("Play Again"):
        for key in defaults:
            st.session_state[key] = defaults[key]
        new_question()
