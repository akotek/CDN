import unittest
from preprocessing.stem.porterstemmer import *


class TestStemmer(unittest.TestCase):

    def __init__(self, method_name='runTest'):
        super().__init__(method_name)
        self.stemmer = PorterStemmer()

    def test_porter_stemmer(self):
        plurals = ['caresses', 'flies', 'dies', 'mules', 'denied', 'died', 'agreed', 'owned',
                   'humbled', 'sized', 'meeting', 'stating', 'siezing', 'itemization', 'sensational',
                   'traditional', 'reference', 'colonizer', 'plotted']

        singles = [self.stemmer.stem(plural) for plural in plurals]

        self.assertEqual(19, len(singles))
        self.assertListEqual(['caress', 'fli', 'die', 'mule', 'deni', 'die', 'agre', 'own', 'humbl', 'size',
                              'meet', 'state', 'siez', 'item', 'sensat', 'tradit', 'refer', 'colon', 'plot'],
                             singles)
