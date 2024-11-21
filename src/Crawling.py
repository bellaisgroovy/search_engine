from src.Indexer import index_file
from src.Cache import Cache
from os import scandir

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