def _add_to_or_create_set_entry(d: dict[str, set], index: str, new_item: str):
    if d.get(index) is None:
        d[index] = {new_item}
    else:
        d.get(index).add(new_item)


class IndexUpdater:
    def update_forward_index(self, forward_index: dict[str, set[str]], doc_name: str, word: str):
        _add_to_or_create_set_entry(forward_index, doc_name, word)

    def update_invert_index(self, invert_index: dict[str, set[str]], word: str, doc_name: str):
        _add_to_or_create_set_entry(invert_index, word, doc_name)
