import unittest
from src.IndexUpdater import IndexUpdater

DOC_NAME = ""


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.index_updater = IndexUpdater()

    def test_update_forward_index_creates_set_if_doc_entry_empty(self):
        forward_index: dict[str, set[str]] = {}
        doc_name: str = "woo_hoo.txt"
        word: str = "mum"

        self.index_updater.update_forward_index(forward_index, doc_name, word)

        expected_forward_index: dict[str, set[str]] = {doc_name: {word}}
        self.assertEqual(forward_index, expected_forward_index)

    def test_update_forward_index_adds_word_to_docs_set(self):
        doc_name: str = "woo_hoo.txt"
        word: str = "mum"
        forward_index: dict[str, set[str]] = {doc_name: {word}}
        new_word: str = "dad"

        self.index_updater.update_forward_index(forward_index, doc_name, new_word)

        expected_forward_index: dict[str, set[str]] = {doc_name: {word, new_word}}
        self.assertEqual(forward_index, expected_forward_index)

    def test_update_forward_index_adds_word_to_docs_set_many_sets(self):
        doc_name: str = "woo_hoo.txt"
        word: str = "mum"
        doc_name_2: str = "hee_haa.txt"
        forward_index: dict[str, set[str]] = {doc_name: {word}, doc_name_2: {word}}
        new_word: str = "dad"

        self.index_updater.update_forward_index(forward_index, doc_name, new_word)

        expected_forward_index: dict[str, set[str]] = {doc_name: {word, new_word}, doc_name_2: {word}}
        self.assertEqual(forward_index, expected_forward_index)

    def test_update_invert_index_creates_set_if_doc_entry_empty(self):
        invert_index: dict[str, set[str]] = {}
        doc_name: str = "woo_hoo.txt"
        word: str = "mum"

        self.index_updater.update_invert_index(invert_index, doc_name, word)

        expected_invert_index: dict[str, set[str]] = {doc_name: {word}}
        self.assertEqual(invert_index, expected_invert_index)

    def test_update_invert_index_adds_word_to_docs_set(self):
        doc_name: str = "woo_hoo.txt"
        word: str = "mum"
        invert_index: dict[str, set[str]] = {doc_name: {word}}
        new_word: str = "dad"

        self.index_updater.update_invert_index(invert_index, doc_name, new_word)

        expected_invert_index: dict[str, set[str]] = {doc_name: {word, new_word}}
        self.assertEqual(invert_index, expected_invert_index)

    def test_update_invert_index_adds_word_to_docs_set_many_sets(self):
        doc_name: str = "woo_hoo.txt"
        word: str = "mum"
        doc_name_2: str = "hee_haa.txt"
        invert_index: dict[str, set[str]] = {doc_name: {word}, doc_name_2: {word}}
        new_word: str = "dad"

        self.index_updater.update_invert_index(invert_index, doc_name, new_word)

        expected_invert_index: dict[str, set[str]] = {doc_name: {word, new_word}, doc_name_2: {word}}
        self.assertEqual(invert_index, expected_invert_index)

    def test_update_term_freq_5_words(self):
        doc_name: str = "plain_jane.xml"
        word_count: int = 5
        word_occurrences: dict[str, int] = {"hi": 1, "who": 2, "is": 1, "doctor": 1}
        term_freq: dict[str: dict[str, float]] = {doc_name: {}}

        self.index_updater.update_term_freq(term_freq, word_occurrences, word_count, doc_name)

        expected_term_freq: dict[str: dict[str, float]] = {doc_name: {"hi": 0.2,
                                                                      "who": 0.4,
                                                                      "is": 0.2,
                                                                      "doctor": 0.2}}
        self.assertEqual(term_freq, expected_term_freq)

    def test_update_term_freq_first_time_in_doc(self):
        doc_name: str = "plain_jane.xml"
        word_count: int = 5
        word_occurrences: dict[str, int] = {"hi": 1, "who": 2, "is": 1, "doctor": 1}
        term_freq: dict[str: dict[str, float]] = {}

        self.index_updater.update_term_freq(term_freq, word_occurrences, word_count, doc_name)

        expected_term_freq: dict[str: dict[str, float]] = {doc_name: {"hi": 0.2,
                                                                      "who": 0.4,
                                                                      "is": 0.2,
                                                                      "doctor": 0.2}}
        self.assertEqual(term_freq, expected_term_freq)

    def test_update_inv_doc_freq(self):
        inv_doc_freq: dict[str, float] = {}
        invert_index: dict[str, set[str]] = {"hee": {"doc1"}, "hi": {"doc1", "doc2"}, "how": {"doc1", "doc2", "doc3"}}
        total_docs: int = 3

        self.index_updater.update_inv_doc_freq(inv_doc_freq, invert_index, total_docs)

        expected_inv_doc_freq = {"hee": 1 / 3, "hi": 2 / 3, "how": 3 / 3}
        self.assertEqual(inv_doc_freq, expected_inv_doc_freq)

    def test_update_doc_rank(self):
        doc_name: str = "creeper_aw_man.mc"
        doc2_name: str = "ay.yai"
        doc_word_counts: dict[str, int] = {doc_name: 99, doc2_name: 108}
        doc_rank: dict[str, float] = {doc2_name: 1 / 108}

        self.index_updater.update_doc_rank(doc_rank, doc_word_counts, doc_name)

        expected_doc_rank: dict[str, float] = {doc_name: 1 / 99, doc2_name: 1 / 108}
        self.assertEqual(doc_rank, expected_doc_rank)


if __name__ == '__main__':
    unittest.main()
