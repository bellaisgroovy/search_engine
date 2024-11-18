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
    _search_engine.dict_to_file(di, fi)


# %%----------------------------------------------------------------------------
def print_result(result):
    _search_engine.print_result(result)


# %%----------------------------------------------------------------------------
def crawl_folder(folder, forward_index, invert_index, term_freq, inv_doc_freq, doc_rank):
    _search_engine.crawl_folder(folder, forward_index, invert_index, term_freq, inv_doc_freq, doc_rank)


# %%----------------------------------------------------------------------------
def search(search_phrase, forward_index, invert_index, term_freq, inv_doc_freq, doc_rank):
    return _search_engine.search(search_phrase, forward_index, invert_index, term_freq, inv_doc_freq, doc_rank)
