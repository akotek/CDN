import unittest, random, os
from preprocessing.tokenizer import *


class TestTokenisation(unittest.TestCase):

    def __init__(self, method_name='runTest'):
        super().__init__(method_name)
        self.tokenizer = Tokenizer()

    def test_standard_tokenizer(self):
        # removes word dividers, duplications and lowercase  words
        str1 = " i'm A simp le string. . string  "

        tokens = self.tokenizer.standard_tokenizer(str1)

        self.assertEqual(5, len(tokens))  # duplications
        self.assertListEqual(["i'm", 'a', 'simp', 'le', 'string'], tokens)

    def test_standard_tokenizer_punct(self):
        # removes punctuation
        rnd1, rnd2 = random.choice(self.tokenizer.PUNCT_MARKS), random.choice(self.tokenizer.PUNCT_MARKS)
        str1 = "don$t (you) ever_5speak" + rnd1 + "^to' him! you-bad-boy" + rnd2

        tokens = self.tokenizer.standard_tokenizer(str1)

        self.assertEqual(8, len(tokens))  # typography should split words
        self.assertListEqual(['don', 't', 'you', 'ever_5speak', 'to', 'him', 'bad', 'boy'], tokens)
        self.assertTrue(all(punct not in tokens for punct in self.tokenizer.PUNCT_MARKS))

    def test_standard_tokenizer_invalid(self):
        str2 = random.randint(1, 5) * " "

        tokens = self.tokenizer.standard_tokenizer(str2)
        self.assertEqual(0, len(tokens))

    def test_keyword_tokenizer(self):
        str1 = "Kfar Saba city"

        tokens = self.tokenizer.keyword_tokenizer(str1)

        self.assertEqual(1, len(tokens))
        self.assertEqual(str1.lower(), tokens[0])

    def test_edge_ngram_tokenizer_default_params(self):
        str1 = "Quick Fox"

        tokens = self.tokenizer.edge_ngram_tokenizer(str1)

        self.assertEqual(2, len(tokens))
        self.assertListEqual(['Q', 'Qu'], tokens)

    def test_edge_ngram_tokenizer_with_params(self):
        str1 = "Quick2Brown$Fox"

        # split on digit && symbol
        tokens = self.tokenizer.edge_ngram_tokenizer(str1, min_gram=3, max_gram=7, tok_chars=["letter"])

        self.assertEqual(7, len(tokens))
        self.assertListEqual(['Qui', 'Quic', 'Quick', 'Bro', 'Brow', 'Brown', 'Fox'], tokens)

    def test_edge_ngram_tokenizer_invalid(self):
        str2 = " "  # len == 1

        tokens = self.tokenizer.edge_ngram_tokenizer(str2, min_gram=2, max_gram=2)
        self.assertEqual(0, len(tokens))

    def test_uax_url_email_tokenizer(self):
        str1 = "Email me at john.smith@global-international.com"

        tokens = self.tokenizer.uax_url_email_tokenizer(str1)

        self.assertEqual(4, len(tokens))
        self.assertListEqual(['Email', 'me', 'at', 'john.smith@global-international.com'], tokens)

    def test_uax_url_email_tokenizer_invalid(self):
        # should behave like standard tokenizer
        str1 = "Email me at john.smith.global-international.com"

        tokens = self.tokenizer.uax_url_email_tokenizer(str1)

        self.assertEqual(5, len(tokens))
        self.assertListEqual(['email', 'me', 'at', 'john.smith.global', 'international.com'], tokens)

    def test_stopwords_tokenizer(self):
        # should JUST remove stopwords without any tokenization process
        str1 = "The 2 QUICK Brown-Foxes jumped over the lazy dog's bone."

        tokens = self.tokenizer.stop_words_tokenizer(str1)

        self.assertEqual(7, len(tokens))
        self.assertListEqual(['2', 'QUICK', 'Brown-Foxes', 'jumped', 'lazy', "dog's", 'bone.'], tokens)

    def test_stopwords_tokenizer_from_file(self):
        str1 = "im awake or asleep a"

        path = os.path.join(os.path.dirname(__file__), "files\stops.txt")
        tokens = self.tokenizer.stop_words_tokenizer(str1, path, None, False)

        self.assertEqual(4, len(tokens))
        self.assertListEqual(['awake', 'or', 'asleep', 'a'], tokens)

    def test_stopwords_invalidity(self):
        str1 = random.randint(1, 5) * " "

        tokens = self.tokenizer.stop_words_tokenizer(str1)

        self.assertListEqual([""], tokens)  # strips and splits on " "


    def test_invalidity(self):
        # tests simple invalid inputs for all existing tokenizers
        funcs_list = [self.tokenizer.standard_tokenizer, self.tokenizer.edge_ngram_tokenizer,
                      self.tokenizer.uax_url_email_tokenizer]

        str1 = ""
        for func in funcs_list:

            self.assertRaises(AssertionError, func, None)

            tokens = func(str1)
            self.assertEqual(0, len(tokens))
