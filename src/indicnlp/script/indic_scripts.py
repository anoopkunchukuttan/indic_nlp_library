# Copyright Anoop Kunchukuttan 2014 - present
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

import pandas as pd
import numpy as np

from indicnlp import common
from indicnlp.common import IndicNlpException
from indicnlp import langinfo as li

###
# Phonetic Information about script characters 
###

""" Phonetic data about all languages except Tamil """
ALL_PHONETIC_DATA=None

""" Phonetic data for Tamil """
TAMIL_PHONETIC_DATA=None

""" Phonetic vector for all languages except Tamil """
ALL_PHONETIC_VECTORS=None

""" Phonetic vector for Tamil """
TAMIL_PHONETIC_VECTORS=None

""" Start offset for the phonetic feature vector in the phonetic data vector """
PHONETIC_VECTOR_START_OFFSET=6

####
# Indexes into the Phonetic Vector 
####
PVIDX_BT_VOWEL=0
PVIDX_BT_CONSONANT=1
PVIDX_BT_NUKTA=2
PVIDX_BT_HALANT=3
PVIDX_BT_ANUSVAAR=4
PVIDX_BT_MISC=5
PVIDX_BT_S=PVIDX_BT_VOWEL 
PVIDX_BT_E=PVIDX_BT_MISC+1

PVIDX_VSTAT_DEP=12

def init():
    """
    To be called by library loader, do not call it in your program 
    """

    global ALL_PHONETIC_DATA, ALL_PHONETIC_VECTORS, TAMIL_PHONETIC_DATA, TAMIL_PHONETIC_VECTORS 

    ALL_PHONETIC_DATA=pd.read_csv(common.get_resources_path()+'/script/all_script_phonetic_data.csv',encoding='utf-8')    
    TAMIL_PHONETIC_DATA=pd.read_csv(common.get_resources_path()+'/script/tamil_script_phonetic_data.csv',encoding='utf-8')    

    ALL_PHONETIC_VECTORS= ALL_PHONETIC_DATA.ix[:,PHONETIC_VECTOR_START_OFFSET:].as_matrix()
    TAMIL_PHONETIC_VECTORS=TAMIL_PHONETIC_DATA.ix[:,PHONETIC_VECTOR_START_OFFSET:].as_matrix()

def is_supported_language(lang): 
    return lang in li.SCRIPT_RANGES.keys()

def get_offset(c,lang): 
    if not is_supported_language(lang): 
        raise IndicNlpException('Language {}  not supported'.format(lang))
    return ord(c)-li.SCRIPT_RANGES[lang][0]

def offset_to_char(off,lang): 
    """
    Applicable to Brahmi derived Indic scripts 
    """
    if not is_supported_language(lang): 
        raise IndicNlpException('Language {}  not supported'.format(lang))
    return unichr(off+li.SCRIPT_RANGES[lang][0])

def is_indiclang_char(c,lang): 
    """
    Applicable to Brahmi derived Indic scripts 
    Note that DANDA and DOUBLE_DANDA have the same Unicode codepoint for all Indic scripts 
    """
    if not is_supported_language(lang): 
        raise IndicNlpException('Language {}  not supported'.format(lang))
    o=get_offset(c,lang)
    return (o>=0 and o<=0x7f) or ord(c)==li.DANDA or ord(c)==li.DOUBLE_DANDA

def in_coordinated_range_offset(c_offset): 
    """
    Applicable to Brahmi derived Indic scripts 
    """
    return  (c_offset>=li.COORDINATED_RANGE_START_INCLUSIVE and c_offset<=li.COORDINATED_RANGE_END_INCLUSIVE) 

def in_coordinated_range(c,lang):
    if not is_supported_language(lang): 
        raise IndicNlpException('Language {}  not supported'.format(lang))
    return in_coordinated_range_offset(get_offset(c,lang))

def get_phonetic_info(lang): 
    if not is_supported_language(lang): 
        raise IndicNlpException('Language {}  not supported'.format(lang))
    phonetic_data= ALL_PHONETIC_DATA if lang!=li.LC_TA else TAMIL_PHONETIC_DATA
    phonetic_vectors= ALL_PHONETIC_VECTORS if lang!=li.LC_TA else TAMIL_PHONETIC_VECTORS
   
    return (phonetic_data, phonetic_vectors)

def get_phonetic_feature_vector(c,lang):

    offset=get_offset(c,lang) 

    if not in_coordinated_range_offset(offset): 
        raise IndicNlpException(u'Character not in co-ordinated script range: {}'.format(c))

    phonetic_data, phonetic_vectors= get_phonetic_info(lang)

    if phonetic_data.ix[offset,'Valid Vector Representation']==0: 
        raise IndicNlpException(u'Character does not have a phonetic vector representation: {}'.format(c))
        
    return phonetic_vectors[offset]

### Unary operations on vectors 
def is_valid(v): 
    """
    at least one of the basic type bits must be 1
    """
    return sum(v[PVIDX_BT_S:PVIDX_BT_E])>0 

def is_vowel(v): 
    return True if v[PVIDX_BT_VOWEL]==1 else False

def is_consonant(v): 
    return True if v[PVIDX_BT_CONSONANT]==1 else False

def is_halant(v): 
    return True if v[PVIDX_BT_HALANT]==1 else False

def is_nukta(v): 
    return True if v[PVIDX_BT_NUKTA]==1 else False

def is_anusvaar(v): 
    return True if v[PVIDX_BT_ANUSVAAR]==1 else False

def is_dependent_vowel(v): 
    return is_vowel(v) and v[PVIDX_VSTAT_DEP]==1

### Binary operations on phonetic vectors

def get_phonetic_similarity_v(v1,v2,base=5.0): 

    dotprod=float(np.dot( v1, v2 ))
    return np.power(base,dotprod) 

    #dotprod=float(np.dot( v1, v2 ))
    #cos_sim=dotprod/(np.sqrt(np.dot(v1,v1))*np.sqrt(np.dot(v2,v2)))
    #return cos_sim

def or_vectors(v1,v2): 
    return np.array([ 1 if (b1+b2)>=1 else 0 for b1,b2 in zip(v1,v2) ])

def add_vectors(v1,v2): 

    if is_consonant(v1) and is_halant(v2): 
        v1[PVIDX_BT_HALANT]=1
        return v1
    elif is_consonant(v1) and is_nukta(v2): 
        v1[PVIDX_BT_NUKTA]=1
        return v1
    elif is_consonant(v1) and is_dependent_vowel(v2): 
        return or_vectors(v1,v2)
    elif is_anusvaar(v1) and is_consonant(v2): 
        return or_vectors(v1,v2)
    else: 
        return [0]*len(v1)

