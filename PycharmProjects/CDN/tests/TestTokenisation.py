import unittest, random
from preprocessing.Tokenizer import *


class TestTokenisation(unittest.TestCase):

    def __init__(self, method_name='runTest'):
        super().__init__(method_name)
        self.tokenizer = Tokenizer()

    def test_standard_tokenization(self):
        # removes word dividers, duplications and lowercase  words
        str1 = " i'm A simp le string. string  "

        tokenized = self.tokenizer.standard_tokenizer(str1)

        self.assertEqual(len(str1.split()) - 1, len(tokenized))  # duplications
        self.assertEqual("i'm", tokenized[0])
        self.assertEqual("a", tokenized[1])
        self.assertEqual("string", tokenized[-1])

    def test_tokenization_punct(self):
        # removes punctuation
        rnd1, rnd2 = random.choice(self.tokenizer.PUNCT_MARKS), random.choice(self.tokenizer.PUNCT_MARKS)
        str1 = "don$t (you) ever_speak" + rnd1 + "^to' him! you-bad-boy" + rnd2

        tokenized = self.tokenizer.standard_tokenizer(str1)

        self.assertEqual(7, len(tokenized))     # typography should split words
        self.assertTrue(tokenized[0] == "don"
                        and tokenized[1] == "t"
                        and tokenized[2] == "you"
                        and tokenized[3] == "ever_speak"
                        and tokenized[-1] == "you-bad-boy")
        self.assertTrue(all(punct not in tokenized for punct in self.tokenizer.PUNCT_MARKS))
