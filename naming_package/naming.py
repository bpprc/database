"""
Naming algorithm

A best match protein and available proteins are provided in the function.
It predicts the next available name.

Xpp35Ab1
   --->   35 ---> rank1_naming [1 to 3 digits]
   --->   A  ---> rank2_naming [One uppercase letter]
   --->   b  ---> rank3_naming [One lowercase letter]
   --->   1  ---> rank4_naming [ 1 to 3 digits]
"""

import re
from typing import Iterable


def next_alphabetic_character(character):
    """
    Given an alphabet (any upper or lowercase) returns the next alphabet

    >>> next_alphabetic_character('A')
    'B'
    >>> next_alphabetic_character('a')
    'b'
    """

    return chr(ord(character) + 1)


def rank2_naming(proteins_available: Iterable[str], best_match_protein_name: str) -> str:
    """
    Given a list of proteins available as well as the best match name
    the function returns predicted name

    In this example the function extracts the first three letter pattern along with the number (it can be 3 to 5 digits)
    from the best match protein name. It filters the pattern from the proteins available.
    It also extracts the uppercase letter from the filtered patterns and finds the highest alphabet. Predict the next alphabet.
    Add the pattern 'Xpp35', predicted uppercase as well as 'a1' to get the name.

    Xpp35Ab1
       --->   pattern ---> Xpp35
       --->   Filters the pattern from the proteins available ---> ['Xpp35Aa1', 'Xpp35Ab45','Xpp35Ad1','Xpp35Ba1']
       --->   Extract all the uppercase from the filtered pattern  ---> ['A', 'A', 'A', 'B']
       --->   Find the highest alphabet ---> ['B']
       --->   Predict the next alphabet ---> by using the function next_alphabetic_character() ---> ['C']
       --->   predicted name is Xpp35+C+a1 ---> Xpp50Aa1

    >>> proteins_available = ('Xpp1Aa1', 'Xpp2Aa1', 'Xpp35Aa1', 'Xpp35Ab45',
    'Xpp35Ad1','Xpp35Ba1', 'Xpp36Aa1', 'Xpp49Aa1', 'Xpp49Ab1')

    >>> best_match_protein_name = 'Xpp35Ab1'

    >>> rank2_naming(proteins_available, best_match_protein_name)
    'Xpp35Ca1'

    """
    # extract the three-letter pattern with number Xpp35
    protein_pattern = re.search(
        r"[A-Z][a-z]{2}\d{1,3}", best_match_protein_name).group()

    # re.compile('Xpp35([A-Z])')
    base_pattern = re.compile('{}([A-Z])'.format(protein_pattern))

    # Available candidates ['A', 'A', 'A', 'B']
    candidates = []
    for name in proteins_available:
        candidate = base_pattern.search(name)
        if candidate:
            candidates.append(candidate.group(1))

    # best candidate in this example 'B'
    best_candidate = max(candidates)

    # next letter in this example 'C'
    new_letter = next_alphabetic_character(best_candidate)

    # Add the protein pattern, the next predicted letter and 'a1' at the suffix
    # predicted name Xpp35Ca1
    return f'{protein_pattern}{new_letter}a1'


