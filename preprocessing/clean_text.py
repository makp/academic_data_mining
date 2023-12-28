"""Clean text."""

import html
import textacy.preprocessing as tp
from bs4 import BeautifulSoup, Comment
import spacy
import re
from symspellpy.symspellpy import SymSpell


class TextCleaner:
    """Class for cleaning text."""

    def __init__(self):
        """Initialize the TextCleaner class."""
        self.normalize_text = tp.make_pipeline(
            tp.normalize.bullet_points,
            tp.normalize.hyphenated_words,  # reattach separated by line breaks
            tp.normalize.quotation_marks,
            tp.normalize.unicode,
            tp.remove.accents)

        self.replace_from_text = tp.make_pipeline(
            tp.replace.urls,
            tp.replace.emails,
            tp.replace.phone_numbers,
            tp.replace.numbers,
            tp.replace.currency_symbols)

    def clean_html(self, text):
        """Clean HTML text."""
        text = html.unescape(text)  # convert html escape to characters

        # parse HTML
        soup = BeautifulSoup(text, 'lxml')

        # remove certain tags
        for tag in soup(["script", "style"]):
            tag.decompose()

        # remove comments
        for comment in soup.find_all(string=lambda t:
                                     isinstance(t, Comment)):
            comment.extract()  # comment doesn't have decompose() method

        # get untagged text
        text = soup.get_text()

        return text

    def clean_text(self, text, is_html=False):
        """
        Clean text.

        Main steps:
        - Normalize text
        - Replace certain types of text (e.g. URLs, emails, phone
          numbers).
        """
        if is_html:
            text = self.clean_html(text)
        text = self.normalize_text(text)
        # text = self.replace_from_text(text)
        # text = tp.normalize.whitespace(text)
        return text


class SplitTokens:
    """Class for splitting tokens."""

    def __init__(self, path_data_dict):
        """Initialize the SplitTokens class."""
        # Define alphanumeric regex pattern
        self.pattern = r"^[a-zA-Z0-9]+$"

        # Initialize SymSpell
        self.sym_spell = SymSpell()
        self.sym_spell.create_dictionary(path_data_dict)

        # Initialize spaCy model
        self.nlp = spacy.load("en_core_web_trf",
                              disable=["parser", "ner"])

    def fix_word_segmentation(self, text, max_edit_distance=0):
        """Fix word segmentation."""
        # Tokenize text with spaCy
        doc = self.nlp.make_doc(text)

        # Create list to store tokens
        lst_tokens = []

        for t in doc:
            # Check if t.text is alphanumeric
            if re.match(self.pattern, t.text):

                # Run SymSpell word segmentation
                segmented_token = self.sym_spell.word_segmentation(
                    t.text, max_edit_distance=max_edit_distance)

                # Don't correct words and only accept segments if both
                # words are in the dictionary
                if (segmented_token.corrected_string.replace(" ", "") == t.text
                    and all(part in self.sym_spell.words for
                            part in segmented_token.corrected_string.split())):

                    # Save segmented token
                    lst_tokens.append(
                        segmented_token.corrected_string + t.whitespace_)
                else:
                    lst_tokens.append(t.text + t.whitespace_)
            else:
                lst_tokens.append(t.text + t.whitespace_)

        return "".join(lst_tokens)
