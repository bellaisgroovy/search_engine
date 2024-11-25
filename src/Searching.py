from src.common.Sanitizer import parse_line


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


def search(search_phrase: str,
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
