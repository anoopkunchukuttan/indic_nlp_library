# Copyright Anoop Kunchukuttan 2013 - present
#
# This file is part of Indic NLP Library.
# 
# Indic NLP Library is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# Indic NLP Library is distributed in the hope that it will be useful,
#        but WITHOUT ANY WARRANTY; without even the implied warranty of
#        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#        GNU General Public License for more details.
# 
#        You should have received a copy of the GNU General Public License
#        along with Indic NLP Library.  If not, see <http://www.gnu.org/licenses/>.
#

#Program for normalization of text written in Unicode. This is mainly geared towards Indic scripts 
#
# @author Anoop Kunchukuttan 
#

class AggressiveScriptUnifier():

    def __init__(self,common_lang'hi',nasals_mode='to_nasal_consonants'):
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
        SElf.normalizer_map['or']=normalizer_factory.get_normalizer('or', nasals_mode=self.nasals_mode,
                                    do_remap_wa=True)
        self.normalizer_map['as']=normalizer_factory.get_normalizer('as', nasals_mode=self.nasals_mode,
                                    do_remap_assamese_chars=True)
        self.normalizer_map['mr']=normalizer_factory.get_normalizer('mr', nasals_mode=self.nasals_mode)
        self.normalizer_map['ta']=normalizer_factory.get_normalizer('ta', nasals_mode=self.nasals_mode)
        self.normalizer_map['te']=normalizer_factory.get_normalizer('te', nasals_mode=self.nasals_mode)
        self.normalizer_map['ml']=normalizer_factory.get_normalizer('ml', nasals_mode=self.nasals_mode,
                                                do_canonicalize_chillus=True)
        self.normalizer_map['kn']=normalizer_factory.get_normalizer('kn', nasals_mode=self.nasals_mode)

    def transform(text,lang):

        text=self.normalizer_map[lang].normalize(text)

        text=unicode_transliterate.UnicodeIndicTransliterator.transliterate(text, lang, common_lang)
	return text 

if __name__ == '__main__': 

    if len(sys.argv)<=4:
        print("Usage: python script_unifier <command> <infile> <outfile> <language>")
        sys.exit(1)

    if sys.argv[1]=='agg':

        language=sys.argv[4]

        unifier=AggresiveScriptUnifier()

        with codecs.open(sys.argv[2],'r','utf-8') as ifile:
            with codecs.open(sys.argv[3],'w','utf-8') as ofile:
                for line in ifile.readlines():
                    transliterated_line=unifier.normalize(line,language)
                    ofile.write(transliterated_line)
