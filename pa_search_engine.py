# -*- coding: utf-8 -*-

"""
Module:
pa_search_engine

About:
Implements functions used by a directory search engine

SOME FUNCTIONS OR THEIR SKELETONS HAVE BEEN PROVIDED
HOWEVER, YOU ARE FREE TO MAKE ANY CHANGES YOU WANT IN THIS FILE
AS LONG AS IT REMAINS COMPATIBLE WITH main.py and tester.py
"""

import os
from os import scandir
import pickle
from timeit import default_timer as timer

_forward_index_path = "forward_index.pase"
_invert_index_path = "invert_index.pase"
_term_freq_path = "term_freq.pase"
_inv_doc_freq_path = "inv_doc_freq.pase"
_doc_rank_path = "doc_rank.pase"


class Cache:
    def __init__(self, cache_path: str):
        self.cache_path: str = cache_path

    def save(self,
             folder: str,
             forward_index: dict[str, set[str]],
             invert_index: dict[str, set[str]],
             term_freq: dict[str, dict[str, float]],
             inv_doc_freq: dict[str, float],
             doc_rank: dict[str, float]):

        dir_to_dump_in = os.path.join(self.cache_path, folder)

        if not os.path.exists(dir_to_dump_in):
            os.makedirs(dir_to_dump_in)

        self._dump(folder, _forward_index_path, forward_index)
        self._dump(folder, _invert_index_path, invert_index)
        self._dump(folder, _term_freq_path, term_freq)
        self._dump(folder, _inv_doc_freq_path, inv_doc_freq)
        self._dump(folder, _doc_rank_path, doc_rank)

    def load(self, folder: str):

        try:
            forward_index: dict[str, set[str]] = self._load(folder, _forward_index_path)
            invert_index: dict[str, set[str]] = self._load(folder, _invert_index_path)
            term_freq: dict[str, dict[str, float]] = self._load(folder, _term_freq_path)
            inv_doc_freq: dict[str, float] = self._load(folder, _inv_doc_freq_path)
            doc_rank: dict[str, float] = self._load(folder, _doc_rank_path)

            print(f"{folder} has been crawled before, using cached indices")

            return forward_index, invert_index, term_freq, inv_doc_freq, doc_rank

        except FileNotFoundError:

            print(f"{folder} has not been crawled before")

            return None, None, None, None, None

    def _dump(self, folder: str, filename: str, obj):

        path_to_dump_at = os.path.join(self.cache_path, folder, filename)

        with open(path_to_dump_at, "wb") as f:
            pickle.dump(obj, f)

    def _load(self, folder: str, filename: str):

        path_to_load_from = os.path.join(self.cache_path, folder, filename)

        with open(path_to_load_from, "rb") as f:
            obj = pickle.load(f)

            return obj


_SPECIAL_CHARS = """
~`!@#$%^&*()_-+={}[]|:;'<>,./?"
"""


def _strip_special_chars(line: str):
    token = line.strip(_SPECIAL_CHARS)

    return token


def _remove_non_ascii(line: str):
    ascii_line: str = ""
    for character in line:
        if ord(character) < 128 or character == "." or character == " ":
            ascii_line += character

    return ascii_line


def _strip_specials_from_words(list_of_words: list[str]):
    """
    removes leading and trailing special characters from each string in the list
    """
    sanitized_list = []
    for word in list_of_words:
        word = _strip_special_chars(word)
        sanitized_list.append(word)

    return sanitized_list


def _remove_empty_words(list_of_words):
    no_empties = []
    for word in list_of_words:
        if word != "":
            no_empties.append(word)

    return no_empties


def parse_line(line: str):
    """
    Parses a given line,
    removes whitespaces, splits into list of sanitize words
    Uses sanitize_word()

    HINT: Consider using the "strip()" and "split()" function here

    """
    ascii_line: str = _remove_non_ascii(line)

    lowercase_line: str = ascii_line.lower()

    list_of_words: list[str] = lowercase_line.split()

    stripped_list: list[str] = _strip_specials_from_words(list_of_words)

    no_empty_words: list[str] = _remove_empty_words(stripped_list)

    return no_empty_words


def _add_item_to_dict(d: dict[str, set], index: str, new_item: str):
    if d.get(index) is None:
        d[index] = {new_item}
    else:
        d.get(index).add(new_item)


def _create_entry_if_empty(d: dict, index, new_item):
    d[index] = d.get(index) or new_item


def update_forward_index(forward_index: dict[str, set[str]], doc_name: str, word: str):
    _add_item_to_dict(forward_index, index=doc_name, new_item=word)


def update_invert_index(invert_index: dict[str, set[str]], word: str, doc_name: str):
    _add_item_to_dict(invert_index, index=word, new_item=doc_name)


def update_term_freq(term_freq: dict[str, dict[str, float]],
                     word_occurrences: dict[str, int],
                     word_count: int,  # unclear if this is to be unique word count or actual word count
                     doc_name: str):
    _create_entry_if_empty(term_freq, index=doc_name, new_item={})

    for word in word_occurrences.keys():
        single_term_freq: float = word_occurrences.get(word) / word_count
        term_freq[doc_name][word] = single_term_freq


