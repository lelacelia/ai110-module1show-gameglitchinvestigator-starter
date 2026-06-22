# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [ ] Describe the game's purpose.
The game is about guessing what the secret number is and earning scores. The fewer attempts one needs to use to guess the secret correctly, the higher the score. If guessing correctly on the first try, player will get 100 score. If guessing correctly on last attempt alloted, player will get 10. If fail completely, scores can be negative. Scores are substracted or added depending on how many attempts are used and the direction of the guesses (higher or lower than the secret). 

- [ ] Detail which bugs you found.
I detailed the 9 bugs I found with the helped of AI on the reflection.md file

- [ ] Explain what fixes you applied.
This summary was put together with the help of AI agent.

### Detailed Bug Fixes with Code References

> **Note:** Code locations and references below refer to the original broken version of the files. The current version has been refactored and optimized, so line numbers and file structures may differ from what is listed in this table.

| Bug | Issue | Code Fix | Location |
|-----|-------|----------|----------|
| **Bug #1** | Attempts left showed 7 instead of 8 at Normal level | Changed `st.session_state.attempts = 1` to `st.session_state.attempts = 0` so the counter starts at 0 instead of 1 | [app.py:35](app.py#L35) |
| **Bug #2** | Hints were backwards ("Go higher" when should be "Go lower") | Swapped the hint messages: when `guess > secret`, return "Go LOWER!" instead of "Go HIGHER!" | [logic_utils.py:64-66](logic_utils.py#L64-L66) |
| **Bug #3** | Decimal numbers were floored instead of rounded (42.7 → 42 instead of 43) | Changed `int(float(raw))` to `round(float(raw))` to use proper rounding | [logic_utils.py:29](logic_utils.py#L29) |
| **Bug #4** | Game announcement didn't change with difficulty level; range always 1-100 | Updated announcement text to use dynamic `low` and `high` variables instead of hardcoded 1-100. Also updated secret generation from `random.randint(1, 100)` to `random.randint(low, high)` | [app.py:54](app.py#L54), [app.py:85](app.py#L85) |
| **Bug #5** | New Game button didn't restart the game | Added two missing reset statements: `st.session_state.status = "playing"` and `st.session_state.history = []` when New Game is clicked | [app.py:81](app.py#L81), [app.py:83](app.py#L83) |
| **Bug #6** | Secret number was a string on even attempts, integer on odd attempts | Removed buggy conditional code that converted secret to string on even attempts. Now always use: `secret = st.session_state.secret` (always an integer) | [app.py:114](app.py#L114) (lines 110-113 commented out) |
| **Bug #7** | Maximum score was 80 instead of 100 | Changed scoring formula from `100 - 10 * (attempt_number + 1)` to `100 - 10 * (attempt_number - 1)`, allowing 100 points for a first-attempt win | [logic_utils.py:74](logic_utils.py#L74) |
| **Bug #8** | Attempts left count lagged by 1 in the info display | Added a check for pending guess input: if user has typed something but hasn't submitted, decrement `attempts_left` by 1 to show accurate count before submission | [app.py:49-51](app.py#L49-L51) |
| **Bug #9** | History persisted in Developer Debug Info after New Game | Added `st.session_state.history = []` to the New Game button handler to clear the history list | [app.py:83](app.py#L83) |

#### Key Logic Changes Summary

**In [logic_utils.py](logic_utils.py):**
- **parse_guess()** [line 29]: Uses `round()` instead of `int()` for float handling
- **check_guess()** [lines 64-66]: Fixed reversed hint logic 
- **update_score()** [line 74]: Corrected formula to allow max 100 points

**In [app.py](app.py):**
- **Session State Init** [line 35]: Attempts counter starts at 0
- **Display Logic** [lines 49-51]: Dynamic attempts_left calculation accounting for pending input
- **Game Reset** [lines 81, 83]: Reset status, history, and secret when New Game is clicked
- **Range & Secret** [lines 54, 85]: Use `low` and `high` from `get_range_for_difficulty()` instead of hardcoded 1-100

## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:

1. Select Difficulty level using the dropdown menu. Normal is the defaulted stage. Show hint box is checked by default.
2. Enter 50 in the Enter your guess: textbox and click Submit
3. Game returned "📉 Go HIGHER!" // Game info: "Guess a number between 1 and 100. Attempts left: 7"// Developer Bug Info shows correct outputs, including attempts: 0, score: 0, difficulty: normal, history: []
4. Enter 75 in the Enter your guess: textbox and click Submit
5. Game returned "📈 Go LOWER!" // "Guess a number between 1 and 100. Attempts left: 6" // Developer Bug Info shows correct outputs, including attempts: 1, score: -5, difficulty: normal, history: [0:50,]
6. Enter 69 in the Enter your guess textbox and click Sumbit.
7. Game ends after the correct guess, score is correct at 85. 
8. Click New Game, history list in the Developer Bug Info is empty, Attempts left and Attempts count are reset, Score is retained.
9. There are enhanced UI now that game announcements are accompanied with player's name - if player chooses to enter their name in the input box.
10. Also, there is a Player's Statistics that count number of games played, games won, and total score each game session (cleared when the game is refreshed)

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

```
# Paste your pytest output here, e.g.:
# pytest tests/
# ============================= 36 passed in 0.09s ==============================


To see full pytest test output, view the test_result.txt
I included edge tests as well in the test_result.txt file. 28 tests before new feature extension and UI enhancement are added. After further extensions with AI supports, 8 more tests were ran.


```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
1. **UI Enhancement** — Add a player name input to the sidebar with a 💾 Save button and confirmation message. Personalize all win/loss/new-game messages throughout the app with the player's name.

2. **Feature Extension** — Add a Player's Statistics section in the sidebar that tracks and displays the current session's Games Played, Games Won, and Total Score. Stats update on every game end (win or loss) and reset to 0 on New Game.

![UI and Feature Enhancements](UI%20and%20Feature%20Enhancements.png)
