import re

from preprocessing.tokenize.stand import StandardTokenizer


class UAXEmailTokenizer(StandardTokenizer):

    def tokenize(self, s: str) -> list:
        # The uax_url_email tokenizer is like the stand.py tokenizer except that
        # it recognises URLs and email addresses as single tokens.

        # "Email me at john.smith@global-international.com"
        # >> [ Email, me, at, john.smith@global-international.com ]
        # while stand.py tokenizer >> [ email, me, at, john.smith, global, international.com ]

        if not re.findall(self.REGEX_EMAIL, s):
            return super().tokenize(s)

        self._word_divider, self._meaningful_puncts = self._get_dividers()
        return self._general_tokenizer(s)

    def _get_dividers(self):
        return list(filter(lambda s: s not in ['@', '-', '.'], self.WORD_DIVIDERS)), self.MEANINGFUL_PUNCTS + ['@', '-']