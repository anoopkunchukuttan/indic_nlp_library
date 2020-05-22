# 
#  Copyright (c) 2013-present, Anoop Kunchukuttan
#  All rights reserved.
#  
#  This source code is licensed under the MIT license found in the
#  LICENSE file in the root directory of this source tree.
# 

#Program for normalization of text written in Unicode. This is mainly geared towards Indic scripts 
#
# @author Anoop Kunchukuttan 
#

import sys
from indicnlp.normalize import indic_normalize
from indicnlp.transliterate import unicode_transliterate
from indicnlp import loader

class AggressiveScriptUnifier():

    def __init__(self,common_lang='hi',nasals_mode='to_nasal_consonants'):
        self.common_lang=common_lang
        self.nasals_mode=nasals_mode
        self.do_normalize_chandras=True
        self.do_normalize_vowel_ending=True
        self.remove_nuktas=True
        self.normalizer_map={}
        self._init_normalizers()

    def _init_normalizers(self):
        normalizer_factory=indic_normalize.IndicNormalizerFactory()

        ## for languages with common parameters
        for lang in ['hi','mr','sa','kK','ne','sd','bn','gu','ta','te','kn']:
            self.normalizer_map[lang]=normalizer_factory.get_normalizer(lang, nasals_mode=self.nasals_mode, 
                    do_normalize_chandras=self.do_normalize_chandras, remove_nuktas=self.remove_nuktas,
                    do_normalize_vowel_ending=self.do_normalize_vowel_ending)

        ## for languages with language specific parameters
        self.normalizer_map['pa']=normalizer_factory.get_normalizer('pa', nasals_mode=self.nasals_mode, 
                    do_normalize_chandras=self.do_normalize_chandras, remove_nuktas=self.remove_nuktas,
                    do_normalize_vowel_ending=self.do_normalize_vowel_ending,
                    do_canonicalize_addak=True, do_canonicalize_tippi=True,
                    do_replace_vowel_bases=True)
        self.normalizer_map['or']=normalizer_factory.get_normalizer('or', nasals_mode=self.nasals_mode, 
                    do_normalize_chandras=self.do_normalize_chandras, remove_nuktas=self.remove_nuktas,
                    do_normalize_vowel_ending=self.do_normalize_vowel_ending,
                    do_remap_wa=True)
        self.normalizer_map['as']=normalizer_factory.get_normalizer('as', nasals_mode=self.nasals_mode,
                    do_normalize_chandras=self.do_normalize_chandras, remove_nuktas=self.remove_nuktas,
                    do_normalize_vowel_ending=self.do_normalize_vowel_ending,
                    do_remap_assamese_chars=True)
        self.normalizer_map['ml']=normalizer_factory.get_normalizer('ml', nasals_mode=self.nasals_mode,
                    do_normalize_chandras=self.do_normalize_chandras, remove_nuktas=self.remove_nuktas,
                    do_normalize_vowel_ending=self.do_normalize_vowel_ending,
                    do_canonicalize_chillus=True, do_correct_geminated_T=True)

    def transform(self,text,lang):
        text=self.normalizer_map[lang].normalize(text)
        text=unicode_transliterate.UnicodeIndicTransliterator.transliterate(text, lang, self.common_lang)
        return text

class BasicScriptUnifier():

    def __init__(self,common_lang='hi',nasals_mode='do_nothing'):
        self.common_lang=common_lang
        self.nasals_mode=nasals_mode
        self.normalizer_map={}
        self._init_normalizers()

    def _init_normalizers(self):
        normalizer_factory=indic_normalize.IndicNormalizerFactory()

        for lang in ['hi','mr','sa','kK','ne','sd','bn','gu','ta','te','kn','pa','or','as','ml']:
            self.normalizer_map[lang]=normalizer_factory.get_normalizer(lang, nasals_mode=self.nasals_mode)    

    def transform(self,text,lang):

        if lang in self.normalizer_map:
            text=self.normalizer_map[lang].normalize(text)

        text=unicode_transliterate.UnicodeIndicTransliterator.transliterate(text, lang, self.common_lang)
        return text

class NaiveScriptUnifier():

    def __init__(self,common_lang='hi'):
        self.common_lang=common_lang

    def transform(self,text,lang):

        text=unicode_transliterate.UnicodeIndicTransliterator.transliterate(text, lang, self.common_lang)
        return text

if __name__ == '__main__': 

    loader.load()

    if len(sys.argv)<=4:
        print("Usage: python script_unifier <command> <infile> <outfile> <language>")
        sys.exit(1)

    if sys.argv[1]=='aggressive':

        language=sys.argv[4]

        unifier=AggressiveScriptUnifier(nasals_mode='to_nasal_consonants')

        with open(sys.argv[2],'r',encoding='utf-8') as ifile:
            with open(sys.argv[3],'w',encoding='utf-8') as ofile:
                for i, line in enumerate(ifile.readlines()):

                    line=line.strip()
                    transliterated_line=unifier.transform(line,language)
                    ofile.write(transliterated_line+'\n')

    elif sys.argv[1]=='moderate':

        language=sys.argv[4]

        unifier=AggressiveScriptUnifier(nasals_mode='do_nothing')

        with open(sys.argv[2],'r',encoding='utf-8') as ifile:
            with open(sys.argv[3],'w',encoding='utf-8') as ofile:
                for i, line in enumerate(ifile.readlines()):

                    line=line.strip()
                    transliterated_line=unifier.transform(line,language)
                    ofile.write(transliterated_line+'\n')
                    
    elif sys.argv[1]=='basic':

        language=sys.argv[4]

        unifier=BasicScriptUnifier()

        with open(sys.argv[2],'r',encoding='utf-8') as ifile:
            with open(sys.argv[3],'w',encoding='utf-8') as ofile:
                for i, line in enumerate(ifile.readlines()):

                    line=line.strip()
                    transliterated_line=unifier.transform(line,language)
                    ofile.write(transliterated_line+'\n')

    elif sys.argv[1]=='naive':

        language=sys.argv[4]

        unifier=NaiveScriptUnifier()

        with open(sys.argv[2],'r',encoding='utf-8') as ifile:
            with open(sys.argv[3],'w',encoding='utf-8') as ofile:
                for i, line in enumerate(ifile.readlines()):

                    line=line.strip()
                    transliterated_line=unifier.transform(line,language)
                    ofile.write(transliterated_line+'\n')
