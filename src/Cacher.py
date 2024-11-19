import os
import pickle

_forward_index_path = "forward_index.pase"
_invert_index_path = "invert_index.pase"
_term_freq_path = "term_freq.pase"
_inv_doc_freq_path = "inv_doc_freq.pase"
_doc_rank_path = "doc_rank.pase"


class Cacher:
    def __init__(self, cache_path: str):
        self.cache_path: str = cache_path

    def cache(self,
              folder: str,
              forward_index: dict[str, set[str]],
              invert_index: dict[str, set[str]],
              term_freq: dict[str, dict[str, float]],
              inv_doc_freq: dict[str, float],
              doc_rank: dict[str, float]):

        dir_to_dump_in = os.path.join(self.cache_path, folder)
        if not os.path.exists(dir_to_dump_in):
            os.makedirs(dir_to_dump_in)

        self._dump(folder, _forward_index_path, forward_index)
        self._dump(folder, _invert_index_path, invert_index)
        self._dump(folder, _term_freq_path, term_freq)
        self._dump(folder, _inv_doc_freq_path, inv_doc_freq)
        self._dump(folder, _doc_rank_path, doc_rank)

    def load(self, folder: str):
        try:
            forward_index: dict[str, set[str]] = self._load(folder, _forward_index_path)
            invert_index: dict[str, set[str]] = self._load(folder, _invert_index_path)
            term_freq: dict[str, dict[str, float]] = self._load(folder, _term_freq_path)
            inv_doc_freq: dict[str, float] = self._load(folder, _inv_doc_freq_path)
            doc_rank: dict[str, float] = self._load(folder, _doc_rank_path)

            print("directory has been cached")
            return forward_index, invert_index, term_freq, inv_doc_freq, doc_rank
        except FileNotFoundError:
            print("directory has not been cached")
            return None, None, None, None, None

    def _dump(self, folder: str, filename: str, obj):
        path_to_dump_at = os.path.join(self.cache_path, folder, filename)
        with open(path_to_dump_at, "wb") as f:
            pickle.dump(obj, f)

    def _load(self, folder: str, filename: str):
        path_to_load_from = os.path.join(self.cache_path, folder, filename)
        with open(path_to_load_from, "rb") as f:
            obj = pickle.load(f)

            return obj
