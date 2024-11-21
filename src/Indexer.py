from timeit import default_timer as timer
from Sanitizer import parse_line
from src.IndexUpdater import IndexUpdater


class Indexer:
    def __init__(self):
        self.index_updater = IndexUpdater()

    def index_file(self,
                   filename: str,
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

                    self.index_updater.update_forward_index(forward_index, filename, word)

                    self.index_updater.update_invert_index(invert_index, word, filename)

        self.index_updater.update_term_freq(term_freq, word_occurrences, word_count, filename)

        self.index_updater.update_doc_rank(doc_rank, word_count, filename)

        end = timer()
        print("Time taken to index file: ", filename, " = ", end - start)
