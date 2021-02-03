import string
import random

class Wordsearch_Generator:
    def __init__(self, wordlist, size=12):
        '''Initialize wordsearch generator.'''
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
        self.wordlist = [word.upper() for word in wordlist]
        
        self.wordsearch_arr = [[None] * size for i in range(size)]
        self.solution = []


    def generate_puzzle(self, print_puzzle=True):
        self.insert_words()
        self.randomize()
        if print_puzzle:
            self.print_wordsearch()


    def reset_array(self):
        self.wordsearch_arr = [[None] * self.size for i in range(self.size)]


    def insert_words(self, max_tries=2):
        '''Insert words from wordlist into random positions of array.'''
        for word in self.wordlist:
            if not self.try_insert_word(word, max_tries):
                raise Exception(f"Was not able to insert word: {word} within {max_tries} tries.")


    def try_insert_word(self, word, max_tries):
        for _ in range(max_tries):
            possible_positions = self.get_possible_positions(len(word))
            while len(possible_positions) != 0:
                start = random.sample(possible_positions, 1)[0]
                possible_positions.remove(start)
                possible_directions = self.get_possible_directions(start, word)
                if len(possible_directions) != 0:
                    (change_i, change_j), is_reversed = random.choice(possible_directions)
                    self.solution.append((word, start, (change_i, change_j)))
                    if is_reversed:
                        word = word[::-1]
                    self.insert_word(word, start, change_i, change_j)
                    # found a valid insertion position, so break out to insert
                    # next word.
                    return True
            # When trying a new set of insertions, need to start with empty array
            self.reset_array()
            # Also need to generate new seed
            random.seed(random.random())
        return False


    def get_possible_positions(self, word_len):
        unsampled_positions = set()
        unfit_zone = self.size - word_len + 1
        for i in range(self.size):
            for j in range(self.size):
                if not (i >= unfit_zone and j >= unfit_zone):
                    unsampled_positions.add((i,j))
        return unsampled_positions


    def get_possible_directions(self, start, word):
        fitting_directions = self.get_fitting_directions(start, word)
        clear_directions = self.clear_directions(start, word, fitting_directions)
        return clear_directions


    def get_fitting_directions(self, start, word):
        '''
        
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


    def clear_directions(self, start, word, directions):
        '''
        
        '''
        def is_direction_clear_helper(self, start, word, direction):
            '''
            Check if the positions extending from start,
            with given length in given direction, are all None or
            has the correct letter at that position.
            '''
            i,j = start
            change_i, change_j = direction
            for letter in word:
                # position has to be empty or the letter at that
                # position must match
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
            if is_direction_clear_helper(self, start, word, direction):
                clear_directions.append((direction, False))
            # try word reversed
            if is_direction_clear_helper(self, start, word[::-1], direction):
                clear_directions.append((direction, True))
        return clear_directions


    def insert_word(self, word, start, change_i, change_j):
        '''
        Insert word into wordsearch array, overwriting if necessary.
        Word needs to be able to fit into array.
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


    def randomize(self):
        '''Replace None elts in array with random uppercase letters.'''
        for i, row in enumerate(self.wordsearch_arr):
            for j, elt in enumerate(row):
                if elt is None:
                    self.wordsearch_arr[i][j] = random.choice(string.ascii_uppercase)


    def print_wordsearch(self):
        '''Print wordsearch array.'''
        for row in self.wordsearch_arr:
            for char in row:
                print(char, end=" ")
            print("\n", end="")


    def print_solutions(self):
        for word, start, direction in self.solution:
            print(f"{word}: {start} -> {direction}")


if __name__ ==  "__main__":
    #"HAPPY", "APPLE", "LUCKY"
    test = Wordsearch_Generator(["HAPPY", "APPLE", "LUCKY"], size=5)
    test.insert_words()
    test.print_wordsearch()
    test.print_solutions()
    '''
    fail_count = 0
    for i in range(10000):
        test = Wordsearch_Generator(["HAPPY", "APPLE", "LUCKY"], size=5)
        try:
            test.insert_words()
        except Exception:
            fail_count += 1
    print(fail_count)
    '''
