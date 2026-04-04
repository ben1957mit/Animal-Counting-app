import streamlit as st
import random
import os
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
if "correct_answer" not in st.session_state:
    st.session_state.correct_answer = None

if "animal" not in st.session_state:
    st.session_state.animal = None

if "count" not in st.session_state:
    st.session_state.count = None

if "show_result" not in st.session_state:
    st.session_state.show_result = False

# -----------------------------
# Generate New Question
# -----------------------------
def new_question():
    st.session_state.animal = random.choice(list(animals.keys()))
    st.session_state.count = random.randint(1, 5)
    st.session_state.correct_answer = st.session_state.count
    st.session_state.show_result = False

# Generate first question if needed
if st.session_state.animal is None:
    new_question()

# -----------------------------
# UI
# -----------------------------
st.title("🐯 Animal Counting Game")
st.write("### Count the animals and choose the correct number!")

# Display animals
st.write("### How many do you see?")
st.write((st.session_state.animal + " ") * st.session_state.count)

# Number buttons
st.write("### Choose the number:")
cols = st.columns(5)

for i in range(1, 6):
    if cols[i-1].button(str(i)):
        if i == st.session_state.correct_answer:
            st.session_state.show_result = "correct"
            play_sound("correct.mp3")
        else:
            st.session_state.show_result = "wrong"
            play_sound("wrong.mp3")  new_question()
       
# -----------------------------
# Result Message
# -----------------------------
if st.session_state.show_result == "correct":
    st.success("🎉 Correct! Great job!")
elif st.session_state.show_result == "wrong":
    st.error("❌ Oops! Try again!")

# -----------------------------
# Next Question Button
# -----------------------------
if st.button("Next"):
   




