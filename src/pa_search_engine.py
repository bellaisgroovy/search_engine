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
from src.SearchEngine import SearchEngine

_search_engine: SearchEngine = SearchEngine()


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
def crawl_folder(folder, forward_index, invert_index, term_freq, inv_doc_freq, doc_rank):
    _search_engine.crawl_folder(folder, forward_index, invert_index, term_freq, inv_doc_freq, doc_rank)


# %%----------------------------------------------------------------------------
def search(search_phrase, forward_index, invert_index, term_freq, inv_doc_freq, doc_rank):
    return _search_engine.search(search_phrase, forward_index, invert_index, term_freq, inv_doc_freq, doc_rank)
