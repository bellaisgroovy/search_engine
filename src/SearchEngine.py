import os
from src.Indexer import Indexer
from src.Sanitizer import Sanitizer
from src.Scale import Scale
from src.Cacher import Cacher


def _fill_keys_with(keys: list[str], value: float):
    """
    returns dictionary with all keys specified filled with value specified
    """
    result: dict[str, float] = {}
    for key in keys:
        result[key] = value
    return result


def _find_docs_present(search_phrase: list[str], invert_index: dict[str, set[str]]):
    """
    returns all document names where all words in search_phrase are present
    """
    docs_present: set[str] = invert_index.get(search_phrase[0]) or {}

    for word in search_phrase[1:]:
        word_docs_present = invert_index.get(word) or {}
        docs_present = docs_present.intersection(word_docs_present)

    return docs_present


def _dict_to_list(d: dict):
    """
    converts a dictionary to a list of key-value tuples
    """
    result_tuples: list[tuple[str, float]] = []

    for key in d.keys():
        result_tuples.append((key, d.get(key)))

    return result_tuples


class SearchEngine:
    def __init__(self, cacher: Cacher):
        self._indexer: Indexer = Indexer()
        self._sanitizer: Sanitizer = Sanitizer()
        self.scale: Scale = Scale()
        self.cacher: Cacher = cacher

    def crawl_folder(self,
                     folder: str,
                     forward_index: dict[str, set[str]],
                     invert_index: dict[str, set[str]],
                     term_freq: dict[str, dict[str, float]],
                     inv_doc_freq: dict[str, float],
                     doc_rank: dict[str, float]):
        """
        Crawls a given folder, and runs the indexer on each file
        """

        # check if indices are already calculated and cached for this folder
        if self._are_indices_cached(folder, forward_index, invert_index, term_freq, inv_doc_freq, doc_rank):
            return

        total_docs = 0
        for file in os.scandir(folder):
            if file.is_file():
                total_docs += 1
                self._indexer.index_file(file.name, file.path, forward_index, invert_index, term_freq, doc_rank)

        # with invert_index calculated, we can calculate the inv_doc_freq of each unique word
        # where inv_doc_freq = number of documents with the word / total number of documents
        for word in invert_index.keys():
            inv_doc_freq[word] = len(invert_index[word]) / total_docs

        self.cacher.cache(folder, forward_index, invert_index, term_freq, inv_doc_freq, doc_rank)

    def search(self,
               search_phrase: str,
               forward_index: dict[str, set[str]],
               invert_index: dict[str, set[str]],
               term_freq: dict[str, dict[str, float]],
               inv_doc_freq: dict[str, float],
               doc_rank: dict[str, float]):
        """
        For every document, you can take the product of TF and IDF
        for term of the query, and calculate their cumulative product.
        Then you multiply this value with that documents document-rank
        to arrive at a final weight for a given query, for every document.
        """
        search_phrase: list[str] = self._sanitizer.parse_line(search_phrase)

        if len(search_phrase) == 0:
            return []

        result: dict[str, float] = _fill_keys_with(keys=list(doc_rank.keys()), value=0.0)

        docs_present: set[str] = _find_docs_present(search_phrase, invert_index)

        for doc_name in docs_present:
            weight = self.scale.weigh(search_phrase,
                                      doc_name,
                                      doc_rank,
                                      term_freq.get(doc_name),
                                      inv_doc_freq)

            result[doc_name] = weight

        result_tuples: list[tuple[str, float]] = _dict_to_list(result)

        sorted_result = sorted(result_tuples, key=lambda pair: pair[1], reverse=True)
        return sorted_result

    def _are_indices_cached(self,
                            folder: str,
                            forward_index: dict[str, set[str]],
                            invert_index: dict[str, set[str]],
                            term_freq: dict[str, dict[str, float]],
                            inv_doc_freq: dict[str, float],
                            doc_rank: dict[str, float]):
        """
        If all indices are cached already for this folder, update indices and return True, otherwise return False
        """
        cached_forward_index, cached_invert_index, cached_term_freq, cached_inv_doc_freq, cached_doc_rank = self.cacher.load(
            folder)

        if cached_forward_index is not None:
            forward_index.update(cached_forward_index)
            invert_index.update(cached_invert_index)
            term_freq.update(cached_term_freq)
            inv_doc_freq.update(cached_inv_doc_freq)
            doc_rank.update(cached_doc_rank)
            return True
        else:
            return False
