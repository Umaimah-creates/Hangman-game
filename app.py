import streamlit as st
import random

# --- Custom Dark Theme CSS ---
st.markdown(
    """
    <style>
        body {
            background-color: black;
            color: gold;
        }
        .stApp {
            background-color: black;
            color: gold;
        }
        .stTextInput>div>div>input {
            background-color: black !important;
            color: gold !important;
            border: 1px solid gold !important;
        }
        .stButton>button {
            background-color: gold !important;
            color: black !important;
            font-weight: bold;
            border-radius: 5px;
        }
        .stSidebar {
            background-color: black !important;
        }
        .stSidebar .stRadio label {
            color: gold !important;
        }
        .stSidebar .stTitle, .stSidebar .stHeader {
            color: gold !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Sidebar Navigation ---
st.sidebar.title("🔎 Navigate")
page = st.sidebar.radio("Go to:", ["Home", "Play Hangman"])

# --- Home Page ---
if page == "Home":
    st.title("🎮 Hangman Game")
    st.image("banner.png", use_container_width=True)
    st.write("Welcome to the Hangman game! Select 'Play Hangman' from the sidebar to start playing.")

# --- Play Hangman Page ---
elif page == "Play Hangman":
    st.title("🎮 Play Hangman")

    # Initialize session state variables
    if "word" not in st.session_state:
        words_with_hints = {
            "python": "A popular programming language",
            "streamlit": "A framework for data apps",
            "github": "A platform for code collaboration",
            "hangman": "The name of this game",
            "laptop": "A portable computer"
        }
        st.session_state.word, st.session_state.hint = random.choice(list(words_with_hints.items()))
        st.session_state.display_word = "_" * len(st.session_state.word)
        st.session_state.attempts = 6
        st.session_state.guessed_letters = set()
        st.session_state.message = ""

    st.write(f"💡 **Hint:** {st.session_state.hint}")

    # Display word progress
    st.write(" ".join(st.session_state.display_word))

    # Letter input
    guess = st.text_input("Guess a letter:", key="guess_input", max_chars=1).lower()

    if st.button("Submit Guess"):
        if not guess or not guess.isalpha():
            st.session_state.message = "⚠️ Please enter a valid letter!"
        elif guess in st.session_state.guessed_letters:
            st.session_state.message = "⚠️ You already guessed this letter!"
        elif guess in st.session_state.word:
            st.session_state.guessed_letters.add(guess)
            updated_display = "".join([
                letter if letter in st.session_state.guessed_letters else "_"
                for letter in st.session_state.word
            ])
            st.session_state.display_word = updated_display
            st.session_state.message = "✅ Correct Guess!"
        else:
            st.session_state.guessed_letters.add(guess)
            st.session_state.attempts -= 1
            st.session_state.message = "❌ Wrong Guess!"

        if "_" not in st.session_state.display_word:
            st.success("🎉 You Won!")
            st.session_state.word = ""

        elif st.session_state.attempts == 0:
            st.error(f"❌ Game Over! The word was: {st.session_state.word}")
            st.session_state.word = ""

    # Show message and remaining attempts
    st.write(f"📝 {st.session_state.message}")
    st.write(f"❤️ Attempts Left: {st.session_state.attempts}")
