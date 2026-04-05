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
# Session State Defaults
# -----------------------------
defaults = {
    "mode": "Counting",            # Counting | Timed | ChooseAnimal | Parent
    "correct_answer": None,
    "animal": None,
    "count": None,
    "show_result": False,
    "stars": 0,
    "progress": 0,
    "score": 0,
    "level": "Easy",
    "game_complete": False,
    "timer_start": None,
    "chosen_animal": None
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
    if st.session_state.mode == "ChooseAnimal" and st.session_state.chosen_animal:
        st.session_state.animal = st.session_state.chosen_animal
    else:
        st.session_state.animal = random.choice(list(animals.keys()))

    min_n, max_n = level_ranges[st.session_state.level]
    st.session_state.count = random.randint(min_n, max_n)
    st.session_state.correct_answer = st.session_state.count
    st.session_state.show_result = False

# First question
if st.session_state.animal is None:
    new_question()

# -----------------------------
# Sidebar Navigation
# -----------------------------
with st.sidebar:
    st.header("🎮 Game Modes")
    if st.button("Counting Mode"):
        st.session_state.mode = "Counting"
        st.experimental_rerun()

    if st.button("Timed Challenge"):
        st.session_state.mode = "Timed"
        st.session_state.timer_start = time.time()
        st.experimental_rerun()

    if st.button("Choose Animal"):
        st.session_state.mode = "ChooseAnimal"
        st.experimental_rerun()

    if st.button("Parent Dashboard"):
        st.session_state.mode = "Parent"
        st.experimental_rerun()

# -----------------------------
# Parent Dashboard
# -----------------------------
if st.session_state.mode == "Parent":
    st.title("👨‍👩‍👧 Parent Dashboard")
    st.write("### Game Stats")
    st.write(f"⭐ Stars: {st.session_state.stars}")
    st.write(f"🏆 Score: {st.session_state.score}")
    st.write(f"🎚️ Level: {st.session_state.level}")

    if st.button("Reset Game"):
        for key in defaults:
            st.session_state[key] = defaults[key]
        new_question()
        st.experimental_rerun()

    st.stop()

# -----------------------------
# Choose Animal Mode
# -----------------------------
if st.session_state.mode == "ChooseAnimal":
    st.title("🐾 Choose Your Animal")
    cols = st.columns(5)

    for idx, emoji in enumerate(animals.keys()):
        if cols[idx % 5].button(emoji, use_container_width=True):
            st.session_state.chosen_animal = emoji
            st.session_state.mode = "Counting"
            new_question()
            st.experimental_rerun()

    st.stop()

# -----------------------------
# Timed Challenge Mode
# -----------------------------
if st.session_state.mode == "Timed":
    st.title("⏱️ Timed Challenge")
    elapsed = int(time.time() - st.session_state.timer_start)
    st.write(f"### Time: **{elapsed} seconds**")

# -----------------------------
# Main Counting Game
# -----------------------------
st.title("🐯 Animal Counting Game")
st.write(f"### Level: **{st.session_state.level}**")
st.write(f"### ⭐ Stars: **{st.session_state.stars}**")
st.progress(st.session_state.progress / 100)

# Display animals
st.write("### How many do you see?")
st.write((st.session_state.animal + " ") * st.session_state.count)

# -----------------------------
# Big Toddler-Friendly Buttons
# -----------------------------
st.write("### Tap the number:")

cols = st.columns(10)

for i in range(1, 11):
    if cols[i-1].button(str(i), use_container_width=True):
        if i == st.session_state.correct_answer:
            st.session_state.show_result = "correct"
            st.session_state.stars += 1
            st.session_state.score += 10
            st.session_state.progress += 10
            play_sound("correct.mp3")
        else:
            st.session_state.show_result = "wrong"
            play_sound("wrong.mp3")

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

        # 1-second delay
        time.sleep(1)

        if st.session_state.game_complete:
            st.experimental_rerun()
        else:
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
    st.markdown("<h1 style='text-align:center; color:#4CAF50;'>🎉 YOU DID IT! 🎉</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center;'>Amazing job!</h2>", unsafe_allow_html=True)

    st.write(f"🏆 **Final Score:** {st.session_state.score}")
    st.write(f"⭐ **Total Stars:** {st.session_state.stars}")

    if st.button("Play Again"):
        for key in defaults:
            st.session_state[key] = defaults[key]
        new_question()

    st.stop()
