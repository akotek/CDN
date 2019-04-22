import unittest, random
from preprocessing.tokenizer import *


class TestTokenisation(unittest.TestCase):

    def __init__(self, method_name='runTest'):
        super().__init__(method_name)
        self.tokenizer = Tokenizer()

    def test_standard_tokenizer(self):
        # removes word dividers, duplications and lowercase  words
        str1 = " i'm A simp le string. string  "

        tokens = self.tokenizer.standard_tokenizer(str1)

        self.assertEqual(len(str1.split()) - 1, len(tokens))  # duplications
        self.assertEqual("i'm", tokens[0])
        self.assertEqual("a", tokens[1])
        self.assertEqual("string", tokens[-1])

    def test_standard_tokenizer_punct(self):
        # removes punctuation
        rnd1, rnd2 = random.choice(self.tokenizer.PUNCT_MARKS), random.choice(self.tokenizer.PUNCT_MARKS)
        str1 = "don$t (you) ever_speak" + rnd1 + "^to' him! you-bad-boy" + rnd2

        tokens = self.tokenizer.standard_tokenizer(str1)

        self.assertEqual(7, len(tokens))  # typography should split words
        self.assertTrue(tokens[0] == "don"
                        and tokens[1] == "t"
                        and tokens[2] == "you"
                        and tokens[3] == "ever_speak"
                        and tokens[-1] == "you-bad-boy")
        self.assertTrue(all(punct not in tokens for punct in self.tokenizer.PUNCT_MARKS))

    def test_keyword_tokenizer(self):
        str1 = "Kfar Saba city"

        tokens = self.tokenizer.keyword_tokenizer(str1)

        self.assertEqual(1, len(tokens))
        self.assertEqual(str1.lower(), tokens[0])