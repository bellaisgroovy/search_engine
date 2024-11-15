import os
from Indexer import Indexer
from Sanitizer import Sanitizer


class SearchEngine:
    def __init__(self):
        self._indexer: Indexer = Indexer()
        self._sanitizer: Sanitizer = Sanitizer()

    def crawl_folder(self, folder, forward_index, invert_index, term_freq, inv_doc_freq, doc_rank):
        """
        Crawls a given folder, and runs the indexer on each file
        """

        total_docs = 0
        for file in os.scandir(folder):
            if file.is_file():
                total_docs += 1
                self._indexer.index_file(file.name, file.path, forward_index, invert_index, term_freq, doc_rank)

        # with invert_index calculated, we can calculate the inv_doc_freq of each unique word
        # where inv_doc_freq = number of documents with the word / total number of documents
        for word in invert_index.keys():
            inv_doc_freq[word] = len(invert_index[word]) / total_docs

    def dict_to_file(self, di, fi):
        with open(fi, "w") as f:
            for key, value in di.items():
                f.write("%s:%s\n" % (key, value))

    def search(self, search_phrase, forward_index, invert_index, term_freq, inv_doc_freq, doc_rank):
        """
        For every document, you can take the product of TF and IDF
        for term of the query, and calculate their cumulative product.
        Then you multiply this value with that documents document-rank
        to arrive at a final weight for a given query, for every document.
        """

        words = self._sanitizer.parse_line(search_phrase)
        result = {}

        # TODO

        sorted_result = []
        return sorted_result

    def print_result(self, result):
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
