import unittest
import os
from src.Indexer import Indexer

TESTING1212: str = "testing1212.txt"
TESTING1212_PATH: str = os.path.join("search_dir", TESTING1212)

CHILLI: str = "chilli.txt"
CHILLI_PATH: str = os.path.join("search_dir", CHILLI)

post_testing_forward_index: dict[str, set[str]] = {
    TESTING1212: {"high", "low", "dog", "cat", "man", "bat", "tree", "log"}}
post_testing_invert_index: dict[str, set[str]] = {"high": {TESTING1212},
                                                  "low": {TESTING1212},
                                                  "dog": {TESTING1212},
                                                  "cat": {TESTING1212},
                                                  "man": {TESTING1212},
                                                  "bat": {TESTING1212},
                                                  "tree": {TESTING1212},
                                                  "log": {TESTING1212}}
post_testing_term_freq: dict[str, dict[str, float]] = {TESTING1212: {"high": 3 / 22,
                                                                     "low": 3 / 22,
                                                                     "dog": 1 / 22,
                                                                     "cat": 4 / 22,
                                                                     "man": 2 / 22,
                                                                     "bat": 1 / 22,
                                                                     "tree": 2 / 22,
                                                                     "log": 6 / 22}}
post_testing_doc_rank: dict[str, float] = {TESTING1212: 1 / 22}


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

        self.assertEqual(forward_index, post_testing_forward_index)
        self.assertEqual(invert_index, post_testing_invert_index)
        self.assertEqual(term_freq, post_testing_term_freq)
        self.assertEqual(doc_rank, post_testing_doc_rank)

    def test_index_file_second_file(self):
        forward_index = post_testing_forward_index
        invert_index = post_testing_invert_index
        term_freq = post_testing_term_freq
        doc_rank = post_testing_doc_rank

        self.indexer.index_file(filename=CHILLI,
                                filepath=CHILLI_PATH,
                                forward_index=forward_index,
                                invert_index=invert_index,
                                term_freq=term_freq,
                                doc_rank=doc_rank)

        expected_forward_index: dict[str, set[str]] = {
            TESTING1212: {"high", "low", "dog", "cat", "man", "bat", "tree", "log"},
            CHILLI: {"ouch", "hot", "eek", "yowza", "bat", "man", "low", "log"}}
        expected_invert_index: dict[str, set[str]] = {"high": {TESTING1212},
                                                      "low": {TESTING1212, CHILLI},
                                                      "dog": {TESTING1212},
                                                      "cat": {TESTING1212},
                                                      "man": {TESTING1212, CHILLI},
                                                      "bat": {TESTING1212, CHILLI},
                                                      "tree": {TESTING1212},
                                                      "log": {TESTING1212, CHILLI},
                                                      "ouch": {CHILLI},
                                                      "eek": {CHILLI},
                                                      "hot": {CHILLI},
                                                      "yowza": {CHILLI}}
        expected_term_freq: dict[str, dict[str, float]] = {TESTING1212: {"high": 3 / 22,
                                                                         "low": 3 / 22,
                                                                         "dog": 1 / 22,
                                                                         "cat": 4 / 22,
                                                                         "man": 2 / 22,
                                                                         "bat": 1 / 22,
                                                                         "tree": 2 / 22,
                                                                         "log": 6 / 22},
                                                           CHILLI: {"ouch": 1 / 10,
                                                                    "hot": 3 / 10,
                                                                    "eek": 1 / 10,
                                                                    "yowza": 1 / 10,
                                                                    "bat": 1 / 10,
                                                                    "man": 1 / 10,
                                                                    "low": 1 / 10,
                                                                    "log": 1 / 10}}
        expected_doc_rank: dict[str, float] = {TESTING1212: 1 / 22, CHILLI: 1 / 10}

        self.assertEqual(forward_index, expected_forward_index)
        self.assertEqual(invert_index, expected_invert_index)
        self.assertEqual(term_freq, expected_term_freq)
        self.assertEqual(doc_rank, expected_doc_rank)
