import itertools
import random
import string
import timeit

import numpy as np

# Define the characters allowed in the password
allowed_chars = string.ascii_letters + string.digits + " "

# Simulation of Database
password_database = {"admin": "MyStr0ngPassW0rD"}


def check_password(user, guess):
    
    # Check if the given `guess` matches the password associated with the `user` in the `password_database`.

    # Args:
    #     user (str): The username.
    #     guess (str): The password guess.
    # Returns:
    #     bool: True if the guess is correct, False otherwise.
    
    actual = password_database.get(user)
    if actual is None or len(guess) != len(actual):
        return False

    return all(guess[i] == actual[i] for i in range(len(actual)))


def random_str(size):
    
    # Generate a random string of characters from `allowed_chars` of the specified `size`.

    # Args:
    #     size (int): The length of the generated string.

    # Returns:
    #     str: The random string.
    
    return ''.join(random.choices(allowed_chars, k=size))


def crack_length(user, max_len=32, verbose=False):
    
    # Determine the likely length of the password associated with a given `user`.

    # This function measures the time taken to check a series of randomly generated passwords of varying lengths
    # and chooses the length that took the most time.

    # Args:
    #     user (str): The username.
    #     max_len (int): The maximum length to consider for the password. Defaults to 32.
    #     verbose (bool): If True, print additional information about the analysis. Defaults to False.

    # Returns:
    #     int: The most likely length of the password.
    
    trials = 2000
    times = np.empty(max_len)
    for i in range(max_len):
        i_time = timeit.repeat(stmt='check_password(user, x)',
                               setup=f'user={user!r};x=random_str({i!r})',
                               globals=globals(),
                               number=trials,
                               repeat=10)
        times[i] = min(i_time)

    if verbose:
        most_likely_n = np.argsort(times)[::-1][:5]
        print(most_likely_n, times[most_likely_n] / times[most_likely_n[0]])

    most_likely = int(np.argmax(times))
    return most_likely


def crack_password(user, length, verbose=False):
    
    # Crack the password associated with a given `user`.

    # This function generates and tests different variations of the password until the correct one is found.

    # Args:
    #     user (str): The username.
    #     length (int): The length of the password.
    #     verbose (bool): If True, print the progress of the cracking process. Defaults to False.

    # Returns:
    #     str: The cracked password.
    
    guess = random_str(length)
    counter = itertools.count()
    trials = 1000
    while True:
        i = next(counter) % length
        for c in allowed_chars:
            alt = guess[:i] + c + guess[i + 1:]

            alt_time = timeit.repeat(stmt='check_password(user, x)',
                                     setup=f'user={user!r};x={alt!r}',
                                     globals=globals(),
                                     number=trials,
                                     repeat=10)
            guess_time = timeit.repeat(stmt='check_password(user, x)',
                                       setup=f'user={user!r};x={guess!r}',
                                       globals=globals(),
                                       number=trials,
                                       repeat=10)

            if check_password(user, alt):
                return alt

            if min(alt_time) > min(guess_time):
                guess = alt
                if verbose:
                    print(guess)


def main():
    # Define the target username
    user = "admin"

    # Determine the likely length of the password
    length = crack_length(user, verbose=True)
    print(f"Most likely length: {length}")
    input("Press Enter to continue...")
    password = crack_password(user, length, verbose=True)
    print(f"Password cracked: '{password}'")


if __name__ == '__main__':
    main()
