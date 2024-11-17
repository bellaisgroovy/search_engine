import unittest
from src.IndexUpdater import IndexUpdater

DOC_NAME = ""


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.index_updater = IndexUpdater()

    def test_creates_set_if_doc_entry_empty(self):
        forward_index: dict[str, set[str]] = {}
        doc_name: str = "woo_hoo.txt"
        word: str = "mum"

        self.index_updater.update_forward_index(forward_index, doc_name, word)

        expected_forward_index: dict[str, set[str]] = {doc_name: {word}}
        self.assertEqual(forward_index, expected_forward_index)

    def test_adds_word_to_docs_set(self):
        doc_name: str = "woo_hoo.txt"
        word: str = "mum"
        forward_index: dict[str, set[str]] = {doc_name: {word}}
        new_word: str = "dad"

        self.index_updater.update_forward_index(forward_index, doc_name, new_word)

        expected_forward_index: dict[str, set[str]] = {doc_name: {word, new_word}}
        self.assertEqual(forward_index, expected_forward_index)

    def test_adds_word_to_docs_set_many_sets(self):
        doc_name: str = "woo_hoo.txt"
        word: str = "mum"
        doc_name_2: str = "hee_haa.txt"
        forward_index: dict[str, set[str]] = {doc_name: {word}, doc_name_2: {word}}
        new_word: str = "dad"

        self.index_updater.update_forward_index(forward_index, doc_name, new_word)

        expected_forward_index: dict[str, set[str]] = {doc_name: {word, new_word}, doc_name_2: {word}}
        self.assertEqual(forward_index, expected_forward_index)


if __name__ == '__main__':
    unittest.main()
