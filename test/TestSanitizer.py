import unittest
from src.common.Sanitizer import parse_line


class TestSanitizer(unittest.TestCase):

    def test_removes_non_ascii(self):
        actual_line = parse_line("日本人 中國的 ascii characters")
        self.assertEqual(["ascii", "characters"], actual_line)

    def test_removes_capitals(self):
        actual_line = parse_line("I AM very ANGRY")
        self.assertEqual(["i", "am", "very", "angry"], actual_line)

    def test_removes_whitespace(self):
        actual_line = parse_line("    i   declare the  eeee wo hooo       a      - to    ")
        self.assertEqual(["i", "declare", "the", "eeee", "wo", "hooo", "a", "to"], actual_line)

    def test_removes_only_leading_trailing_special_chars(self):
        actual_line = parse_line("""
        ~`!@#$%^&*()_-+={}[]|:;'<>,.?/ ..._&*()__...anna_kerenina.txt...___()_-+={}[]|:;'<>,.?  )_-+="
        """)
        self.assertEqual(["anna_kerenina.txt"], actual_line)

    def test_returns_list(self):
        actual_line = parse_line("hi")
        self.assertEqual(["hi"], actual_line)


if __name__ == '__main__':
    unittest.main()
