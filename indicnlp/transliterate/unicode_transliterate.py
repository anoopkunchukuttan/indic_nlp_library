# 
#  Copyright (c) 2013-present, Anoop Kunchukuttan
#  All rights reserved.
#  
#  This source code is licensed under the MIT license found in the
#  LICENSE file in the root directory of this source tree.
#  

#Program for text written in one Indic script to another based on Unicode mappings. 
#
# @author Anoop Kunchukuttan 
#

import sys, string, itertools, re, os
from collections import defaultdict

from indicnlp import common
from indicnlp import langinfo 
from indicnlp.script import indic_scripts as isc
from indicnlp.transliterate.sinhala_transliterator import SinhalaDevanagariTransliterator  as sdt
import pandas as pd

OFFSET_TO_ITRANS={}
ITRANS_TO_OFFSET=defaultdict(list)

DUPLICATE_ITRANS_REPRESENTATIONS={}


def init():
    """
    To be called by library loader, do not call it in your program 
    """
    
    ### Load the ITRANS-script offset map. The map was initially generated using the snippet below (uses the old itrans transliterator) 
    ### The map is modified as needed to accomodate extensions and corrections to the mappings 
    #
    # base=0x900
    # l=[]
    # for i in range(0,0x80):
    #     c=chr(base+i)
    #     itrans=ItransTransliterator.to_itrans(c,'hi')
    #     l.append((hex(i),c,itrans))
    # print(l)
    #
    # pd.DataFrame(l,columns=['offset_hex','devnag_char','itrans']).to_csv('offset_itrans_map.csv',index=False,encoding='utf-8')

    itrans_map_fname=os.path.join(common.get_resources_path(),'transliterate','offset_itrans_map.csv')
    #itrans_map_fname=r'D:\src\python_sandbox\src\offset_itrans_map.csv'
    itrans_df=pd.read_csv(itrans_map_fname,encoding='utf-8')        

    global OFFSET_TO_ITRANS, ITRANS_TO_OFFSET, DUPLICATE_ITRANS_REPRESENTATIONS

    for r in itrans_df.iterrows():
        itrans=r[1]['itrans']
        o=int(r[1]['offset_hex'],base=16)

        OFFSET_TO_ITRANS[o]=itrans
        
        if langinfo.is_consonant_offset(o):
            ### for consonants, strip the schwa - add halant offset 
            ITRANS_TO_OFFSET[itrans[:-1]].extend([o,0x4d])
        else:
            ### the append assumes that the maatra always comes after independent vowel in the df
            ITRANS_TO_OFFSET[itrans].append(o)


        DUPLICATE_ITRANS_REPRESENTATIONS =  {
                'A': 'aa',
                'I': 'ii',
                'U': 'uu',
                'RRi': 'R^i',
                'RRI': 'R^I',
                'LLi': 'L^i',
                'LLI': 'L^I',
                'L': 'ld',
                'w': 'v',
                'x': 'kSh',    
                'gj': 'j~n',    
                'dny': 'j~n',    
                '.n': '.m',        
                'M': '.m',
                'OM': 'AUM'
            }

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

            offsets = [ isc.get_offset(c,lang_code) for c in text ]
            
            ### naive lookup
            # itrans_l = [ OFFSET_TO_ITRANS.get(o, '-' ) for o in offsets ]
            itrans_l=[]
            for o in offsets:
                itrans=OFFSET_TO_ITRANS.get(o, chr(langinfo.SCRIPT_RANGES[lang_code][0]+o) )
                if langinfo.is_halanta_offset(o):
                    itrans=''
                    if len(itrans_l)>0:
                        itrans_l.pop()
                elif langinfo.is_vowel_sign_offset(o) and len(itrans_l)>0:
                    itrans_l.pop()
                itrans_l.extend(itrans)
                
            return ''.join(itrans_l)
            
        else:
            return text

    @staticmethod
    def from_itrans(text,lang):
        """
        TODO: Document this method properly
        TODO: A little hack is used to handle schwa: needs to be documented
        TODO: check for robustness
        """

        MAXCODE=4  ### TODO: Needs to be fixed
        
        ##  handle_duplicate_itrans_representations
        for k, v in DUPLICATE_ITRANS_REPRESENTATIONS.items():
            if k in text:
                text=text.replace(k,v)
        
        start=0
        match=None
        solution=[]

        i=start+1  
        while i<=len(text):

            itrans=text[start:i]
            
    #         print('===')
    #         print('i: {}'.format(i))
    #         if i<len(text):
    #             print('c: {}'.format(text[i-1]))
    #         print('start: {}'.format(start))
    #         print('itrans: {}'.format(itrans))
            
            if itrans in ITRANS_TO_OFFSET:
                offs=ITRANS_TO_OFFSET[itrans]
                
                ## single element list - no problem 
                ## except when it is 'a'
                
                ## 2 element list of 2 kinds: 
                ### 1. alternate char for independent/dependent vowel
                ### 2. consonant + halant
                
                if len(offs)==2 and \
                    langinfo.is_vowel_offset(offs[0]):
                        ### 1. alternate char for independent/dependent vowel
                        ## if previous is a consonant, then use the dependent vowel 
                    if len(solution)>0 and langinfo.is_halanta(solution[-1],lang):
                        offs=[offs[1]]  ## dependent vowel
                    else:
                        offs=[offs[0]]  ## independent vowel

                c=''.join([ langinfo.offset_to_char(x,lang) for x in offs ])
                match=(i,c)
                
            elif len(itrans)==1: ## unknown character 
                match=(i,itrans)
            elif i<len(text) and (i-start)<MAXCODE+1: ## continue matching till MAXCODE length substring
                i=i+1
                continue
            else: 
                solution.extend(match[1])
    #             start=i-1
                start=match[0]
                i=start
                match=None
    #             print('match done')
                
                
    #         print('match: {}'.format(match))
            
            i=i+1

        ### flush matches 
        if match is not None:
            solution.extend(match[1])

        #### post-processing 
        ## delete unecessary halants 
    #     print(''.join(solution))
        temp_out=list(''.join(solution))
        rem_indices=[]
        for i in range(len(temp_out)-1):
            if langinfo.is_halanta(temp_out[i],lang) and \
                (langinfo.is_vowel_sign(temp_out[i+1],lang) \
                or langinfo.is_nukta(temp_out[i+1],lang)  \
                or temp_out[i+1]==langinfo.offset_to_char(0x7f,lang)):
                rem_indices.append(i)
    #         if temp_out[i]==langinfo.offset_to_char(0x7f,lang):
    #             rem_indices.append(i)
        for i in reversed(rem_indices):
            temp_out.pop(i)

        out=''.join(temp_out)    
        
        ## delete schwa placeholder
        out=out.replace(langinfo.offset_to_char(0x7f,lang),'')

        return out 

if __name__ == '__main__': 

    if len(sys.argv)<4:
        print("Usage: python unicode_transliterate.py <command> <infile> <outfile> <src_language> <tgt_language>")
        sys.exit(1)

    if sys.argv[1]=='transliterate':

        src_language=sys.argv[4]
        tgt_language=sys.argv[5]

        with open(sys.argv[2],'r', encoding='utf-8') as ifile:
            with open(sys.argv[3],'w', encoding='utf-8') as ofile:
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

        with open(sys.argv[2],'r', encoding='utf-8') as ifile:
            with open(sys.argv[3],'w', encoding='utf-8') as ofile:
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

        with open(sys.argv[2],'r', encoding='utf-8') as ifile:
            with open(sys.argv[3],'w', encoding='utf-8') as ofile:
                for line in ifile.readlines():
                    transliterated_line=ItransTransliterator.from_itrans(line,language)
                    ofile.write(transliterated_line)

