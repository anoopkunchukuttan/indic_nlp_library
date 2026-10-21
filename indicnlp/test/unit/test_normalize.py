import unittest

from indicnlp.normalize.indic_normalize import IndicNormalizerFactory

# lang, consonant, vowel sign, halanta, digit, visarga
SCRIPT_CHARS=[
    ('hi','क','ा','्','१','ः'),
    ('pa','ਕ','ਾ','੍','੧','ਃ'),
    ('gu','ક','ા','્','૧','ઃ'),
    ('or','କ','ା','୍','୧','ଃ'),
    ('bn','ক','া','্','১','ঃ'),
    ('ta','க','ா','்','௧','ஃ'),
    ('te','క','ా','్','౧','ః'),
    ('kn','ಕ','ಾ','್','೧','ಃ'),
    ('ml','ക','ാ','്','൧','ഃ'),
]

class TestVisarga(unittest.TestCase):

    def normalize(self,lang,text):
        return IndicNormalizerFactory().get_normalizer(lang).normalize(text)

    def test_colon_replaced(self):
        for lang,consonant,vowel_sign,_,_,visarga in SCRIPT_CHARS:
            self.assertEqual(self.normalize(lang,consonant+':'),consonant+visarga)
            self.assertEqual(self.normalize(lang,consonant+vowel_sign+':'),consonant+vowel_sign+visarga)

    def test_colon_not_replaced(self):
        for lang,consonant,_,halanta,digit,_ in SCRIPT_CHARS:
            self.assertEqual(self.normalize(lang,consonant+halanta+': '),consonant+halanta+': ')
            self.assertEqual(self.normalize(lang,digit+digit+':'+digit+digit),digit+digit+':'+digit+digit)

        self.assertEqual(self.normalize('hi','क।:'),'क।:')
        self.assertEqual(self.normalize('ml','അവൻ:'),'അവൻ:')

    def test_examples(self):
        self.assertEqual(self.normalize('te','హైదరాబాద్:'),'హైదరాబాద్:')
        self.assertEqual(self.normalize('te','అంత:'),'అంతః')
        self.assertEqual(self.normalize('hi','अत: प्राय:'),'अतः प्रायः')
        self.assertEqual(self.normalize('te','Note: అంత:'),'Note: అంతః')

if __name__ == '__main__':
    unittest.main()
