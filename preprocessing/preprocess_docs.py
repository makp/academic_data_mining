"""Common text preprocessing steps for NLP tasks."""

import re

# NLP modules
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.util import bigrams


# Regex for matching non-alphabetic characters
# This regex matches sequences of non-alphabetic characters at the
# beginning or at the end of a token
PUNCT_RE = re.compile(r'^[^a-zA-Z]+|[^a-zA-Z]+$')


# Custom stop words
WORD_STOPLIST = set('would could may might account et al used also'.split(' '))
BIGRAMS_STOPLIST = set('et_al'.split(' '))


class TextPreprocessor:
    """Class for preprocessing text data for NLP tasks."""

    def __init__(self):
        """Initialize the TextPreprocessor."""
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english')).union(WORD_STOPLIST)

    def download_nltk_data(self):
        """Download required NLTK data for preprocessing."""
        nltk.download('punkt')
        nltk.download('stopwords')
        nltk.download('wordnet')

    def lowercase_and_tokenize_text(self, text):
        """
        Tokenize and lowercase the given text.

        Parameters
        ----------
        text : str
            The text to tokenize and lowercase.

        Returns
        -------
        list of str
            The list of tokens.
        """
        return word_tokenize(text.lower())

    def is_punct(self, token):
        """Check if the given token is a punctuation character."""
        return PUNCT_RE.search(token) is not None

    def remove_punctuation(self, tokens):
        """
        Remove punctuation characters from the given list of tokens.

        Parameters
        ----------
        tokens : list of str
            The list of tokens to remove punctuation from.

        Returns
        -------
        list of str
            The list of tokens with punctuation removed.
        """
        return [token for token in tokens if not self.is_punct(token)]

    def remove_stop_words(self, tokens):
        """
        Remove stopwords from the given list of tokens.

        Parameters
        ----------
        tokens : list of str
            The list of tokens to remove stop words from.

        Returns
        -------
        list of str
            The list of tokens with stop words removed.
        """
        return [word for word in tokens if word not in self.stop_words]

    def lemmatize(self, tokens):
        """
        Lemmatize the given list of tokens.

        Parameters
        ----------
        tokens : list of str
            The list of tokens to lemmatize.

        Returns
        -------
        list of str
            The list of lemmatized tokens.
        """
        return [self.lemmatizer.lemmatize(token) for token in tokens]

    def remove_single_characters(self, tokens):
        """
        Remove single characters from the given list of tokens.

        Parameters
        ----------
        tokens : list of str
            The list of tokens to remove single characters from.

        Returns
        -------
        list of str
            The list of tokens with single characters removed.
        """
        return [token for token in tokens if len(token) > 1]

    def generate_bigrams(self, tokens):
        """
        Generate bigrams from the given list of tokens.

        Parameters
        ----------
        tokens : list of str
            The list of tokens to generate bigrams from.

        Returns
        -------
        list of str
            The list of bigrams.
        """
        return ['_'.join(bigram) for bigram in bigrams(tokens)]

    def remove_bigrams(self, tokens):
        """Remove bigrams from the given list of tokens."""
        return [token for token in tokens if token not in BIGRAMS_STOPLIST]

    def preprocess_text(self, text, create_bigrams=True):
        """
        Preprocesse the given text.

        Steps:
        1. Tokenizes and lowercases the text.
        2. Removes punctuation characters.
        3. Removes stop words
        4. Removes single characters.
        5. Lemmatizes.
        6. Generates bigrams (if bigrams=True).

        Parameters
        ----------
        text : str
            The text to preprocess.
        bigrams : bool, optional
            Whether or not to generate bigrams (default is True).

        Returns
        -------
        list of str
            The list of preprocessed tokens (and bigrams, if applicable).
        """
        tokens = self.lowercase_and_tokenize_text(text)
        tokens = self.remove_punctuation(tokens)
        tokens = self.remove_stop_words(tokens)
        tokens = self.remove_single_characters(tokens)
        tokens = self.lemmatize(tokens)
        if create_bigrams:
            b_tokens = self.generate_bigrams(tokens)
            b_tokens = self.remove_bigrams(b_tokens)
            return tokens + b_tokens
        else:
            return tokens
