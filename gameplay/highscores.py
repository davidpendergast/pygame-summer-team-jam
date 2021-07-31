
_BEST_SCORE = 0


def add_new_score(score):
    global _BEST_SCORE
    _BEST_SCORE = max(score, _BEST_SCORE)


def get_best():
    return _BEST_SCORE


def save_score():
    # TODO ?
    pass


def load_score():
    # TODO ?
    pass
