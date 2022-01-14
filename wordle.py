import random
import sys

MAX_GUESSES = 6
WORD_LENGTH = 5

class Game:
    def __init__(self):
        self.guesses = []

    def guess(self, word):
        print('Guessing ' + word)
        self.guesses.append(word)
        return word == self.word

    def incomplete(self):
        return len(self.guesses) < MAX_GUESSES

    def win(self):
        print('You won, the word was ' + self.word)

    def lose(self):
        print('You lost, the word was ' + self.word)

    def num_guesses(self):
        return len(self.guesses)

    def fixed_letter(self, n):
        for g in self.guesses:
            if self.word[n] == g[n]:
                return self.word[n]
        return None

    def wild_letters(self):
        ls = []
        for g in self.guesses:
            for l in g:
                if l in self.word:
                    ls.append(l)
        return ls

    def bad_letters(self):
        ls = []
        for g in self.guesses:
            for l in g:
                if l not in self.word:
                    ls.append(l)
        return ls

def play():
    game = Game()
    dictionary = get_dictionary()
    game.word = random.choice(dictionary)
    while game.incomplete():
        potential_answers = find_potential_answers(game, dictionary)
        hist = histogram(potential_answers)
        if game.num_guesses() == MAX_GUESSES - 1:
            guess = random.choice(potential_answers)
        else:
            best_words = find_best_words(hist, dictionary)
            guess = random.choice(best_words)
        if game.guess(guess):
            game.win()
            return
    game.lose()


def histogram(words):
    hist = {}
    for word in words:
        for letter in word:
            hist[letter] = hist.get(letter, 0) + 1
    return hist

def find_potential_answers(game, dictionary):
    r = []
    for word in dictionary:
        if word in game.guesses:
            continue
        if not has_fixed_letters(word, game):
            continue
        if not has_wild_letters(word, game):
            continue
        if has_bad_letter(word, game):
            continue
        r.append(word)
    return r

def has_fixed_letters(word, game):
    for n in range(0, len(word)):
        if game.fixed_letter(n) and not word[n] == game.fixed_letter(n):
            return False
    return True

def has_wild_letters(word, game):
    for letter in game.wild_letters():
        if letter not in word: # BAKERT it also can't be in pos
            return False
    return True

def has_bad_letter(word, game):
    for letter in word:
        if letter in game.bad_letters():
            return True
    return False

def find_best_words(hist, dictionary):
    r = []
    best_score = find_best_score(hist, dictionary)
    for word in dictionary:
        if score(hist, word) == best_score:
            r.append(word)
    return r

def find_best_score(hist, dictionary):
    best_score = 0
    for word in dictionary:
        best_score = max(best_score, score(hist, word))
    return best_score

def score(hist, word):
    found = []
    n = 0
    for letter in word:
        if letter not in found:
            n += hist.get(letter, 0)
            found.append(letter)
    return n

def get_dictionary():
    with open('/usr/share/dict/words') as f:
        return [w.strip() for w in f.readlines() if len(w.strip()) == WORD_LENGTH and w.lower() == w]

def test():
    test_find_best_words()
    test_find_best_score()
    test_score()
    test_get_dictionary()

def test_find_best_words():
    hist = {
        'a': 10,
        'b': 1,
    }
    dictionary = ['a', 'baa', 'count']
    assert find_best_words(hist, dictionary) == ['baa']

def test_find_best_score():
    hist = {
        'a': 10,
        'b': 1,
    }
    dictionary = ['a', 'baa', 'count']
    assert find_best_score(hist, dictionary) == 11

def test_score():
    hist = {
        'a': 10,
        'b': 1,
    }
    assert score(hist, 'baa') == 11
    assert score(hist, 'count') == 0
    assert score(hist, 'a') == 10

def test_get_dictionary():
    d = get_dictionary()
    assert len(d) > 1000
    for w in d:
        assert len(w) == 5
        assert w.lower() == w

if len(sys.argv) < 2:
    play()
else:
    test()
