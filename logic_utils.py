# Refactored from app.py by Claude Code - Reviewed and approved by user before implementation
def get_range_for_difficulty(difficulty: str):
    """Return the inclusive (low, high) number range for a given difficulty level.

    Args:
        difficulty (str): One of "Easy", "Normal", or "Hard".
            - "Easy"   → 1–20
            - "Normal" → 1–100
            - "Hard"   → 1–50
            Unrecognized values fall back to the Normal range (1–100).

    Returns:
        tuple[int, int]: A (low, high) pair representing the inclusive bounds
        of the random number range for the chosen difficulty.

    Examples:
        >>> get_range_for_difficulty("Easy")
        (1, 20)
        >>> get_range_for_difficulty("Hard")
        (1, 50)
        >>> get_range_for_difficulty("Unknown")
        (1, 100)
    """
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 50
    return 1, 100


# Refactored from app.py by Claude Code - All Bug #3 comments preserved during collaboration with user
def parse_guess(raw: str):
    """Parse raw user input into an integer guess value.

    Accepts whole-number strings and decimal strings. Decimal inputs are
    rounded to the nearest integer (Bug #3 fix — previously truncated via
    int()). Returns a structured 3-tuple so callers can distinguish between
    a valid guess and a validation error without raising exceptions.

    Args:
        raw (str | None): The raw string submitted by the user. May be None
            (e.g. when the form field is empty before submission) or an empty
            string, both of which are treated as missing input.

    Returns:
        tuple: A 3-element tuple ``(ok, guess, error)``:
            - ok (bool): True if the input was successfully parsed.
            - guess (int | None): The parsed integer, or None on failure.
            - error (str | None): A human-readable error message, or None on
              success.

    Examples:
        >>> parse_guess("42")
        (True, 42, None)
        >>> parse_guess("3.7")
        (True, 4, None)
        >>> parse_guess("")
        (False, None, 'Enter a guess.')
        >>> parse_guess("abc")
        (False, None, 'That is not a number.')
    """
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        # FIX: Bug #3 allows float inputs by rounding them DOWN to the nearest integer instead of ROUNDING them.
        if "." in raw:
            value = round(float(raw)) # <- Bug 3 Fix: round instead of floor, change int() to round()
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


# Refactored from app.py by Claude Code - All Bug #2 comments and commented-out buggy code preserved with user approval
def check_guess(guess, secret):
    """Compare the player's guess against the secret number and return a result.

    Determines whether the guess is correct, too high, or too low. The hint
    direction is intentionally correct here — "Too High" means the player
    should go lower, and "Too Low" means the player should go higher (Bug #2
    fix — the original hints were reversed).

    Args:
        guess (int): The integer value submitted by the player.
        secret (int): The randomly generated target number for the round.

    Returns:
        tuple[str, str]: A 2-element tuple ``(outcome, message)``:
            - outcome (str): One of ``"Win"``, ``"Too High"``, or ``"Too Low"``.
            - message (str): A display-ready string with an emoji hint shown
              to the player (e.g. ``"📈 Go LOWER!"``).

    Examples:
        >>> check_guess(50, 50)
        ('Win', '🎉 Correct!')
        >>> check_guess(75, 50)
        ('Too High', '📈 Go LOWER!')
        >>> check_guess(25, 50)
        ('Too Low', '📉 Go HIGHER!')
    """
    if guess == secret:
        return "Win", "🎉 Correct!"
    # FIX: Bug #2 hints are reversed incorrectly, fixed below.

    # BUGGY CODE (commented out - try/except no longer needed since Bug #6 is fixed, secret is always integer):
    # try:
    #     if guess > secret:
    #         return "Too High", "📈 Go LOWER!" # <- Bug 2 Fix: HIGHER becomes LOWER
    #     else:
    #         return "Too Low", "📉 Go HIGHER!" # <- Bug 2 Fix: LOWER becomes HIGHER
    # except TypeError:
    #     g = str(guess)
    #     if g == secret:
    #         return "Win", "🎉 Correct!"
    #     if g > secret:
    #         return "Too High", "📈 Go LOWER!" # <- Bug 2 Fix: HIGHER becomes LOWER
    #     return "Too Low", "📉 Go HIGHER!" # <- Bug 2 Fix: LOWER becomes HIGHER

    if guess > secret:
        return "Too High", "📈 Go LOWER!" # <---- Bug 2 Fix: HIGHER becomes LOWER
    else:
        return "Too Low", "📉 Go HIGHER!"#  <---- Bug 2 Fix: LOWER becomes HIGHER


# Refactored from app.py by Claude Code - All Bug #7 comments preserved during user collaboration
def update_score(current_score: int, outcome: str, attempt_number: int):
    """Calculate and return a new score after evaluating a single guess outcome.

    Scoring rules:
        - **Win**: Awards ``100 - 10 * (attempt_number - 1)`` points, with a
          floor of 10. A correct guess on the first attempt earns the maximum
          100 points (Bug #7 fix — the original formula used
          ``attempt_number + 1``, capping first-attempt wins at 80).
        - **Too High**: Awards +5 on even-numbered attempts, deducts −5 on
          odd-numbered attempts.
        - **Too Low**: Always deducts −5 points.
        - Any other outcome leaves the score unchanged.

    Args:
        current_score (int): The player's score before this guess.
        outcome (str): Result string from ``check_guess()``. Expected values
            are ``"Win"``, ``"Too High"``, or ``"Too Low"``.
        attempt_number (int): 1-based index of the current attempt within the
            round (i.e. 1 for the first guess, 2 for the second, etc.).

    Returns:
        int: The updated score after applying the outcome's point adjustment.

    Examples:
        >>> update_score(0, "Win", 1)
        100
        >>> update_score(100, "Win", 5)
        160
        >>> update_score(50, "Too High", 2)
        55
        >>> update_score(50, "Too Low", 3)
        45
    """
    if outcome == "Win":
        #FIX: Bug #7 maximum score is 80 but should be 100.
        points = 100 - 10 * (attempt_number - 1) # <--- changed (attempt_number + 1) to (attempt_number - 1) to allow max 100 on first attempt
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High":
        if attempt_number % 2 == 0:
            return current_score + 5
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score
