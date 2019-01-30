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

#Program for text written in one Indic script to another based on Unicode mappings. 
#
# @author Anoop Kunchukuttan 
#

import sys, codecs, string, itertools, re

from indicnlp import langinfo 
from indicnlp.transliterate import itrans_transliterator
from indicnlp.transliterate.sinhala_transliterator import SinhalaDevanagariTransliterator  as sdt



class UnicodeIndicTransliterator(object):
    """
    Base class for rule-based transliteration among Indian languages. 

    Script pair specific transliterators should derive from this class and override the transliterate() method. 
    They can call the super class 'transliterate()' method to avail of the common transliteration
    """

    @staticmethod
    def _correct_tamil_mapping(offset): 
        # handle missing unaspirated and voiced plosives in Tamil script 
        # replace by unvoiced, unaspirated plosives

        # for first 4 consonant rows of varnamala
        # exception: ja has a mapping in Tamil  
        if offset>=0x15 and offset<=0x28 and \
                offset!=0x1c and \
                not ( (offset-0x15)%5==0 or (offset-0x15)%5==4 )  :
            subst_char=(offset-0x15)//5
            offset=0x15+5*subst_char

        # for 5th consonant row of varnamala                         
        if offset in [ 0x2b, 0x2c, 0x2d]:
            offset=0x2a

        # 'sh' becomes 'Sh'
        if offset==0x36:
            offset=0x37

        return offset             

    @staticmethod
    def transliterate(text,lang1_code,lang2_code):
        """
        convert the source language script (lang1) to target language script (lang2)

        text: text to transliterate
        lang1_code: language 1 code 
        lang1_code: language 2 code 
        """
        if lang1_code in langinfo.SCRIPT_RANGES and lang2_code in langinfo.SCRIPT_RANGES:
            
            # if Sinhala is source, do a mapping to Devanagari first 
            if lang1_code=='si': 
                text=sdt.sinhala_to_devanagari(text)
                lang1_code='hi'

            # if Sinhala is target, make Devanagiri the intermediate target
            org_lang2_code=''
            if lang2_code=='si': 
                lang2_code='hi'
                org_lang2_code='si'

            trans_lit_text=[]
            for c in text: 
                newc=c
                offset=ord(c)-langinfo.SCRIPT_RANGES[lang1_code][0]
                if offset >=langinfo.COORDINATED_RANGE_START_INCLUSIVE and offset <= langinfo.COORDINATED_RANGE_END_INCLUSIVE:
                    if lang2_code=='ta': 
                        # tamil exceptions 
                        offset=UnicodeIndicTransliterator._correct_tamil_mapping(offset)
                    newc=chr(langinfo.SCRIPT_RANGES[lang2_code][0]+offset)

                trans_lit_text.append(newc)        

            # if Sinhala is source, do a mapping to Devanagari first 
            if org_lang2_code=='si': 
                return sdt.devanagari_to_sinhala(''.join(trans_lit_text))

            return ''.join(trans_lit_text)
        else:
            return text

class ItransTransliterator(object):
    """
    Transliterator between Indian scripts and ITRANS
    """

    @staticmethod
    def to_itrans(text,lang_code):
        if lang_code in langinfo.SCRIPT_RANGES:
            if lang_code=='ml': 
                # Change from chillus characters to corresponding consonant+halant
                text=text.replace('\u0d7a','\u0d23\u0d4d')
                text=text.replace('\u0d7b','\u0d28\u0d4d')
                text=text.replace('\u0d7c','\u0d30\u0d4d')
                text=text.replace('\u0d7d','\u0d32\u0d4d')
                text=text.replace('\u0d7e','\u0d33\u0d4d')
                text=text.replace('\u0d7f','\u0d15\u0d4d')

            devnag=UnicodeIndicTransliterator.transliterate(text,lang_code,'hi')
            
            itrans=itrans_transliterator.transliterate(devnag.encode('utf-8'), 'devanagari','itrans',
                                 {'outputASCIIEncoded' : False, 'handleUnrecognised': itrans_transliterator.UNRECOGNISED_ECHO})
            return itrans.decode('utf-8') 
        else:
            return text

    @staticmethod
    def from_itrans(text,lang_code):
        if lang_code in langinfo.SCRIPT_RANGES: 
            devnag_text=itrans_transliterator.transliterate(text.encode('utf-8'), 'itrans', 'devanagari',
                                 {'outputASCIIEncoded' : False, 'handleUnrecognised': itrans_transliterator.UNRECOGNISED_ECHO})

            lang_text=UnicodeIndicTransliterator.transliterate(devnag_text.decode('utf-8'),'hi',lang_code)
            
            return lang_text
        else:
            return text

if __name__ == '__main__': 

    if len(sys.argv)<4:
        print("Usage: python unicode_transliterate.py <command> <infile> <outfile> <src_language> <tgt_language>")
        sys.exit(1)

    if sys.argv[1]=='transliterate':

        src_language=sys.argv[4]
        tgt_language=sys.argv[5]

        with codecs.open(sys.argv[2],'r','utf-8') as ifile:
            with codecs.open(sys.argv[3],'w','utf-8') as ofile:
                for line in ifile.readlines():
                    transliterated_line=UnicodeIndicTransliterator.transliterate(line,src_language,tgt_language)
                    ofile.write(transliterated_line)

    elif sys.argv[1]=='romanize':

        language=sys.argv[4]

        ### temp fix to replace anusvara with corresponding nasal
        #r1_nasal=re.compile(ur'\u0902([\u0915-\u0918])')
        #r2_nasal=re.compile(ur'\u0902([\u091a-\u091d])')
        #r3_nasal=re.compile(ur'\u0902([\u091f-\u0922])')
        #r4_nasal=re.compile(ur'\u0902([\u0924-\u0927])')
        #r5_nasal=re.compile(ur'\u0902([\u092a-\u092d])')

        with codecs.open(sys.argv[2],'r','utf-8') as ifile:
            with codecs.open(sys.argv[3],'w','utf-8') as ofile:
                for line in ifile.readlines():
                    ### temp fix to replace anusvara with corresponding nasal
                    #line=r1_nasal.sub(u'\u0919\u094D\\1',line)
                    #line=r2_nasal.sub(u'\u091e\u094D\\1',line)
                    #line=r3_nasal.sub(u'\u0923\u094D\\1',line)
                    #line=r4_nasal.sub(u'\u0928\u094D\\1',line)
                    #line=r5_nasal.sub(u'\u092e\u094D\\1',line)

                    transliterated_line=ItransTransliterator.to_itrans(line,language)

                    ## temp fix to replace 'ph' to 'F' to match with Urdu transliteration scheme
                    transliterated_line=transliterated_line.replace('ph','f')

                    ofile.write(transliterated_line)

    elif sys.argv[1]=='indicize':

        language=sys.argv[4]

        with codecs.open(sys.argv[2],'r','utf-8') as ifile:
            with codecs.open(sys.argv[3],'w','utf-8') as ofile:
                for line in ifile.readlines():
                    transliterated_line=ItransTransliterator.from_itrans(line,language)
                    ofile.write(transliterated_line)

