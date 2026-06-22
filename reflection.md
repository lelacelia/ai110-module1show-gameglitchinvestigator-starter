# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
The Game's Difficulty level is Normal, Range: 1 to 100, Attempts allowed: 8. In the middle of the screen, there is a notice "Guess a number between 1 and 100. Attempts left: 7". Show hint is enabled. There is a Developer Debug Info showing the game details including the Secret, Attempts, Score, Difficulty, and History.

- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").
  
  **Bug #1:** Attempts left at the start is 7 at the Normal level, however, this should be 8.
  
  **Bug #2:** The hints are backwards - for example, the correct answer is 65, when user enters 80, the hint is "Go higher", which is wrong direction.
  
  **Bug #3:** Decimal numbers always get rounded down. The system rounded down the number first, recorded the rounded down number in the History list and compared that rounded down number with the secret.
  
  **Bug #4:** The game announcement is always "Guess a number between 1 and 100" regardless of what difficulty level is selected. Also, the secret's range is fixed at 1-100

  **Bug #5:"** New Game button does not restart the game
  
  **Bug #6:** The secret number is converted to a string on even-numbered attempts, but in odd attempts, it remains an integer. On odd attempts the game works correctly, but on even attempts it yields incorrect results.
  
  **Bug #7:** Maximum score is 80, but it should be 100.
  
  **Bug #8:** After bug #1 is fixed, count of attempts left still lags by 1 in the info section, even though it is still correctly recorded in the system.

  **Bug 9:** In the Developer Debug Info, history is retained and carried over after New Game is selected

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| 31 | Go HIGHER! | Go LOWER! | none |
| None | Attempts left: 8 | Attempts left: 7 | none |
| Easy | Guess a number between 1 and 20 | Guess a number between 1 and 100 | none |
| 49.5 | Go LOWER! (secret is 49) | Correct! | none |
| 81 | Win, Score = 100 | Win, Score = 80 | none |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
Claude Haiku 4.5 . AI helped me fixed the bugs I pointed out (bug 1, 2, 3, and 5) AI pointed out the remaining bugs for me. AI helped me note the edits and write comments for git commits.

- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
I asked Claude Haiku about Bug #1 (attempts left showing 7 instead of 8). Claude explained the problem and pointed me to line 96 of app.py where the issue was. I implemented the fix Claude suggested and refreshed the page to test. After the fix, I verified that at Normal level, Attempts left shows 8; at Easy level, it shows 6; and at Hard level, it shows 5 - all correct.

- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
I asked AI to fix bug #8 for me, which is about the incorrect attempt left displayed in the game info. It gave me some suggestions but still too complicated, so I asked for a simpler solution. It gave me this suggestion:

    Just use the history length instead of the attempts counter:

    st.info(
        f"Guess a number between {low} and {high}. "
        f"Attempts left: {attempt_limit - len(st.session_state.history)}"
    )
    Since the history is updated with every guess submission, it's always accurate and doesn't have the lag issue. No state tracking needed, no moving code around.

I was not sure if it is gonna work, but I still accepted this edit. I ran the game again, test played it, attempt left still remained 8 after the first wrong guess. I asked AI again, and it admitted that using history length does not solve this issue completely because history is also only updated after the display runs. 

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
I manually test-played three to four times. I also asked AI to build test cases, ran pytest, and point out any possible loop holes.

- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.

**Test 1: `test_parse_guess_float_rounds_correctly`**
This pytest verified that Bug #3 was fixed. When a user enters "42.7", the game now correctly rounds it to 43 (not floors it to 42). This test was crucial because it showed that float inputs are now treated fairly—users expect standard rounding behavior, not flooring. Without this test, the rounding bug could easily return if someone refactors the code later.

**Test 2: `test_update_score_first_attempt_win_max_points`**
This pytest demonstrated that Bug #7 was fixed. Winning on the first attempt now awards 100 points (the maximum), not 80 as the buggy code did. This test revealed that the scoring formula was using `(attempt_number + 1)` instead of `(attempt_number - 1)`. It ensures the game properly rewards perfect plays and prevents score ceiling bugs from reappearing in future updates.


- Did AI help you design or understand any tests? How?
AI helped me understand that the original tests on the test_game_logic.py has issues, i.e. the result of check_guess function should be tuples, so all three tests test_winning_guess, test_guess_too_high, test_guess_too_low should be revised.

AI helped me designed all tests about the bugs I fixed and even generated edgecase tests (as noted on the test_game_logic.py). I asked AI if there is any test that overlaps/is redundant, so I eliminated 1 AI-generated test in my final submission.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

Streamlit is used to build interactive, data-driven web-based dashboards and applications. Some people use it as an interactive front-end to test if their Python code works.

**Reruns**: Streamlit reruns the entire script from top to bottom every time a user interacts with the app (clicking a button, entering text, moving a slider, etc.). This is different from traditional web apps where only the specific function handling that interaction runs. The constant rerunning makes the app feel responsive and interactive—as if it's updating in real-time.

**Session State**: The challenge with reruns is that variables reset each time the script runs, so the app would "forget" everything. Session state is Streamlit's way of remembering things between reruns. Without session state, user input would disappear every time they clicked a button, making the app unusable. 

In app.py file, I noticed session_state was used. session_state is an attribute of the Streamlit module. This is a dictionary-like object that stores data specific to each user's session. Every time the script reruns, the values you stored in st.session_state persist, meaning they don't reset like regular Python variables would.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
I will commit to Git more frequently, i.e. at the end of any major stages in my project, and add a note on what were done in that stage. This project showed me that I can prompt AI to write me a note summarizing changes between commits and help me commit to Github, which is very helpful.

- What is one thing you would do differently next time you work with AI on a coding task?
Ask AI to write notes next to all changes made by AI. Even though I did review and approve the change before AI proceeded, sometimes it was still hard to follow and recall. I tended to forget the changes that AI made very quickly. 


- In one or two sentences, describe how this project changed the way you think about AI generated code.

AI generated codes can be inefficient and redundant, sometimes inaccurate - I used to just blindly accept whatevery AI recommended. However, redundant codes can be costly in real life. Now I realize AI's codes should be carefully supervised and optimized. 


