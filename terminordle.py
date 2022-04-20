"""
a wordle emulator in the terminal
"""
from collections import Counter
from random import choice
from termcolor import colored
import sys, argparse

ALLOWED_GUESSES = 6


def play(word=None):
    """
    plays wordle with the given word

    rules:
        1. letters show up as green when they are correctly in the right position
        2. letters show up as yellow when they are in the word, but not in the right position
            letters will be yellowed from left to right until there are no more letters to be yellowed
            that is, if we guess a word with two 'x' and the correct word only has one 'x' in a different position,
            the leftmost x is yellowed
            if we guess a word with two 'x' and the correct word has three 'x' in matching and different positions,
            then we will green out the 'x's that we can and then yellow the rest of the 'x's from left to right
    """
    with open('dictionaries/valid_answers.txt') as f:
        if word is None:
            word = choice(f.read().split('\n'))
        elif not word in f.read():
            print(f'{word} is an invalid word choice to play wordle')
            return

    n = len(word)

    print(f"your word is of length {n}. guess!")

    # COLOR_CODE_ESCAPES = {'green': '\N{large green square}', 'yellow': '\N{large yellow square}', 'grey': '\N{white large square}'}

    def guess_word(guess):
        """
        guesses a word, returns the result array

        the result array is an word-length array with numbers representing colors:

        0 - grey
        1 - yellow
        2 - green
        """

        ret = ["" for _ in range(n)]
        word_letter_counts = Counter(word)

        # check for greens and decrement word_letter_counts for matches
        for i in range(n):
            if guess[i] == word[i]:
                # found green match
                ret[i] = colored(guess[i], 'green', attrs=['bold'])
                word_letter_counts[guess[i]] -= 1

        for letter, count in word_letter_counts.items():
            i = 0
            while i < n and count > 0:
                if guess[i] == letter and not ret[i]:
                    ret[i] = colored(guess[i], 'yellow', attrs=['bold'])
                    count -= 1
                i += 1

        return ''.join([x if x else colored(guess[idx], 'grey', attrs=['bold']) for idx, x in enumerate(ret) ])

    guess_num = 1

    while guess_num <= ALLOWED_GUESSES:
        guess = input()
        m = len(guess)

        if len(guess) != n:
            sys.stdout.write(f"\033[A\033[{m}C\033[K")
            sys.stdout.write(f"\033[{1}C")

            print(f"guess is invalid: must be of length {n}. try again!")
            sys.stdout.write(f"\033[A")
            continue

        with open('dictionaries/valid_guesses.txt') as f:
            if not guess in f.read():
                sys.stdout.write(f"\033[A\033[{m}C\033[K")
                sys.stdout.write(f"\033[{1}C")
                print(f"guess is invalid: guess is not in our dictionary. try again!")
                sys.stdout.write(f"\033[A")
                continue

        sys.stdout.write("\033[A\033[K")
        guess_result = guess_word(guess)
        print(guess_result)


        if guess.lower() == word.lower():
            print("congrats! you won :)")
            return

        guess_num += 1

    print(f'too bad :( the word was {word}')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='play wordle <3')
    parser.add_argument('word', nargs='?' , default=None, type=str, help='optional word to play. uses a random word by default')
    args = parser.parse_args()
    play(args.word)
