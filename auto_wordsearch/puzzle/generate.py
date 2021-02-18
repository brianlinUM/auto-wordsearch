"""
Random Wordsearch Generator.

By Brian Lin (brianlin@umich.edu), 2021
"""
import string
import random


class WordsearchGenerator:
    """Generates a square wordsearch puzzle randomly, from a list of words."""

    def __init__(self, wordlist, size=12):
        """
        Initialize wordsearch generator.

        args:
        wordlist (list): list of words (str) to be added into wordsearch
            puzzle. All words need to have length of puzzle size or smaller.
        size (int): size of the square puzzle to be generated. Default: 12
        """
        if not isinstance(size, int) or size < 0:
            raise Exception("size needs to be a positive int")
        self.size = size

        if not isinstance(wordlist, list):
            raise Exception("wordlist is not a list")
        for word in wordlist:
            if not isinstance(word, str) or len(word) == 0:
                raise Exception("wordlist does not consist of non-empty str")
            if len(word) > self.size:
                raise Exception((
                    f"word: {word} does not fit in,",
                    f" puzzle of size {size}"
                ))
        # Make all letters uppercase for uniformity
        self.wordlist = [word.upper() for word in wordlist]
        # All positions start as None so that we know which to randomize
        self.wordsearch_arr = [[None] * size for i in range(size)]
        # Stores information on how to solve the puzzle
        self.solution = []

    def generate_puzzle(self, print_puzzle=True):
        """
        Generate a new, randomized wordsearch puzzle.

        args:
        print_puzzle (bool): if True, print the generated puzzle.
        """
        self.insert_words()
        self.random_fill()
        if print_puzzle:
            self.print_wordsearch()

    def reset_array(self):
        """Clear the wordsearch array by making all elements None."""
        self.wordsearch_arr = [[None] * self.size for i in range(self.size)]

    def insert_words(self, max_tries=5):
        """
        Attempt to randomly insert all puzzle words into the array.

        Will attempt to find a permutation that fits all words, but success
        is not guaranteed. Will retry up to max_tries.

        args:
        max_tries (int): max number of times to attempt inserting all words
            into the puzzle array.
        """
        for _ in range(max_tries):
            if self.__try_insert_all_words():
                return
            # Need to start with empty array when trying new set of insertions
            self.reset_array()

        raise Exception(
            f"Was not able to insert all words within {max_tries} tries."
        )

    def __try_insert_all_words(self):
        """
        Attempt to insert all words into the puzzle array once.

        Returns True if success, else False.
        """
        for word in self.wordlist:
            if not self.__try_insert_single_word(word):
                return False
        return True

    def __try_insert_single_word(self, word):
        """
        Attempt to insert a word into a random position in the puzzle array.

        Returns True if success, else False.

        args:
        word (str): word to be inserted into puzzle array.
        """
        possible_positions = self.__get_possible_positions(len(word))
        while len(possible_positions) != 0:
            # try a random start position
            start = random.sample(possible_positions, 1)[0]
            # remove selected position so that we don't resample it in next try
            possible_positions.remove(start)
            # obtain all possible directions from the start position
            possible_directions = self.__get_possible_directions(start, word)
            if len(possible_directions) != 0:
                # choose a random direction and insert word at start position
                (change_i, change_j), is_reversed = random.choice(
                    possible_directions)
                self.solution.append((
                    word, start, (change_i, change_j), is_reversed))
                if is_reversed:
                    word = word[::-1]
                self.__insert_word(word, start, change_i, change_j)
                return True
            # retry with new start position if no directions possible
        return False

    def __get_possible_positions(self, word_len):
        """
        Return all coordinates that a word of length word_len can fit in.

        Considers all possible orientations.

        args:
        word_len (int): length of word to be considered.
        """
        possible_positions = set()
        # top left corner index of the zone in which the word can not fit in
        unfit_zone = self.size - word_len + 1
        for i in range(self.size):
            for j in range(self.size):
                # only add positions that the word can fit in
                if not (i >= unfit_zone and j >= unfit_zone):
                    possible_positions.add((i, j))
        return possible_positions

    def __get_possible_directions(self, start, word):
        """
        Return all valid directions word can have from the start coordinates.

        args:
        start ((int, int)): coordinates that the word is considered to be
            inserted at.
        word (str): word to be considered to insert.
        """
        fitting_directions = self.__get_fitting_directions(start, word)
        clear_directions = self.__get_clear_directions(
            start, word, fitting_directions)
        return clear_directions

    def __get_fitting_directions(self, start, word):
        """
        Return all directions word can have while fitting in the puzzle array.

        args:
        start ((int, int)): coordinates that the word is considered to be
            inserted at.
        word (str): word to be considered to insert.
        """
        i, j = start
        unfit_zone = self.size - len(word) + 1
        possible = []
        i_fit = i < unfit_zone
        j_fit = j < unfit_zone

        if i_fit:
            possible.append((1, 0))
            if j_fit:
                possible.append((0, 1))
                possible.append((1, 1))
        elif j_fit:
            # but not i_fit
            possible.append((0, 1))
        # Check if we can add (-1,1) diagonal
        if i >= len(word) - 1 and j_fit:
            possible.append((-1, 1))

        return possible

    def __get_clear_directions(self, start, word, directions):
        """
        Return all the directions that the word can be inserted, from start.

        args:
            start ((int, int)): coordinate to check for
                if a word can be inserted at.
            word (str): word to check if it can be inserted into array
            direction ((int,int)): change in i and j for the inserting
                position, for each letter inserted.
        """
        def __is_direction_clear_helper(self, start, word, direction):
            """
            Check if valid to insert word at a given position and orientation.

            A direction is valid if the positions extending from start, with
            given length in given direction, are all None or has the correct
            letter at that position.
            """
            i, j = start
            change_i, change_j = direction
            for letter in word:
                # position has to be None, or the letter at that position must
                # match with corresponding letter of word considered for
                # insertion
                if (
                    self.wordsearch_arr[i][j] is not None and
                    self.wordsearch_arr[i][j] != letter
                ):
                    return False
                i += change_i
                j += change_j
            return True

        clear_directions = []
        for direction in directions:
            # Consider both normal and reversed directions
            if __is_direction_clear_helper(self, start, word, direction):
                clear_directions.append((direction, False))
            if __is_direction_clear_helper(self, start, word[::-1], direction):
                clear_directions.append((direction, True))
        return clear_directions

    def __insert_word(self, word, start, change_i, change_j):
        """
        Insert word into wordsearch array.

        Word needs to be able to fit into array.

        args:
        word (str): word to insert into puzzle array.
        start ((int, int)): coordinate to begin inserting the word.
        change_i: (int): change in i for the inserting position,
            for each letter inserted.
        change_j: (int): change in j for the inserting position,
            for each letter inserted.
        """
        i, j = start
        for letter in word:
            self.wordsearch_arr[i][j] = letter
            i += change_i
            j += change_j

    def random_fill(self):
        """Replace None elts in array with random uppercase letters."""
        for i, row in enumerate(self.wordsearch_arr):
            for j, elt in enumerate(row):
                if elt is None:
                    # We only use uppercase, for uniformity
                    self.wordsearch_arr[i][j] = random.choice(
                        string.ascii_uppercase)

    def print_wordsearch(self):
        """Print wordsearch puzzle."""
        for row in self.wordsearch_arr:
            for char in row:
                print(char, end=" ")
            print("\n", end="")

    def print_solutions(self):
        """Print out the solution to the generated puzzle."""
        for word, start, direction, is_reversed in self.solution:
            print(f"{word}: {start} -> {direction}, reversed: {is_reversed}")


if __name__ == "__main__":
    # "HAPPY", "APPLE", "LUCKY"
    test = WordsearchGenerator(["HAPPY", "APPLE", "LUCKY"], size=15)
    test.generate_puzzle()
