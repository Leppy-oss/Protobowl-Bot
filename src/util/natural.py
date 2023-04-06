import random
import math
from string import ascii_lowercase
from string import ascii_uppercase
from itertools import islice

srand = random.random()
random.seed(srand)

k_mu_n_g = 0.15
k_sigma_n_g = 0.05
cpm = 1000  # chars per minute of the bot's chunks
t_buzz = 7  # seconds
k_mu_n_s = 0.15
k_sigma_n_s = 0.01


def naturalize_guess(guess: str) -> str:
    # split the guess into a string of words to "naturalize" independently
    guess_split = guess.split()
    naturalized_words = []

    for w in guess_split:
        w_l = list(w)
        if len(w_l) > 6:
            i_all = [i for i, _ in enumerate(w_l)]
            # randomizing the first letter may result in Protobowl counting it wrong!
            i_all.pop(0)
            num_randomize = abs(math.floor(gaussian_rand(
                float(len(i_all)) * k_mu_n_g, float(len(i_all)) * k_mu_n_g)))
            i_rand = random.sample(i_all, num_randomize)
            for i in i_rand:
                if weighted_tf(0.7):
                    # replace this char in the word with a random letter with an 80% chance of being lowercase
                    w_l[i] = random.choice(
                        ascii_lowercase if weighted_tf(0.8) else ascii_uppercase)
                elif (weighted_tf(0.67)):
                    w_l.insert(i, random.choice(ascii_lowercase if weighted_tf(
                        0.8) else ascii_uppercase))  # 20% to insert instead of replace
                else:
                    pass  # 10% chance to delete instead of insert OR replace

        naturalized_words.append(''.join(w_l))

    return ' '.join(naturalized_words)


def naturalized_splits(guess: str) -> list:
    min_chunk_size = 1
    max_chunk_size = max(math.floor(gaussian_rand(
        len(guess) * k_mu_n_s, len(guess) * k_sigma_n_s)), 2)
    chunks = list(r_chunks(guess, min_chunk_size, max_chunk_size))
    splits = []  # tuple of words + delay
    for chunk in chunks:
        splits.append((chunk, gaussian_rand(
            len(chunk) / cpm * 60, 0.2, min=0)))

    return splits


def weighted_tf(weight_t: float) -> bool:
    if random.random() < weight_t:
        return True

    return False


def r_chunks(guess: str, size_min, size_max) -> str:
    i = iter(guess)
    while True:
        n = list(islice(i, random.randint(size_min, size_max)))
        if n:
            yield ''.join(n)
        else:
            break


def gaussian_rand(mu: float, sigma: float, min: float = -1e9, max: float = 1e9) -> float:
    # handle edge cases
    if min < -1e8:
        min = mu - sigma
    if max > 1e8:
        max = mu + sigma

    return clip(random.gauss(mu, sigma), min, max)


def clip(x, min, max):
    if x < min:
        return min
    elif x > max:
        return max
    return x