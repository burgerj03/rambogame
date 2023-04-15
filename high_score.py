HIGH_SCORE_FILE = 'high_score.txt'


def read_high_score():
    try:
        with open(HIGH_SCORE_FILE, 'r') as f:
            return int(f.read())
    except:
        return 0


def update_high_score(new_score):
    current_score = read_high_score()
    if new_score > current_score:
        with open(HIGH_SCORE_FILE, 'w') as f:
            f.write(str(new_score))
        return True
    return False
