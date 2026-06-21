# Refactored from app.py - Reviewed and approved by user before implementation
def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 50
    return 1, 100


# Refactored from app.py - All Bug #3 comments preserved during collaboration with user
def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
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


# Refactored from app.py - All Bug #2 comments and commented-out buggy code preserved with user approval
def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
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


# Refactored from app.py - All Bug #7 comments preserved during user collaboration
def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
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