def rank3_naming(proteins_available: Iterable[str], best_match_protein_name: str) -> str:
    """
    Given a list of proteins available as well as the best match name
    the function returns predicted name

    In this example the function extracts the first three letter pattern with the number (it can be 3 to 5 digits)
    and uppercase (1 letter) from the best match protein name. It filters the pattern from the proteins available.
    It also extracts the lower letter from the filtered patterns. Predict the next alphabet.
    Add the pattern 'Xpp35A', predicted lowercase as well as '1' digit to get the name.

    Xpp35Ab1
       --->   pattern ---> Xpp35A
       --->   Filters the pattern from the proteins available ---> ['Xpp35Aa1', 'Xpp35Ab45','Xpp35Ad1']
       --->   Extract all the lowercase from the filtered pattern  ---> ['a', 'b', 'd']
       --->   Find the highest alphabet ---> ['d']
       --->   Predict the next alphabet ---> by using the function next_alphabetic_character() ---> ['e']
       --->   predicted name is Xpp35+C+a1 ---> Xpp50Aa1

    >>> proteins_available = ('Xpp1Aa1', 'Xpp2Aa1', 'Xpp35Aa1', 'Xpp35Ab45',
    'Xpp35Ad1','Xpp35Ba1', 'Xpp36Aa1', 'Xpp49Aa1', 'Xpp49Ab1')

    >>> best_match_protein_name = 'Xpp35Ab1'

    >>> rank3_naming(proteins_available, best_match_protein_name)
    'Xpp35Ae1'

    """
    # extract the three-letter pattern Xpp35A from best_match_protein_name Xpp35Ab1
    protein_pattern = re.search(
        r"[A-Z][a-z]{2}\d{1,3}[A-Z]", best_match_protein_name).group()

    # re.compile('Xpp35A([a-z])')
    base_pattern = re.compile('{}([a-z])'.format(protein_pattern))

    # ['a', 'b', 'd']
    candidates = []
    for name in proteins_available:
        candidate = base_pattern.search(name)
        if candidate:
            candidates.append(candidate.group(1))

    # 'd'
    best_candidate = max(candidates)

    # 'e'
    new_letter = next_alphabetic_character(best_candidate)

    # Add the protein pattern, the next predicted letter and 'a1' at the suffix
    # Xpp35Ae1
    return f'{protein_pattern}{new_letter}1'


def rank4_naming(proteins_available: Iterable[str], best_match_protein_name: str) -> str:
    """
    Given a list of proteins available as well as the best match name
    the function returns predicted name

    In this example the function extracts the first three letter pattern with the number (it can be 3 to 5 digits),
    uppercase (1 letter) and a lowercase letter from the best match protein name. It filters the pattern from the proteins available.
    It also extracts the last digits (1 to 3) from the filtered patterns. Predict the next available lowercase name.
    Add the pattern 'Xpp35Ab' as well as '1' digit to get the name.

    Xpp35Ab1
       --->   pattern ---> Xpp35Ab
       --->   Filters the pattern from the proteins available ---> ['Xpp35Ab45']
       --->   Extract the last digits 45
       --->   Add 45 + 1 = 46
       --->   predicted name is Xpp35Ab+46 ---> Xpp35Ab46


    >>> proteins_available = ('Xpp1Aa1', 'Xpp2Aa1', 'Xpp35Aa1', 'Xpp35Ab45',
    'Xpp35Ad1','Xpp35Ba1', 'Xpp36Aa1', 'Xpp49Aa1', 'Xpp49Ab1')

    >>> best_match_protein_name = 'Xpp35Ab1'

    >>> rank4_naming(proteins_available, best_match_protein_name)
    'Xpp35Ab46'

    """
    # extract the pattern Xpp35Ab from the best_match_protein_name Xpp35Ab1
    protein_pattern = re.search(
        r"[A-Z][a-z]{2}\d{1,3}[A-Z][a-z]", best_match_protein_name).group()

    # re.compile('Xpp35Ab(\\d{1,3})')
    base_pattern = re.compile(r'{}(\d{{1,3}})'.format(protein_pattern))

    # ['45']
    candidates = []
    for name in proteins_available:
        candidate = base_pattern.search(name)
        if candidate:
            candidates.append(candidate.group(1))
    # 45
    best_candidate = int(max(candidates))

    # Add the protein pattern, the next predicted letter and 'a1' at the suffix
    # Xpp35Ab46
    return f'{protein_pattern}{best_candidate+1}'


def xpp_naming(proteins_available: Iterable[str], protein_name: str) -> str:

    # extract the three-letter pattern with number Xpp35
    # protein_pattern = re.search(r"[A-Z][a-z]{2}\d{1,3}", best_match_protein_name).group()

    # re.compile('Xpp35([A-Z])')
    base_pattern = re.compile('{}([A-Z])'.format(protein_name))

    # Available candidates ['A', 'A', 'A', 'B']
    candidates = []
    for name in proteins_available:
        candidate = base_pattern.search(name)
        if candidate:
            candidates.append(candidate.group(1))

    # best candidate in this example 'B'
    if not candidates:
        return 'Xpp'
    else:
        best_candidate = max(candidates)
        # next letter in this example 'C'
        new_letter = next_alphabetic_character(best_candidate)
        return f'{protein_pattern}{new_letter}a1'
