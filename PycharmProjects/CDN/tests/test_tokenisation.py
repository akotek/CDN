import unittest, random, os, filecmp
from preprocessing.tokenize.stand import StandardTokenizer
from preprocessing.tokenize.keyword import KeywordTokenizer
from preprocessing.tokenize.ngram import NGramTokenizer
from preprocessing.tokenize.stops import StopwordsTokenizer
from preprocessing.tokenize.tokenizer import Tokenizer
from preprocessing.tokenize.uax import UAXEmailTokenizer


class TestTokenize(unittest.TestCase):

    def test_standard_tokenizer(self):

        tokenizer = StandardTokenizer()
        str1 = " i'm A simp le string. . string  "
        tokens = tokenizer.tokenize(str1)
        self.assertEqual(6, len(tokens))
        self.assertListEqual(["i'm", 'a', 'simp', 'le', 'string', 'string'], tokens)

    @unittest.skip
    def test_standard_tokenizer_edge_cases(self):

        tokenizer = StandardTokenizer()
        str1 = ".69 .d a.b.c 65.3 c. 65-3"
        tokens = tokenizer.tokenize(str1)
        self.assertEqual(5, len(tokens))
        self.assertListEqual(['69', 'd', 'a.b.c', '65.3', 'c'], tokens)

    def test_standard_tokenizer_invalid(self):

        tokenizer = StandardTokenizer()
        str1 = random.randint(1, 5) * " "
        tokens = tokenizer.tokenize(str1)
        self.assertEqual(0, len(tokens))

    def test_standard_tokenizer_punct(self):

        # removes punctuation
        tokenizer = StandardTokenizer()
        rnd1, rnd2 = random.choice(tokenizer.PUNCT_MARKS), random.choice(tokenizer.PUNCT_MARKS)
        str1 = "don$t (you) ever_5speak" + rnd1 + "^to' him! you-bad-boy" + rnd2
        tokens = tokenizer.tokenize(str1)
        self.assertEqual(9, len(tokens))  # typography should split words
        self.assertListEqual(['don', 't', 'you', 'ever_5speak', 'to', 'him', 'you', 'bad', 'boy'], tokens)
        self.assertTrue(all(punct not in tokens for punct in Tokenizer.PUNCT_MARKS))

    def test_keyword_tokenizer(self):

        tokenizer = KeywordTokenizer()
        str1 = "Kfar Saba city"
        tokens = tokenizer.tokenize(str1)
        self.assertEqual(1, len(tokens))
        self.assertEqual(str1.lower(), tokens[0])

    def test_edge_ngram_tokenizer_default_params(self):

        tokenizer = NGramTokenizer()
        str1 = "Quick Fox"
        tokens = tokenizer.tokenize(str1, edges=True)
        self.assertEqual(2, len(tokens))
        self.assertListEqual(['Q', 'Qu'], tokens)

    def test_edge_ngram_tokenizer_with_params(self):

        tokenizer = NGramTokenizer()
        str1 = "Quick2Brown$Fox"
        # split on digit && symbol
        tokens = tokenizer.tokenize(str1, min_gram=3, max_gram=7, tok_chars=["letter"], edges=True)
        self.assertEqual(7, len(tokens))
        self.assertListEqual(['Qui', 'Quic', 'Quick', 'Bro', 'Brow', 'Brown', 'Fox'], tokens)

    def test_edge_ngram_tokenizer_invalid(self):

        tokenizer = NGramTokenizer()
        str2 = " "  # len == 1
        tokens = tokenizer.tokenize(str2, min_gram=2, max_gram=2, edges=True)
        self.assertEqual(0, len(tokens))

    def test_uax_url_email_tokenizer(self):

        tokenizer = UAXEmailTokenizer()
        str1 = "Email me at john.smith@global-international.com"
        tokens = tokenizer.tokenize(str1)
        self.assertEqual(4, len(tokens))
        self.assertListEqual(['email', 'me', 'at', 'john.smith@global-international.com'], tokens)

    def test_uax_url_email_tokenizer_invalid(self):

        # should behave like standard tokenizer
        tokenizer = UAXEmailTokenizer()
        str1 = "Email me at john.smith.global-international.com"
        tokens = tokenizer.tokenize(str1)
        self.assertEqual(5, len(tokens))
        self.assertListEqual(['email', 'me', 'at', 'john.smith.global', 'international.com'], tokens)

    def test_stopwords_tokenizer(self):

        # should JUST remove stopwords without any tokenize process
        tokenizer = StopwordsTokenizer()
        str1 = "The 2 QUICK Brown-Foxes jumped over the lazy dog's bone."
        tokens = tokenizer.tokenize(str1)
        self.assertEqual(7, len(tokens))
        self.assertListEqual(['2', 'QUICK', 'Brown-Foxes', 'jumped', 'lazy', "dog's", 'bone.'], tokens)

    def test_stopwords_tokenizer_from_file(self):

        tokenizer = StopwordsTokenizer()
        str1 = "im awake or asleep a"
        path = os.path.join(os.path.dirname(__file__), "files\\tokenize\stops.txt")
        tokens = tokenizer.tokenize(str1, sw_file=path, stops=None, rmv_trail=False)
        self.assertEqual(4, len(tokens))
        self.assertListEqual(['awake', 'or', 'asleep', 'a'], tokens)

    def test_stopwords_invalidity(self):

        tokenizer = StopwordsTokenizer()
        str1 = random.randint(1, 5) * " "
        tokens = tokenizer.tokenize(str1)
        self.assertListEqual([""], tokens)  # strips and splits on " "

    @unittest.skip("remove after edge cases is fixed")
    def test_tokenization_on_file(self):

        tokenizer = StandardTokenizer()
        fp = os.path.join(os.path.dirname(__file__), "files\\tokenize\\")
        with open(fp + "before", 'r') as f, open(fp + "after", 'w') as w:
            for line in f:
                for tok in tokenizer.tokenize(line):
                    w.write(tok + "\n")
        self.assertTrue(filecmp.cmp(fp + "es_output", fp + "after"))

    def test_invalidity(self):

        tokenizers = [StandardTokenizer(), NGramTokenizer(), UAXEmailTokenizer()]
        str1 = ""
        for tokenizer in tokenizers:
            tokens = tokenizer.tokenize(str1)
            self.assertEqual(0, len(tokens))
