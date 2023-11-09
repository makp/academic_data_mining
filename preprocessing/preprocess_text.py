"""
Run common text preprocessing steps.

Notes:
- Don't forget to download the spaCy model with conda:
  `conda install -c conda-forge spacy-model-en_core_web_sm`
"""

import re
import spacy
from gensim.models.phrases import Phrases, Phraser


"""
Regex for matching non-alphabetic characters.

The regexes below match sequences of non-alphabetic characters at the
beginning or at the end of a token. `[^a-zA-Z]` strictly matches any
character that is not an uppercase or lowercase letter from A to Z,
while `^W+` matches any character that is not a word character, which
includes not only letters but also numbers and underscores.
"""
PUNCT_RE = re.compile(r'^[^a-zA-Z]+|[^a-zA-Z]+$')  # r'^\W+|\W+$'


# Load spaCy model
nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])


# stopwords
CUSTOM_STOP_WORDS = set('would could may might account et al used also'.split(' ')) # noqa
STOP_WORDS = nlp.Defaults.stop_words.union(CUSTOM_STOP_WORDS)


class TextPreprocessor:
    """Class for preprocessing text data for NLP tasks."""

    def __init__(self):
        """Initialize the TextPreprocessor class."""
        self.phrase_model = None  # initialize model

    def train_phrase_model(self, sentences):
        """
        Train a phrase detection model using Gensim's Phrases.

        Parameters
        ----------
        sentences : list of list of str
            A list of tokenized sentences for training the phrase
            model.
        """
        self.phrase_model = Phraser(Phrases(sentences,
                                            min_count=5,
                                            threshold=10))

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
        return [word for word in tokens if word.lower() not in STOP_WORDS]

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
        return [token.lemma_ for token in nlp(" ".join(tokens))]

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

    def preprocess_text(self, text, create_bigrams=True):
        """
        Preprocesse the given text.

        Steps:
        1. Tokenizes and lemmatize the text using spaCy.
        2. Removes punctuation characters.
        3. Removes stop words
        4. Removes single characters
        5. Generates bigrams (if `create_bigrams=True`).

        Parameters
        ----------
        text : str
            The text to preprocess.
        create_bigrams : bool, optional
            Whether or not to generate bigrams (default is True).

        Returns
        -------
        list of str
            The list of preprocessed tokens (and bigrams, if
            applicable).
        """
        doc = nlp(text.lower())
        tokens = [token.text for token in doc if
                  not token.is_punct and
                  not token.is_space]
        tokens = self.remove_stop_words(tokens)
        tokens = self.lemmatize(tokens)
        tokens = self.remove_single_characters(tokens)
        if create_bigrams and self.phrase_model:
            tokens = self.phrase_model[tokens]
        return tokens