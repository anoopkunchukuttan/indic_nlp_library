# -*- coding: utf-8 -*-
# 
#  Copyright (c) 2013-present, Anoop Kunchukuttan
#  All rights reserved.
#  
#  This source code is licensed under the MIT license found in the
#  LICENSE file in the root directory of this source tree.
# 

#Program to transliterate acronyms from one Latin script to Indic languages 
#
# @author Anoop Kunchukuttan 
#

from indicnlp.transliterate.unicode_transliterate import UnicodeIndicTransliterator
import string
import random

class LatinToIndicAcronymTransliterator(object):

    LATIN_TO_DEVANAGARI_TRANSTABLE = str.maketrans({
        'a':'ए',
        'b':'बी',
        'c':'सी',
        'd':'डी',
        'e':'ई',
        'f':'एफ',
        'g':'जी',
        'h':'एच',
        'i':'आई',
        'j':'जे',
        'k':'के',
        'l':'एल',
        'm':'एम',
        'n':'एन',
        'o':'ओ',
        'p':'पी',
        'q':'क्यू',
        'r':'आर',
        's':'एस',
        't':'टी',
        'u':'यू',
        'v':'वी',
        'w':'डब्ल्यू',
        'x':'एक्स',
        'y':'वाय',
        'z':'जेड',
    })

    # a_unichr=ord('a')
    # alphabet = [ chr(a_unichr+n) for n in range(26) ]        
    LATIN_ALPHABET = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

    @staticmethod
    def get_transtable():
        return LatinToIndicAcronymTransliterator.LATIN_TO_DEVANAGARI_TRANSTABLE

    @staticmethod
    def transliterate(w,lang):
        return UnicodeIndicTransliterator.transliterate(w.lower().translate(LatinToIndicAcronymTransliterator.LATIN_TO_DEVANAGARI_TRANSTABLE),'hi',lang)

    @staticmethod
    def generate_latin_acronyms(num_acronyms, min_len=2, max_len=6, strategy='random'):
        """
            generate Latin acronyms in lower case
        """
        
        def sample_acronym(strategy='random'):
            if strategy=='random':
                slen=random.randint(min_len,max_len)
                return ''.join(random.choices(LatinToIndicAcronymTransliterator.LATIN_ALPHABET,k=slen))
        
        
        return [ sample_acronym(strategy) for i in range(num_acronyms) ]
        


    