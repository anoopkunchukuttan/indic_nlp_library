# 
#  Copyright (c) 2013-present, Anoop Kunchukuttan
#  All rights reserved.
#  
#  This source code is licensed under the MIT license found in the
#  LICENSE file in the root directory of this source tree.
# 

import pandas as pd
import numpy as np
import os

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

""" Length of phonetic vector """
PHONETIC_VECTOR_LENGTH=38

""" Start offset for the phonetic feature vector in the phonetic data vector """
PHONETIC_VECTOR_START_OFFSET=6

## PHONETIC PROPERTIES in order in which they occur in the vector 
## This list must be in sync with the keys in the PV_PROP_RANGES dictionary 
PV_PROP=['basic_type',
    'vowel_length',
    'vowel_strength',
    'vowel_status',
    'consonant_type',
    'articulation_place',
    'aspiration',
    'voicing',
    'nasalization',
    'vowel_horizontal',
    'vowel_vertical',
    'vowel_roundness',
    ]

### 
# Bit vector ranges for various properties 
###

PV_PROP_RANGES={
        'basic_type': [0,6],
        'vowel_length': [6,8],
        'vowel_strength': [8,11],
        'vowel_status': [11,13],
        'consonant_type': [13,18],
        'articulation_place': [18,23],
        'aspiration': [23,25],
        'voicing': [25,27],
        'nasalization': [27,29],
        'vowel_horizontal': [29,32],
        'vowel_vertical': [32,36],
        'vowel_roundness': [36,38],
        }


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

#####
# Unicode information about characters 
#####

SCRIPT_OFFSET_START=0
SCRIPT_OFFSET_RANGE=0x80

def init():
    """
    To be called by library loader, do not call it in your program 
    """

    global ALL_PHONETIC_DATA, ALL_PHONETIC_VECTORS, TAMIL_PHONETIC_DATA, TAMIL_PHONETIC_VECTORS, PHONETIC_VECTOR_LENGTH, PHONETIC_VECTOR_START_OFFSET

    ALL_PHONETIC_DATA=pd.read_csv(os.path.join(common.get_resources_path(),'script','all_script_phonetic_data.csv'),encoding='utf-8')    
    TAMIL_PHONETIC_DATA=pd.read_csv(os.path.join(common.get_resources_path(),'script','tamil_script_phonetic_data.csv'),encoding='utf-8')    

    ALL_PHONETIC_VECTORS= ALL_PHONETIC_DATA.iloc[:,PHONETIC_VECTOR_START_OFFSET:].values
    TAMIL_PHONETIC_VECTORS=TAMIL_PHONETIC_DATA.iloc[:,PHONETIC_VECTOR_START_OFFSET:].values

    PHONETIC_VECTOR_LENGTH=ALL_PHONETIC_VECTORS.shape[1]

def is_supported_language(lang): 
    return lang in list(li.SCRIPT_RANGES.keys())

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
    return chr(off+li.SCRIPT_RANGES[lang][0])

def is_indiclang_char(c,lang): 
    """
    Applicable to Brahmi derived Indic scripts 
    Note that DANDA and DOUBLE_DANDA have the same Unicode codepoint for all Indic scripts 
    """
    if not is_supported_language(lang): 
        raise IndicNlpException('Language {}  not supported'.format(lang))
    o=get_offset(c,lang)
    return (o>=SCRIPT_OFFSET_START and o<SCRIPT_OFFSET_RANGE) \
            or ord(c)==li.DANDA or ord(c)==li.DOUBLE_DANDA

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

def invalid_vector():
    ##  TODO: check if np datatype is correct?
    return np.array([0]*PHONETIC_VECTOR_LENGTH)

def get_phonetic_feature_vector(c,lang):

    offset=get_offset(c,lang) 

    if not in_coordinated_range_offset(offset): 
        return invalid_vector()

    phonetic_data, phonetic_vectors= get_phonetic_info(lang)

    if phonetic_data.iloc[offset]['Valid Vector Representation']==0: 
        return invalid_vector()

    return phonetic_vectors[offset]

