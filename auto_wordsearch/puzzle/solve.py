"""
Wordsearch Solver.

By Brian Lin (brianlin@umich.edu), 2021
"""

from generate import WordsearchGenerator


class WordsearchSolver:
    """Search for words within a square grid of characters."""

    _directions = {
        "N": 0, "NE": 1, "E": 2, "SE": 3, "S": 4, "SW": 5, "W": 6, "NW": 7}
    _pos_changes = {
        0: (-1, 0), 1: (-1, 1), 2: (0, 1), 3: (1, 1), 4: (1, 0), 5: (1, -1),
        6: (0, -1), 7: (-1, -1)
    }  # change in puzzle index for given directions

    def __init__(self, puzzle, wordlist):
        """
        Initialize wordsearch solver parameters.

        args:
        puzzle (list(list(chars))): 2d puzzle array of characters to search.
        wordlist (list(str)): list of words (str) to be searched for. All words
            need to fit in the puzzle array.
        """
        if not isinstance(puzzle, list):
            raise Exception("puzzle is not a list")
        self.puzzle = puzzle
        self.size = len(puzzle)

        if not isinstance(wordlist, list):
            raise Exception("wordlist is not a list")
        for word in wordlist:
            if not isinstance(word, str) or len(word) == 0:
                raise Exception("wordlist does not consist of non-empty str")
            if len(word) > self.size:
                raise Exception((
                    f"word: {word} does not fit in,",
                    f" puzzle of size {self.size}"
                ))
        self.wordlist = wordlist

        self.solution = []

    def solve(self):
        """
        Solve the wordsearch puzzle.

        Simple, brute force approach. For each position in puzzle array, check
        if its letter matches any of the words. If there's a match, look at
        each of the eight directions to check if there's a match for second
        letter. Repeat until all letters matched or there's a mismatch.
        """
        for i in range(self.size):
            for j in range(self.size):
                for word in self.wordlist:
                    if self.puzzle[i][j] == word[0]:
                        if len(word) == 0:
                            self.solution.append((word, (i, j), (0, 0)))
                        else:
                            # initiate search in 8 directions
                            result = self.__search_word((i, j), word)
                            if result is not None:
                                self.solution.append(
                                    (word, (i, j), self._pos_changes[result]))

    def __search_word(self, pos, word):
        """
        Find if a sequence of positions, starting at pos, contains the word.

        Returns the direction if the word is found, or None otherwise.
        Assumes that the word is multi-character.

        args:
        pos (tuple(int,int)): position (i,j) from which to search for the word.
        word (str): word to look for.
        """
        # no need to match first letter since we assume this for this function.
        second_letter_matches = self.__get_match_direction(pos, word[1])
        if len(second_letter_matches) == 0:
            return None  # no match
        if len(word) == 2:
            # we already matched first two letters
            return second_letter_matches[0]  # arbitrary select first direction

        for direction in second_letter_matches:
            i, j = pos
            d_i, d_j = self._pos_changes[direction]
            # start comparing at 3rd letter since we already checked first two
            i, j = i + 2 * d_i, j + 2 * d_j
            all_matched = True  # assume all letters match unless proven not to
            for word_letter in word[2:]:
                if not (0 <= i < self.size and 0 <= j < self.size):
                    all_matched = False
                    break
                if self.puzzle[i][j] != word_letter:
                    all_matched = False
                    break
                i, j = i + d_i, j + d_j
            if all_matched:
                return direction
        return None  # for all directions, no continuing matches

    def __get_match_direction(self, pos, char):
        """
        Find the direction from pos that contains char.

        Returns a list of directions or empty list if no match.
        Ignores directions that are not feasible e.g. while at edges.

        args:
        pos (tuple(int,int)): position (i,j) from which to look at the 8
            directions.
        char (str): character to look for.
        """
        i, j = pos
        matches = []
        if i != 0:
            if self.puzzle[i - 1][j] == char:
                matches.append(self._directions["N"])
            if j != self.size - 1 and self.puzzle[i - 1][j + 1] == char:
                matches.append(self._directions["NE"])
            if j != 0 and self.puzzle[i - 1][j - 1] == char:
                matches.append(self._directions["NW"])
        if i != self.size - 1:
            if self.puzzle[i + 1][j] == char:
                matches.append(self._directions["S"])
            if j != self.size - 1 and self.puzzle[i + 1][j + 1] == char:
                matches.append(self._directions["SE"])
            if j != 0 and self.puzzle[i + 1][j - 1] == char:
                matches.append(self._directions["SW"])

        if j != self.size - 1 and self.puzzle[i][j + 1] == char:
            matches.append(self._directions["E"])
        if j != 0 and self.puzzle[i][j - 1] == char:
            matches.append(self._directions["W"])

        return matches

    def print_solution(self):
        """Print where the words from wordlist are found."""
        for word, start, direction in self.solution:
            print(f"{word}: {start} -> {direction}")


if __name__ == "__main__":
    wordsearch = WordsearchGenerator(["HAPPY", "LUCKY", "APPLE"], size=15)
    wordsearch.generate_puzzle()
    solver = WordsearchSolver(wordsearch.wordsearch_arr, wordsearch.wordlist)
    solver.solve()
    solver.print_solution()
