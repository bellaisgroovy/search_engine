class IndexUpdater:
    def update_forward_index(self,forward_index: dict[str, set[str]], doc_name: str, word: str):
        if forward_index.get(doc_name) is None:
            forward_index[doc_name] = {word}
        else:
            forward_index.get(doc_name).add(word)
