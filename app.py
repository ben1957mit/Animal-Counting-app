


def reward_screen():
    st.markdown("<h1 style='text-align:center;'>🎉 Great Job! 🎉</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center;'>You earned all 5 stars!</h2>", unsafe_allow_html=True)
    st.balloons()

st.write("### ⭐ Rewards")
st.write("Stars earned: " + "⭐" * st.session_state.stars)

# If 5 stars → reward screen
if st.session_state.stars >= 5:
    reward_screen()
    if st.button("Play Again"):
        st.session_state.stars = 0
    st.stop()

# Generate new question
animal, count = new_question()

# Show animals
st.write("### Count the animals!")
st.write((animal + " ") * count)

# Number buttons
cols = st.columns(5)
for i in range(1, 11):
    col = cols[(i - 1) % 5]
    if col.button(str(i)):
        if i == st.session_state.correct_answer:
            st.success("Great job! 🎉")
            st.session_state.stars += 1
        else:
            st.error("Try again!")

        st.experimental_rerun()
