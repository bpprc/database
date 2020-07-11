import re


class Search:
    def __init__(self, search_keyword):
        self.search_keyword = search_keyword

    def is_fullname(self):
        try:
            name = re.match(
                r"^[A-Z][a-z]{2}\d{1,3}[A-Z][a-z]\d{1,3}$", self.search_keyword).group()
            return True
        except:
            return False

    def is_uppercase(self):
        try:
            name = re.match(
                r"^[A-Z][a-z]{2}\d{1,3}[A-Z]$", self.search_keyword).group()
            return True
        except:
            return False

    def is_lowercase(self):
        try:
            name = re.match(
                r"^[A-Z][a-z]{2}\d{1,3}[A-Z][a-z]$", self.search_keyword).group()
            return True
        except:
            return False

    def is_single_digit(self):
        try:
            name = re.match(r"^[A-Z][a-z]{2}\d{1}$",
                            self.search_keyword).group()
            return True
        except:
            return False

    def is_double_digit(self):
        try:
            name = re.match(r"^[A-Z][a-z]{2}\d{2}$",
                            self.search_keyword).group()
            return True
        except:
            return False

    def is_triple_digit(self):
        try:
            name = re.match(r"^[A-Z][a-z]{2}\d{3}$",
                            self.search_keyword).group()
            return True
        except:
            return False

    def is_three_letter(self):
        try:
            name = re.match(r"^[A-Z][a-z]{2}$",
                            self.search_keyword).group()
            return True
        except:
            return False

    def is_three_letter_case(self):
        try:
            name = re.match(r"^[a-z][a-z]{2}$",
                            self.search_keyword).group()
            return True
        except:
            return False

    def digit_length(self):
        name = re.split('([0-9]+)', self.search_keyword)
        try:
            length_number = len(str(name[1]))
            return length_number
        except:
            pass

    def is_wildcard(self):
        if '*' in self.search_keyword:
            return True
        else:
            False


class SearchOldname():

    def __init__(self, search_keyword):
        self.search_keyword = search_keyword

    # def find_word(self):


def _sorted_nicely(l, sort_key=None):
    """ Sort the given iterable in the way that humans expect. https://blog.codinghorror.com/sorting-for-humans-natural-sort-order/ """
    def convert(text): return int(text) if text.isdigit() else text
    if sort_key is None:
        def alphanum_key(key): return [convert(c)
                                       for c in re.split('([0-9]+)', key)]
    else:
        def alphanum_key(key): return [convert(c) for c in re.split(
            '([0-9]+)', getattr(key, sort_key))]
    return sorted(l, key=alphanum_key)
