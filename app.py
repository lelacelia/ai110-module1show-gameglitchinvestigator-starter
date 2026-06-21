import random
import streamlit as st
from logic_utils import get_range_for_difficulty, parse_guess, check_guess, update_score

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)
# FIX: Bug #1 Attempts left are 1 lower than supposed to be at the start
# i.e. Attempts left at the start is 7 instead of 8 at the Normal level.
if "attempts" not in st.session_state:
    st.session_state.attempts = 0 # <- fix bug 1 from 1 to 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

st.subheader("Make a guess")
#FIX: Bug #4 guess range is incorrectly displayed as 1-100 for all difficulty levels.
#FIX: Bug #8 attempts left count in Info lags by 1 - check if guess is pending submission.
attempts_left = attempt_limit - st.session_state.attempts
if st.session_state.get(f"guess_input_{difficulty}"):  # If there's a guess in the input, it's about to be submitted
    attempts_left -= 1

st.info(
    f"Guess a number between {low} and {high}. " # <--- change 1 to low and 100 to high, as specifed above low, high = get_range_for_difficulty(difficulty)
    f"Attempts left: {attempts_left}"
)

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}"
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

if new_game:
    st.session_state.attempts = 0
    #FIX: Bug #5 New Game button does not restart the game because status is not reset to "playing".
    st.session_state.status = "playing" # <--- reset status so the game doesn't immediately show win/loss message
    #FIX: Bug #9 history is retained and carried over after New Game is selected.
    st.session_state.history = [] # <--- clear history for new game
    #FIX: Bug #4 guess range is incorrectly displayed as 1-100 for all difficulty levels.
    st.session_state.secret = random.randint(low, high) # <--- change 1 to low and 100 to high, as specifed above low, high = get_range_for_difficulty(difficulty)

    st.success("New game started.")
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

if submit:
    st.session_state.attempts += 1

    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        st.session_state.history.append(raw_guess)
        st.error(err)
    else:
        st.session_state.history.append(guess_int)

        #FIX: Bug #6 secret number is converted to a string on even attempts causing type mismatch.
        # BUGGY CODE (commented out):
        # if st.session_state.attempts % 2 == 0:
        #     secret = str(st.session_state.secret)
        # else:
        #     secret = st.session_state.secret
        secret = st.session_state.secret # <--- always keep secret as integer

        outcome, message = check_guess(guess_int, secret)

        if show_hint:
            st.warning(message)

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
