import streamlit as st
import random

# Set page config
st.set_page_config(page_title="Hangman Game", page_icon="🎭")

# Custom CSS for Full Black Background & Gold Text
st.markdown(
    """
    <style>
        body {
            background-color: black !important;
        }
        .stApp {
            background-color: black !important;
            color: gold !important;
        }
        h1, h2, h3, h4, h5, h6, p, label, div, span {
            color: gold !important;
        }
        .stTextInput input, .stSelectbox div, .stButton button, .stRadio div[role="radiogroup"] label {
            background-color: black !important;
            color: gold !important;
            border: 2px solid gold !important;
        }
        .stButton button {
            background-color: gold !important;
            color: black !important;
            font-weight: bold !important;
        }
        .stSidebar {
            background-color: black !important;
            color: gold !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar Navigation
st.sidebar.title("🔎 Navigate")
page = st.sidebar.radio("Go to:", ["Home", "Play Hangman"])

# ---- HOME PAGE ----
if page == "Home":
    st.title("🎭 Welcome to Hangman!")
    st.image("banner.webp", use_container_width=True)
    st.write(
        "💡 **How to Play:**\n"
        "- Guess the word by suggesting one letter at a time.\n"
        "- If your guess is correct, the letter is revealed.\n"
        "- If wrong, you lose an attempt.\n"
        "- Win by guessing the word before running out of attempts!"
    )
    st.write("🔹 Select 'Play Hangman' from the sidebar to start!")

# ---- GAME PAGE ----
else:
    st.title("🎮 Play Hangman")

    # Sidebar for Game Mode Selection
    game_mode = st.sidebar.radio("Select Mode:", ["Single Player", "Multiplayer"])

    # Hangman Word List with Hints
    words_with_hints = {
        "PYTHON": "A popular programming language",
        "STREAMLIT": "Python framework for data apps",
        "GITHUB": "A platform for code collaboration",
        "JUPYTER": "A notebook for data science",
        "ARTIFICIAL": "Related to AI and Machine Learning",
        "DEVELOPER": "A person who writes code",
        "COMPUTER": "An electronic machine"
    }

    def get_random_word():
        word, hint = random.choice(list(words_with_hints.items()))
        return word, hint

    # ---- Multiplayer Mode ----
    if game_mode == "Multiplayer":
        st.write("👥 **Multiplayer Mode**")
        word = st.text_input("Player 1: Enter a word for Player 2 to guess:", type="password").upper()
        if word:
            st.session_state["word"] = word
            st.success("✅ Word set! Player 2, start guessing!")

    # ---- Single Player Mode ----
    else:
        st.write("🤖 **Single Player Mode**")

        # ✅ **Fix: Initialize word & hint before using session state**
        if "word" not in st.session_state or "hint" not in st.session_state:
            st.session_state["word"], st.session_state["hint"] = get_random_word()

        st.write(f"💡 **Hint:** {st.session_state['hint']}")

    # Hangman Game Logic
    word = st.session_state["word"]
    hidden_word = ["_" for _ in word]
    attempts = 6
    guessed_letters = set()

    st.write(" ".join(hidden_word))
    guess = st.text_input("Guess a letter:", key="guess").upper()

    if guess:
        if guess in guessed_letters:
            st.warning("⚠ You've already guessed that letter!")
        elif guess in word:
            guessed_letters.add(guess)
            for idx, letter in enumerate(word):
                if letter == guess:
                    hidden_word[idx] = letter
        else:
            attempts -= 1
            st.error(f"❌ Wrong guess! {attempts} attempts left.")

    st.write(" ".join(hidden_word))

    if "_" not in hidden_word:
        st.success(f"🎉 You won! The word was: {word}")
    elif attempts == 0:
        st.error(f"💀 Game Over! The correct word was: {word}")
