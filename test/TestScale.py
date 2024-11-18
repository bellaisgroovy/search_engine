import unittest
from src.Scale import Scale


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.Scale = Scale()
    def test_something(self):
        word = "hello"
        search_phrase: list[str] = [word]
        doc_name: str = "hi.txt"
        doc_rank: dict[str, float] = {doc_name: 1/100}  # there are 100 words in hi.txt
        term_freq: dict[str, dict[str, float]] = {doc_name: {word: 5/100}}  # 5/100 words in hi.txt are hello
        inv_doc_freq: dict[str, float] = {word: 1/2} # one of two documents say hello

        weight: float = self.Scale.weigh(search_phrase, doc_name, doc_rank, term_freq, inv_doc_freq)

        expected_weight: float = 0.00025
        self.assertEqual(weight, expected_weight)  # add assertion here


if __name__ == '__main__':
    unittest.main()
