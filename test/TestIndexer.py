import unittest
import os
from src.Indexer import Indexer

TESTING1212: str = "testing1212.txt"
TESTING1212_PATH: str = os.path.join("search_dir", "testing1212.txt")


class TestIndexer(unittest.TestCase):
    def setUp(self):
        self.indexer = Indexer()

    def test_index_file_first_file(self):
        forward_index: dict[str, set[str]] = {}
        invert_index: dict[str, set[str]] = {}
        term_freq: dict[str, dict[str, float]] = {}
        doc_rank: dict[str, float] = {}

        self.indexer.index_file(filename=TESTING1212,
                                filepath=TESTING1212_PATH,
                                forward_index=forward_index,
                                invert_index=invert_index,
                                term_freq=term_freq,
                                doc_rank=doc_rank)

        expected_forward_index: dict[str, set[str]] = {TESTING1212: {"high", "low", "dog", "cat", "man", "bat", "tree", "log"}}
        expected_invert_index: dict[str, set[str]] = {"high": {TESTING1212},
                                                      "low": {TESTING1212},
                                                      "dog": {TESTING1212},
                                                      "cat": {TESTING1212},
                                                      "man": {TESTING1212},
                                                      "bat": {TESTING1212},
                                                      "tree": {TESTING1212},
                                                      "log": {TESTING1212}}
        expected_term_freq: dict[str, dict[str, float]] = {TESTING1212: {"high": 3/22,
                                                                "low": 3/22,
                                                                "dog": 1/22,
                                                                "cat": 4/22,
                                                                "man": 2/22,
                                                                "bat": 1/22,
                                                                "tree": 2/22,
                                                                "log": 6/22}}
        expected_doc_rank: dict[str, float] = {TESTING1212: 1/22}

        self.assertEqual(forward_index, expected_forward_index)
        self.assertEqual(invert_index, expected_invert_index)
        self.assertEqual(term_freq, expected_term_freq)
        self.assertEqual(doc_rank, expected_doc_rank)
