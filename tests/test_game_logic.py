from logic_utils import check_guess, parse_guess, get_range_for_difficulty, update_score

# Bug #2: check_guess - hints were reversed
def test_check_guess_correct():
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"
    assert "Correct" in message

def test_check_guess_too_high_returns_go_lower():
    """Bug #2 Fix: When guess > secret, hint should say 'Go LOWER' not 'Go HIGHER'"""
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in message

def test_check_guess_too_low_returns_go_higher():
    """Bug #2 Fix: When guess < secret, hint should say 'Go HIGHER' not 'Go LOWER'"""
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message


# Bug #3: parse_guess - float handling with rounding
def test_parse_guess_valid_int():
    ok, value, error = parse_guess("42")
    assert ok is True
    assert value == 42
    assert error is None

def test_parse_guess_float_rounds_correctly():
    """Bug #3 Fix: Float inputs should be rounded, not floored"""
    ok, value, error = parse_guess("42.7")
    assert ok is True
    assert value == 43  # 42.7 rounds to 43, not floors to 42
    assert error is None

def test_parse_guess_float_rounds_down():
    """Bug #3 Fix: Verify rounding down works too"""
    ok, value, error = parse_guess("42.3")
    assert ok is True
    assert value == 42  # 42.3 rounds down to 42
    assert error is None

def test_parse_guess_empty_string():
    ok, value, error = parse_guess("")
    assert ok is False
    assert value is None
    assert error == "Enter a guess."

def test_parse_guess_none():
    ok, value, error = parse_guess(None)
    assert ok is False
    assert value is None
    assert error == "Enter a guess."

def test_parse_guess_non_numeric():
    ok, value, error = parse_guess("abc")
    assert ok is False
    assert value is None
    assert error == "That is not a number."


# Bug #4: get_range_for_difficulty - correct ranges per difficulty
def test_easy_range():
    low, high = get_range_for_difficulty("Easy")
    assert (low, high) == (1, 20)

def test_normal_range():
    low, high = get_range_for_difficulty("Normal")
    assert (low, high) == (1, 100)

def test_hard_range():
    low, high = get_range_for_difficulty("Hard")
    assert (low, high) == (1, 50)

def test_unknown_difficulty_defaults_to_normal():
    low, high = get_range_for_difficulty("Unknown")
    assert (low, high) == (1, 100)


# Bug #7: update_score - max score should be 100, not 80
def test_update_score_first_attempt_win_max_points():
    """Bug #7 Fix: First attempt win should give 100 points (100 - 10*0), not 90 (80 - 10*1)"""
    new_score = update_score(0, "Win", 1)
    assert new_score == 100  # 100 - 10 * (1 - 1) = 100

def test_update_score_second_attempt_win():
    """Bug #7 Fix: Second attempt win should give 90 points"""
    new_score = update_score(0, "Win", 2)
    assert new_score == 90  # 100 - 10 * (2 - 1) = 90

def test_update_score_tenth_attempt_win_minimum():
    """Bug #7 Fix: Tenth attempt win should give minimum 10 points"""
    new_score = update_score(0, "Win", 10)
    assert new_score == 10  # 100 - 10 * (10 - 1) = 10, minimum enforced

def test_update_score_too_high_even_attempt():
    new_score = update_score(50, "Too High", 2)
    assert new_score == 55  # +5 for even attempt

def test_update_score_too_high_odd_attempt():
    new_score = update_score(50, "Too High", 1)
    assert new_score == 45  # -5 for odd attempt

def test_update_score_too_low():
    new_score = update_score(50, "Too Low", 1)
    assert new_score == 45  # -5 always


# Edge cases: parse_guess with unusual inputs
def test_parse_guess_leading_trailing_whitespace():
    """Input with whitespace should still parse"""
    ok, value, _ = parse_guess("  42  ")
    assert ok is True
    assert value == 42

def test_parse_guess_negative_number():
    """Negative numbers should parse correctly"""
    ok, value, _ = parse_guess("-15")
    assert ok is True
    assert value == -15

def test_parse_guess_very_large_number():
    """Very large numbers should parse"""
    ok, value, _ = parse_guess("999999")
    assert ok is True
    assert value == 999999

def test_parse_guess_scientific_notation():
    """Scientific notation should fail (not a valid guess format)"""
    ok, _, error = parse_guess("1e5")
    assert ok is False
    assert error == "That is not a number."

def test_parse_guess_multiple_decimals():
    """Multiple decimals should fail"""
    ok, _, error = parse_guess("42.3.5")
    assert ok is False
    assert error == "That is not a number."

def test_parse_guess_zero():
    """Zero should parse correctly"""
    ok, value, _ = parse_guess("0")
    assert ok is True
    assert value == 0


# Edge cases: score floor
def test_update_score_multiple_wrong_guesses():
    """Simulate multiple wrong guesses deducting points"""
    score = 50
    score = update_score(score, "Too High", 1)  # -5 → 45
    score = update_score(score, "Too Low", 1)   # -5 → 40
    score = update_score(score, "Too Low", 1)   # -5 → 35
    assert score == 35


# Full game flow scenarios
def test_full_game_flow_multiple_guesses_then_win():
    """Simulate a complete game: multiple wrong guesses, then win on attempt 4"""
    secret = 50
    score = 0

    # Attempt 1: guess too low
    ok, guess1, _ = parse_guess("30")
    assert ok is True
    outcome, _ = check_guess(guess1, secret)
    assert outcome == "Too Low"
    score = update_score(score, outcome, 1)
    assert score == -5  # -5 for Too Low

    # Attempt 2: guess too high (even attempt, +5)
    ok, guess2, _ = parse_guess("70")
    assert ok is True
    outcome, _ = check_guess(guess2, secret)
    assert outcome == "Too High"
    score = update_score(score, outcome, 2)
    assert score == 0  # -5 + 5 = 0

    # Attempt 3: guess too low
    ok, guess3, _ = parse_guess("40")
    assert ok is True
    outcome, _ = check_guess(guess3, secret)
    assert outcome == "Too Low"
    score = update_score(score, outcome, 3)
    assert score == -5  # 0 - 5 = -5

    # Attempt 4: correct guess
    ok, guess4, _ = parse_guess("50")
    assert ok is True
    outcome, _ = check_guess(guess4, secret)
    assert outcome == "Win"
    score = update_score(score, outcome, 4)
    assert score == 65  # -5 + (100 - 10*(4-1)) = -5 + 70 = 65

def test_full_game_flow_first_attempt_win():
    """Best case: win on first attempt for max score"""
    secret = 42
    score = 0

    ok, guess, _ = parse_guess("42")
    assert ok is True
    outcome, _ = check_guess(guess, secret)
    assert outcome == "Win"
    score = update_score(score, outcome, 1)
    assert score == 100  # Perfect game

