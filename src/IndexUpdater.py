def _add_item_to_dict(d: dict[str, set], index: str, new_item: str):
    if d.get(index) is None:
        d[index] = {new_item}
    else:
        d.get(index).add(new_item)


def _create_entry_if_empty(d: dict, index, new_item):
    if d.get(index) is None:
        d[index] = new_item


class IndexUpdater:
    def update_forward_index(self, forward_index: dict[str, set[str]], doc_name: str, word: str):
        _add_item_to_dict(forward_index, index=doc_name, new_item=word)

    def update_invert_index(self, invert_index: dict[str, set[str]], word: str, doc_name: str):
        _add_item_to_dict(invert_index, index=word, new_item=doc_name)

    def update_term_freq(self,
                         term_freq: dict[str, dict[str, float]],
                         word_occurrences: dict[str, int],
                         word_count: int,  # unclear if this is to be unique word count or actual word count
                         doc_name: str):

        _create_entry_if_empty(term_freq, index=doc_name, new_item={})

        for word in word_occurrences.keys():
            single_term_freq: float = word_occurrences.get(word) / word_count
            term_freq[doc_name][word] = single_term_freq

    def update_inv_doc_freq(self,
                            inv_doc_freq: dict[str, float],
                            invert_index: dict[str, set[str]],
                            total_docs: int):

        for word in invert_index.keys():
            single_inv_doc_freq = len(invert_index.get(word)) / total_docs
            inv_doc_freq[word] = single_inv_doc_freq

    def update_doc_rank(self, doc_rank: dict[str, float], word_count: int, doc_name: str):
        doc_rank[doc_name] = 1 / word_count
