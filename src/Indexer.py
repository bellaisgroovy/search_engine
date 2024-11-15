from timeit import default_timer as timer


class Indexer:
    def index_file(self, filename, filepath, forward_index, invert_index, term_freq, doc_rank):
        """
        Given a file, indexes it by calculating its:
            forward_index
            term_freq
            doc_rank
            and updates the invert_index (which is calculated across all files)
        """
        start = timer()
        with open(filepath, 'r', encoding="utf-8") as f:
            pass
        # TODO

        end = timer()
        print("Time taken to index file: ", filename, " = ", end - start)