def get_phonetic_feature_vector_offset(offset,lang):

    if not in_coordinated_range_offset(offset): 
        return invalid_vector()

    phonetic_data, phonetic_vectors= get_phonetic_info(lang)

    if phonetic_data.iloc[offset]['Valid Vector Representation']==0: 
        return invalid_vector()

    return phonetic_vectors[offset]

### Unary operations on vectors 
def is_valid(v): 
    return np.sum(v)>0

def is_vowel(v): 
    return v[PVIDX_BT_VOWEL]==1 

def is_consonant(v): 
    return  v[PVIDX_BT_CONSONANT]==1 

def is_halant(v): 
    return  v[PVIDX_BT_HALANT]==1 

def is_nukta(v): 
    return  v[PVIDX_BT_NUKTA]==1 

def is_anusvaar(v): 
    return  v[PVIDX_BT_ANUSVAAR]==1 

def is_misc(v): 
    return v[PVIDX_BT_MISC]==1 

def is_dependent_vowel(v): 
    return is_vowel(v) and v[PVIDX_VSTAT_DEP]==1

def is_plosive(v): 
    return is_consonant(v) and get_property_vector(v,'consonant_type')[0]==1

### Binary operations on phonetic vectors

def or_vectors(v1,v2): 
    return np.array([ 1 if (b1+b2)>=1 else 0 for b1,b2 in zip(v1,v2) ])

def xor_vectors(v1,v2): 
    return np.array([ 1 if b1!=b2 else 0 for b1,b2 in zip(v1,v2) ])

### Getting properties from phonetic vectors 

def get_property_vector(v,prop_name): 
    return v[PV_PROP_RANGES[prop_name][0]:PV_PROP_RANGES[prop_name][1]]

def get_property_value(v,prop_name): 
    factor_bits=get_property_vector(v,prop_name).tolist()
    
    v=0
    c=1
    for b in factor_bits[::-1]: 
        v+=(c*b)
        c=c*2.0

    return int(v)

def lcsr_indic(srcw,tgtw,slang,tlang):
    """
    compute the Longest Common Subsequence Ratio (LCSR) between two strings at the character level.
    This works for Indic scripts by mapping both languages to a common script

    srcw: source language string
    tgtw: source language string
    slang: source language 
    tlang: target language 
    """    
    score_mat=np.zeros((len(srcw)+1,len(tgtw)+1))

    for si,sc in enumerate(srcw,1): 
        for ti,tc in enumerate(tgtw,1): 
            so=get_offset(sc,slang)
            to=get_offset(tc,tlang)

            if in_coordinated_range_offset(so) and in_coordinated_range_offset(to) and so==to: 
                score_mat[si,ti]=score_mat[si-1,ti-1]+1.0
            elif not (in_coordinated_range_offset(so) or in_coordinated_range_offset(to)) and sc==tc: 
                score_mat[si,ti]=score_mat[si-1,ti-1]+1.0
            else: 
                score_mat[si,ti]= max(
                    score_mat[si,ti-1],
                    score_mat[si-1,ti])

    return (score_mat[-1,-1]/float(max(len(srcw),len(tgtw))),float(len(srcw)),float(len(tgtw)))

def lcsr_any(srcw,tgtw):
    """
    LCSR computation if both languages have the same script
    """
    score_mat=np.zeros((len(srcw)+1,len(tgtw)+1))

    for si,sc in enumerate(srcw,1): 
        for ti,tc in enumerate(tgtw,1): 

            if sc==tc: 
                score_mat[si,ti]=score_mat[si-1,ti-1]+1.0
            else: 
                score_mat[si,ti]= max(
                    score_mat[si,ti-1],
                    score_mat[si-1,ti])

    return (score_mat[-1,-1]/float(max(len(srcw),len(tgtw))),float(len(srcw)),float(len(tgtw)))

def lcsr(srcw,tgtw,slang,tlang):
    """
    compute the Longest Common Subsequence Ratio (LCSR) between two strings at the character level.

    srcw: source language string
    tgtw: source language string
    slang: source language 
    tlang: target language 
    """

    if slang==tlang or not is_supported_language(slang) or not is_supported_language(tlang):
        return lcsr_any(srcw,tgtw,slang,tlang)
    else:  
        return lcsr_indic(srcw,tgtw)



