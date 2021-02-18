"""
Wordsearch Solver.

By Brian Lin (brianlin@umich.edu), 2021
"""

from generate import WordsearchGenerator


class WordsearchSolver:
    """Search for words with in a square grid of characters."""

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
        self.solution = []

    def solve(self):
        """Solve the wordsearch puzzle."""
        pass

    def print_solution(self):
        """Print where the words from wordlist are found."""
        pass


if __name__ == "__main__":
    wordsearch = WordsearchGenerator(["HAPPY", "APPLE", "LUCKY"], size=5)
    solver = WordsearchSolver(wordsearch.wordsearch_arr, wordsearch.wordlist)
