_SPECIAL_CHARS = """
~`!@#$%^&*()_-+={}[]|:;'<>,./?"
"""


def _strip_special_chars(line: str):
    token = line.strip(_SPECIAL_CHARS)

    return token


def _remove_non_ascii(line: str):
    ascii_line: str = ""
    for character in line:
        if ord(character) < 128 or character == "." or character == " ":
            ascii_line += character

    return ascii_line


def _strip_specials_from_words(list_of_words: list[str]):
    '''
    removes leading and trailing special characters from each string in the list
    '''
    sanitized_list = []
    for word in list_of_words:
        word = _strip_special_chars(word)
        sanitized_list.append(word)

    return sanitized_list


def _remove_empty_words(list_of_words):
    no_empties = []
    for word in list_of_words:
        if word != "":
            no_empties.append(word)

    return no_empties


class Sanitizer:
    def parse_line(self, line: str):
        """
        Parses a given line,
        removes whitespaces, splits into list of sanitize words
        Uses sanitize_word()

        HINT: Consider using the "strip()" and "split()" function here

        """
        ascii_line: str = _remove_non_ascii(line)

        lowercase_line: str = ascii_line.lower()

        list_of_words: list[str] = lowercase_line.split()

        stripped_list: list[str] = _strip_specials_from_words(list_of_words)

        no_empty_words: list[str] = _remove_empty_words(stripped_list)

        return no_empty_words
