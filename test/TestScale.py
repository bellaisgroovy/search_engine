import unittest
from src.Scale import weigh


class MyTestCase(unittest.TestCase):
    def test_weigh(self):
        word = "hello"
        search_phrase: list[str] = [word]
        doc_name: str = "hi.txt"
        doc_rank: dict[str, float] = {doc_name: 1/100}  # there are 100 words in hi.txt
        term_freq: dict[str, float] = {word: 5/100}  # 5/100 words in hi.txt are hello
        inv_doc_freq: dict[str, float] = {word: 1/2} # one of two documents say hello

        weight: float = weigh(search_phrase, doc_name, doc_rank, term_freq, inv_doc_freq)

        expected_weight: float = 0.00025
        self.assertEqual(weight, expected_weight)  # add assertion here


if __name__ == '__main__':
    unittest.main()
