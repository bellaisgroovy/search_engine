from timeit import default_timer as timer
from src.common.Sanitizer import parse_line
from src.crawling.IndexUpdater import update_invert_index, update_forward_index, update_term_freq, update_doc_rank


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
