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
        self.normalizer_map={}
        self._init_normalizers()

    def _init_normalizers(self):
        normalizer_factory=indic_normalize.IndicNormalizerFactory()

        self.normalizer_map['hi']=normalizer_factory.get_normalizer('hi', nasals_mode=self.nasals_mode)
        self.normalizer_map['bn']=normalizer_factory.get_normalizer('bn', nasals_mode=self.nasals_mode)
        self.normalizer_map['pa']=normalizer_factory.get_normalizer('pa', nasals_mode=self.nasals_mode,
                                    do_canonicalize_addak=True, do_canonicalize_tippi=True,
                                    do_replace_vowel_bases=True)
        self.normalizer_map['gu']=normalizer_factory.get_normalizer('gu', nasals_mode=self.nasals_mode)
        self.normalizer_map['or']=normalizer_factory.get_normalizer('or', nasals_mode=self.nasals_mode,
                                    do_remap_wa=True)
        self.normalizer_map['as']=normalizer_factory.get_normalizer('as', nasals_mode=self.nasals_mode,
                                    do_remap_assamese_chars=True)
        self.normalizer_map['mr']=normalizer_factory.get_normalizer('mr', nasals_mode=self.nasals_mode)
        self.normalizer_map['ta']=normalizer_factory.get_normalizer('ta', nasals_mode=self.nasals_mode)
        self.normalizer_map['te']=normalizer_factory.get_normalizer('te', nasals_mode=self.nasals_mode)
        self.normalizer_map['ml']=normalizer_factory.get_normalizer('ml', nasals_mode=self.nasals_mode,
                                                do_canonicalize_chillus=True)
        self.normalizer_map['kn']=normalizer_factory.get_normalizer('kn', nasals_mode=self.nasals_mode)

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

        self.normalizer_map['hi']=normalizer_factory.get_normalizer('hi', nasals_mode=self.nasals_mode)
        self.normalizer_map['bn']=normalizer_factory.get_normalizer('bn', nasals_mode=self.nasals_mode)
        self.normalizer_map['pa']=normalizer_factory.get_normalizer('pa', nasals_mode=self.nasals_mode)
        self.normalizer_map['gu']=normalizer_factory.get_normalizer('gu', nasals_mode=self.nasals_mode)
        self.normalizer_map['or']=normalizer_factory.get_normalizer('or', nasals_mode=self.nasals_mode)
        self.normalizer_map['as']=normalizer_factory.get_normalizer('as', nasals_mode=self.nasals_mode)
        self.normalizer_map['mr']=normalizer_factory.get_normalizer('mr', nasals_mode=self.nasals_mode)
        self.normalizer_map['ta']=normalizer_factory.get_normalizer('ta', nasals_mode=self.nasals_mode)
        self.normalizer_map['te']=normalizer_factory.get_normalizer('te', nasals_mode=self.nasals_mode)
        self.normalizer_map['ml']=normalizer_factory.get_normalizer('ml', nasals_mode=self.nasals_mode)
        self.normalizer_map['kn']=normalizer_factory.get_normalizer('kn', nasals_mode=self.nasals_mode)

    def transform(self,text,lang):

        text=self.normalizer_map[lang].normalize(text)

        text=unicode_transliterate.UnicodeIndicTransliterator.transliterate(text, lang, self.common_lang)
        return text

if __name__ == '__main__': 

    loader.load()

    if len(sys.argv)<=4:
        print("Usage: python script_unifier <command> <infile> <outfile> <language>")
        sys.exit(1)

    if sys.argv[1]=='agg_nasals':

        language=sys.argv[4]

        unifier=AggressiveScriptUnifier(nasals_mode='to_nasal_consonants')

        with open(sys.argv[2],'r',encoding='utf-8') as ifile:
            with open(sys.argv[3],'w',encoding='utf-8') as ofile:
                for i, line in enumerate(ifile.readlines()):

                    line=line.strip()
                    transliterated_line=unifier.transform(line,language)
                    ofile.write(transliterated_line+'\n')

    elif sys.argv[1]=='agg_anuvaara':

        language=sys.argv[4]

        unifier=AggressiveScriptUnifier(nasals_mode='to_anusvaara_relaxed')

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
