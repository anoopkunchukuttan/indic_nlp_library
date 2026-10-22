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
            self.assertEqual(self.normalize(lang,consonant+':'+consonant),consonant+visarga+consonant)
            self.assertEqual(self.normalize(lang,consonant+vowel_sign+':'+consonant),consonant+vowel_sign+visarga+consonant)

    def test_colon_not_replaced(self):
        for lang,consonant,vowel_sign,halanta,digit,_ in SCRIPT_CHARS:
            self.assertEqual(self.normalize(lang,consonant+':'),consonant+':')
            self.assertEqual(self.normalize(lang,consonant+vowel_sign+': '+consonant),consonant+vowel_sign+': '+consonant)
            self.assertEqual(self.normalize(lang,consonant+halanta+':'+consonant),consonant+halanta+':'+consonant)
            self.assertEqual(self.normalize(lang,digit+digit+':'+digit+digit),digit+digit+':'+digit+digit)

        self.assertEqual(self.normalize('hi','क।:क'),'क।:क')

    def test_examples(self):
        self.assertEqual(self.normalize('te','హైదరాబాద్:'),'హైదరాబాద్:')
        self.assertEqual(self.normalize('ml','ദു:ഖം'),'ദുഃഖം')
        self.assertEqual(self.normalize('ml','കാവ്യ പറഞ്ഞു: "ഇതു നല്ലതാണ്"'),'കാവ്യ പറഞ്ഞു: "ഇതു നല്ലതാണ്"')
        self.assertEqual(self.normalize('hi','अंत:करण'),'अंतःकरण')
        self.assertEqual(self.normalize('hi','उसने कहा: "ठीक है"'),'उसने कहा: "ठीक है"')
        self.assertEqual(self.normalize('te','Note: దు:ఖం'),'Note: దుఃఖం')

if __name__ == '__main__':
    unittest.main()
