class Scale:
    def weigh(self,
              search_phrase: list[str],
              doc_name: str,
              doc_rank: dict[str, float],
              doc_term_freq: dict[str, float],
              inv_doc_freq: dict[str, float]):

        weight: float = doc_rank.get(doc_name)

        for word in search_phrase:

            word_weight: float = doc_term_freq.get(word) * inv_doc_freq.get(word)

            weight = weight * word_weight

        return weight
