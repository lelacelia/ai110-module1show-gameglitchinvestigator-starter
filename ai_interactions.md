# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

Two tasks were given to the agent:

1. **UI Enhancement** — Add a player name input to the sidebar with a 💾 Save button and confirmation message. Personalize all win/loss/new-game messages throughout the app with the player's name.

2. **Feature Extension** — Add a Player's Statistics section in the sidebar that tracks and displays the current session's Games Played, Games Won, and Total Score. Stats update on every game end (win or loss) and reset to 0 on New Game.

**What did the agent do?**

*UI Enhancement (player name & personalized messages)* — [app.py:12-19](app.py#L12-L19), [app.py:96-97](app.py#L96-L97), [app.py:103-106](app.py#L103-L106), [app.py:142-145](app.py#L142-L145), [app.py:151-155](app.py#L151-L155):
1. Added `player_name` session state variable initialized to an empty string
2. Added name text input and 💾 Save button in sidebar; confirmation "✓ Registered as [name]" shown after saving
3. Personalized 5 game messages — New Game, first-time win, loss, already-won, already-lost — with player name; all fall back gracefully if no name is entered

*Feature Extension (Player's Statistics)* — [app.py:12-19](app.py#L12-L19), [app.py:47-53](app.py#L47-L53), [app.py:155-160](app.py#L155-L160), [app.py:167-169](app.py#L167-L169):
1. Added `games_played`, `games_won`, and `total_score` session state variables initialized to 0
2. Added 📊 Player's Statistics section in sidebar displaying all three stats (always visible)
3. On win: increments `games_played`, `games_won`, adds current score to `total_score`
4. On loss: increments `games_played` and adds current score to `total_score`
5. Score resets to 0 on New Game so `total_score` accumulates per-game scores correctly

**What did you have to verify or fix manually?**

- **Save button layout** — Iterated on button placement (side-by-side vs. below input) and size to match the Submit Guess button style
- **total_score not updating** — Debugged a KeyError caused by old-format session state missing `games_played` and `total_score` keys; fixed by adding `.setdefault()` in the load function
- **Score not resetting between games** — Score was accumulating across games, inflating total_score; fixed by adding `st.session_state.score = 0` on New Game
- **Attempts left showing 7 after New Game** — Leftover guess in text input triggered Bug #8's subtraction; fixed by incrementing `game_count` to force a fresh text input widget key on New Game ([app.py:114-115](app.py#L114-L115))
- **total_score not updating on loss** — Initially only updated on win; added loss update so all completed games contribute to total_score

---

## Test Generation (SF7)

> Document how you used AI to help generate or improve tests.
This is the prompt I gave AI: "next thing I need to do is to use AI and generate pytest cases to target the logic bugs I fixed on the app.py , some were carried over to logic_utils.py. what would you do?"

Because I outlined my bugs in great details in reflection.md, AI went ahead and generate multiple special logic tests for me.

I also went on and as "Are there any other tests you could think of for this game? Does not have to be about the bugs I spotted?". AI's response is Boundary & Edge Cases, Score Behavior, and Game Flow. I don't need the Score Behavior but I asked AI to suggested tests for Edge Cases and Game Flow.


| Edge Case | Prompt Used | AI-Suggested Test | Did It Pass? | Your Reasoning |
|-----------|-------------|-------------------|--------------|----------------|
| Float input rounding | "Generate pytest cases to target bugs in app.py and logic_utils.py" | `test_parse_guess_float_rounds_correctly` (42.7 → 43) | ✓ Yes | Verified Bug #3 fix—ensures floats round correctly, not floor. Critical for user fairness. |
| Perfect game score | Same prompt | `test_update_score_first_attempt_win_max_points` (100 points on attempt 1) | ✓ Yes | Verified Bug #7 fix—max score is 100, not 80. Prevents regression if code is refactored. |
| Hint direction | Same prompt | `test_check_guess_too_high_returns_go_lower` | ✓ Yes | Verified Bug #2 fix—hints now point correct direction. Essential for game playability. |
| Whitespace in input | "Are there other tests for edge cases?" | `test_parse_guess_leading_trailing_whitespace` | ✓ Yes | Ensures real-world user input (with spaces) parses correctly without errors. |
| Full game flow | Same prompt | `test_full_game_flow_multiple_guesses_then_win` | ✓ Yes | Integration test showing all components work together—multiple guesses, scoring, win condition. |

---

## Linting & Style (SF9)

> Document your use of AI for linting or code style improvements.

**Prompt used:**

```
<!-- Paste the prompt you gave the AI -->
```

**Linting output before:**

```
<!-- Paste relevant linter warnings/errors -->
```

**Changes applied:**

<!-- Describe what you changed based on the AI's suggestions -->

---

## Model Comparison (SF11)

> Compare two AI models on the same task.

**Task given to both models:**

<!-- Describe what you asked each model to do -->

| | Model A | Model B |
|-|---------|---------|
| **Model name** | | |
| **Response summary** | | |
| **More Pythonic?** | | |
| **Clearer explanation?** | | |

**Which did you prefer and why?**

<!-- Your conclusion -->
