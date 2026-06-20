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
  
  **Bug #4:** The game announcement is always "Guess a number between 1 and 100" regardless of what difficulty level is selected.
  
  **Bug #5:** The secret number is converted to a string on even-numbered attempts, but in odd attempts, it remains an integer. On odd attempts the game works correctly, but on even attempts it yields incorrect results.
  
  **Bug #6:** Maximum score is 80, but it should be 100.
  
  **Bug #7:** After bug #1 is fixed, count of attempts left still lags by 1 in the info section, even though it is still correctly recorded in the system.

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
Claude Haiku 4.5

- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
I asked Claude Haiku about Bug #1 (attempts left showing 7 instead of 8). Claude explained the problem and pointed me to line 96 of app.py where the issue was. I implemented the fix Claude suggested and refreshed the page to test. After the fix, I verified that at Normal level, Attempts left shows 8; at Easy level, it shows 6; and at Hard level, it shows 5 - all correct.

- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
[Please add your example here]

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
