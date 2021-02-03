import string
import random

class Wordsearch_Generator:
    def __init__(self, wordlist, size=12):
        '''
        Initialize wordsearch generator.

        args:
        wordlist (list): list of words (str) to be added into wordsearch puzzle. All words need to
            have length of puzzle size or smaller.
        size (int): size of the square puzzle to be generated. Default: 12
        '''
        if type(size) != int or size < 0:
            raise Exception("size needs to be a positive int")
        self.size = size

        if type(wordlist) != list:
            raise Exception("wordlist is not a list")
        for word in wordlist:
            if type(word) != str or len(word) == 0:
                raise Exception("wordlist does not consist of non-empty str")
            if len(word) > self.size:
                raise Exception(f"word: {word} does not fit in puzzle of size {size}")
        # Make all letters uppercase for uniformity
        self.wordlist = [word.upper() for word in wordlist]
        # All positions start as None so that we know which positions to randomize
        self.wordsearch_arr = [[None] * size for i in range(size)]
        # Stores information on how to solve the puzzle
        self.solution = []


    def generate_puzzle(self, print_puzzle=True):
        '''
        Generate a new, randomized wordsearch puzzle.

        args:
        print_puzzle (bool): if True, print the generated puzzle.
        '''
        self.insert_words()
        self.random_fill()
        if print_puzzle:
            self.print_wordsearch()


    def reset_array(self):
        '''Clear the wordsearch array by making all elements None.'''
        self.wordsearch_arr = [[None] * self.size for i in range(self.size)]


    def insert_words(self, max_tries=5):
        '''
        Attempt to randomly insert all puzzle words into the array.
        Will attempt to find a permutation that fits all words, but success is not guaranteed.
        Will retry up to max_tries.

        args:
        max_tries (int): max number of times to attempt inserting all words into the puzzle array.
        '''
        for _ in range(max_tries):
            if self.__try_insert_all_words():
                return
            # When trying a new set of insertions, need to start with empty array
            self.reset_array()

        raise Exception(f"Was not able to insert all words within {max_tries} tries.")


    def __try_insert_all_words(self):
        '''
        Attempt to insert all words into the puzzle array once.
        Returns True if success, else False.
        '''
        for word in self.wordlist:
            if not self.__try_insert_single_word(word):
                return False
        return True


    def __try_insert_single_word(self, word):
        '''
        Attempt to insert a word into a random position in the puzzle array.
        Returns True if success, else False.
    
        args:
        word (str): word to be inserted into puzzle array.
        '''
        possible_positions = self.__get_possible_positions(len(word))
        while len(possible_positions) != 0:
            # try a random start position
            start = random.sample(possible_positions, 1)[0]
            # remove selected position so that we don't resample it in next try
            possible_positions.remove(start)
            # obtain all possible directions from the start position
            possible_directions = self.__get_possible_directions(start, word)
            if len(possible_directions) != 0:
                # choose a random direction, then insert the word at start position
                (change_i, change_j), is_reversed = random.choice(possible_directions)
                self.solution.append((word, start, (change_i, change_j), is_reversed))
                if is_reversed:
                    word = word[::-1]
                self.__insert_word(word, start, change_i, change_j)
                return True
            # retry with new start position if no directions possible
        return False


    def __get_possible_positions(self, word_len):
        '''
        Return all coordinates that a word of length word_len can fit in, with any orientation.

        args:
        word_len (int): length of word to be considered.
        '''
        possible_positions = set()
        # the index of the top left corner of the zone in which the word can not fit in
        unfit_zone = self.size - word_len + 1
        for i in range(self.size):
            for j in range(self.size):
                # only add positions that the word can fit in
                if not (i >= unfit_zone and j >= unfit_zone):
                    possible_positions.add((i,j))
        return possible_positions


    def __get_possible_directions(self, start, word):
        '''
        Return all valid directions that the word can have if inserted at a starting coordinate.

        args:
        start ((int, int)): coordinates that the word is considered to be inserted at.
        word (str): word to be considered to insert.
        '''
        fitting_directions = self.__get_fitting_directions(start, word)
        clear_directions = self.get_clear_directions(start, word, fitting_directions)
        return clear_directions


    def __get_fitting_directions(self, start, word):
        '''
        Return all directions that the word can have while fitting in the puzzle array.

        args:
        start ((int, int)): coordinates that the word is considered to be inserted at.
        word (str): word to be considered to insert.
        '''
        i, j = start
        unfit_zone = self.size - len(word) + 1
        possible = [(0,1), (1,0), (1,1)]
        # Remove infeasible directions
        i_unfit = i >= unfit_zone
        j_unfit = j >= unfit_zone
        if i_unfit or j_unfit:
            possible.pop(2)
            if i_unfit: possible.pop(1)
            if j_unfit: possible.pop(0)

        return possible


    def get_clear_directions(self, start, word, directions):
        '''
        Return all the directions (orientations) that the word can be inserted with, at the given
        (start) coordinate.

        args:
            start ((int, int)): coordinate to check if a word can be inserted at.
            word (str): word to check if it can be inserted into array
            direction ((int,int)): change in i and j for the inserting position,
                for eachletter inserted. 
        '''
        def __is_direction_clear_helper(self, start, word, direction):
            '''
            Check if it is valid to insert a word at a given position and orientation.
            A direction is valid if the positions extending from start,with given length in given
            direction, are all None or has the correct letter at that position.
            '''
            i,j = start
            change_i, change_j = direction
            for letter in word:
                # position has to be None or the letter at that
                # position must match with corresponding letter of word considered for insertion
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
        '''
        Insert word into wordsearch array.
        Word needs to be able to fit into array.

        args:
        word (str): word to insert into puzzle array.
        start ((int, int)): coordinate to begin inserting the word.
        change_i: (int): change in i for the inserting position, for each letter inserted.
        change_j: (int): change in j for the inserting position, for each letter inserted.
        '''
        i,j = start
        if not (-1 < i < self.size and -1 < j < self.size):
            raise Exception("start must be valid indices of array")
        if change_i == 0 and change_j == 0:
            raise Exception("change in i and j can not both be 0")
        if not (-1 < change_i < 2 and -1 < change_j < 2):
            raise Exception("change in i and j must be either 0 or 1")
        if (
            i + len(word) * change_i > self.size or
            j + len(word) * change_j > self.size
        ):
            raise Exception("word won't be able to fit into array")

        for letter in word:
            self.wordsearch_arr[i][j] = letter
            i += change_i
            j += change_j


    def random_fill(self):
        '''Replace None elts in array with random uppercase letters.'''
        for i, row in enumerate(self.wordsearch_arr):
            for j, elt in enumerate(row):
                if elt is None:
                    # We only use uppercase, for uniformity
                    self.wordsearch_arr[i][j] = random.choice(string.ascii_uppercase)


    def print_wordsearch(self):
        '''Print wordsearch puzzle.'''
        for row in self.wordsearch_arr:
            for char in row:
                print(char, end=" ")
            print("\n", end="")


    def print_solutions(self):
        '''Print out the solution to the generated puzzle.'''
        for word, start, direction, reversed in self.solution:
            print(f"{word}: {start} -> {direction}, reversed: {reversed}")


if __name__ ==  "__main__":
    #"HAPPY", "APPLE", "LUCKY"
    test = Wordsearch_Generator(["HAPPY", "APPLE", "LUCKY"], size=5)
    test.generate_puzzle()
    '''
    fail_count = 0
    for i in range(100000):
        test = Wordsearch_Generator(["HAPPY", "APPLE", "LUCKY"], size=5)
        try:
            test.insert_words(max_tries=5)
        except Exception:
            fail_count += 1
    print(fail_count)
    '''