def update_inv_doc_freq(inv_doc_freq: dict[str, float],
                        invert_index: dict[str, set[str]],
                        total_docs: int):
    for word in invert_index.keys():
        single_inv_doc_freq = len(invert_index.get(word)) / total_docs
        inv_doc_freq[word] = single_inv_doc_freq


def update_doc_rank(doc_rank: dict[str, float], word_count: int, doc_name: str):
    doc_rank[doc_name] = 1 / word_count


def index_file(filename: str,
               filepath: str,
               forward_index: dict[str, set[str]],
               invert_index: dict[str, set[str]],
               term_freq: dict[str, dict[str, float]],
               doc_rank: dict[str, float]):
    """
    Given a file, indexes it by calculating its:
        forward_index
        term_freq
        doc_rank
        and updates the invert_index (which is calculated across all files)
    """
    start = timer()

    word_count: int = 0

    word_occurrences: dict[str, int] = {}

    with open(filepath, 'r', encoding="utf-8") as file:
        for line in file:

            list_of_words: list[str] = parse_line(line)

            for word in list_of_words:
                word_count += 1

                # if no entry for word yet sets to 0 then increments
                word_occurrences[word] = word_occurrences.get(word) or 0
                word_occurrences[word] = word_occurrences.get(word) + 1

                update_forward_index(forward_index, filename, word)

                update_invert_index(invert_index, word, filename)

    update_term_freq(term_freq, word_occurrences, word_count, filename)

    update_doc_rank(doc_rank, word_count, filename)

    end = timer()
    print("Time taken to index file: ", filename, " = ", end - start)


_cache_path = "cache"
_cache: Cache = Cache(_cache_path)


def _are_indices_cached(folder: str,
                        forward_index: dict[str, set[str]],
                        invert_index: dict[str, set[str]],
                        term_freq: dict[str, dict[str, float]],
                        inv_doc_freq: dict[str, float],
                        doc_rank: dict[str, float]):
    """
    If all indices are cached already for this folder, update indices and return True, otherwise return False
    """
    cached_forward_index, cached_invert_index, cached_term_freq, cached_inv_doc_freq, cached_doc_rank = _cache.load(
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


def _weigh(search_phrase: list[str],
           doc_name: str,
           doc_rank: dict[str, float],
           doc_term_freq: dict[str, float],
           inv_doc_freq: dict[str, float]):
    weight: float = doc_rank.get(doc_name)

    for word in search_phrase:
        word_weight: float = doc_term_freq.get(word) * inv_doc_freq.get(word)

        weight = weight * word_weight

    return weight


def _dict_to_list(d: dict):
    """
    converts a dictionary to a list of key-value tuples
    """
    result_tuples: list[tuple[str, float]] = []

    for key in d.keys():
        result_tuples.append((key, d.get(key)))

    return result_tuples


# %%----------------------------------------------------------------------------
def dict_to_file(di, fi):
    with open(fi, "w") as f:
        for key, value in di.items():
            f.write("%s:%s\n" % (key, value))


# %%----------------------------------------------------------------------------
def print_result(result):
    """
            Print result (all docs with non-zero weights)
    """
    print("# Search Results:")
    count = 0
    for val in result:
        if val[1] > 0:
            print(val[0])
            count += 1
    print(count, " results returned")


# %%----------------------------------------------------------------------------
def crawl_folder(folder: str,
                 forward_index: dict[str, set[str]],
                 invert_index: dict[str, set[str]],
                 term_freq: dict[str, dict[str, float]],
                 inv_doc_freq: dict[str, float],
                 doc_rank: dict[str, float]):
    """
    Crawls a given folder, and runs the indexer on each file
    """

    # check if indices are already calculated and cached for this folder
    if _are_indices_cached(folder, forward_index, invert_index, term_freq, inv_doc_freq, doc_rank):
        return

    total_docs = 0
    for file in scandir(folder):
        if file.is_file():
            total_docs += 1
            index_file(file.name, file.path, forward_index, invert_index, term_freq, doc_rank)

    # with invert_index calculated, we can calculate the inv_doc_freq of each unique word
    # where inv_doc_freq = number of documents with the word / total number of documents
    for word in invert_index.keys():
        inv_doc_freq[word] = len(invert_index[word]) / total_docs

    _cache.save(folder, forward_index, invert_index, term_freq, inv_doc_freq, doc_rank)


# %%----------------------------------------------------------------------------
def search(search_phrase, forward_index, invert_index, term_freq, inv_doc_freq, doc_rank):
    """
        For every document, you can take the product of TF and IDF
        for term of the query, and calculate their cumulative product.
        Then you multiply this value with that documents document-rank
        to arrive at a final weight for a given query, for every document.
    """
    search_phrase: list[str] = parse_line(search_phrase)

    if len(search_phrase) == 0:
        return []

    result: dict[str, float] = _fill_keys_with(keys=list(doc_rank.keys()), value=0.0)

    docs_present: set[str] = _find_docs_present(search_phrase, invert_index)

    for doc_name in docs_present:
        weight = _weigh(search_phrase,
                        doc_name,
                        doc_rank,
                        term_freq.get(doc_name),
                        inv_doc_freq)

        result[doc_name] = weight

    result_tuples: list[tuple[str, float]] = _dict_to_list(result)

    sorted_result = sorted(result_tuples, key=lambda pair: pair[1], reverse=True)
    return sorted_result
