# 
#  Copyright (c) 2013-present, Anoop Kunchukuttan
#  All rights reserved.
#  
#  This source code is licensed under the MIT license found in the
#  LICENSE file in the root directory of this source tree.
# 

import pandas as pd
import numpy as np

from indicnlp import common
from indicnlp.common import IndicNlpException


#### Maps from ARPABET to Internal Id
ARPABET_ID_MAP={}
ID_ARPABET_MAP={}


###
# Phonetic Information about script characters 
###

""" Phonetic data for English """
ENGLISH_PHONETIC_DATA=None

""" Phonetic vector for English"""
ENGLISH_PHONETIC_VECTORS=None

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

####
SCRIPT_RANGE_START=0x0D00
## TBD
SCRIPT_RANGE_END=0x0D2E


def init():
    """
    To be called by library loader, do not call it in your program 
    """

    global ENGLISH_PHONETIC_DATA, ENGLISH_PHONETIC_VECTORS, PHONETIC_VECTOR_LENGTH, PHONETIC_VECTOR_START_OFFSET

    ENGLISH_PHONETIC_DATA=pd.read_csv(common.get_resources_path()+'/script/english_script_phonetic_data.csv',encoding='utf-8')    

    ENGLISH_PHONETIC_VECTORS=ENGLISH_PHONETIC_DATA.ix[:,PHONETIC_VECTOR_START_OFFSET:].as_matrix()

    PHONETIC_VECTOR_LENGTH=ENGLISH_PHONETIC_VECTORS.shape[1]

    ### Load mapping from ARPABET representation of phoneme to internal ID
    global ARPABET_ID_MAP, ID_ARPABET_MAP

    with open(common.get_resources_path()+'/script/english_arpabet_list.csv','r',encoding='utf-8') as infile: 
        for ph_id, name in enumerate(iter(infile)): 
            name=name.strip()
            ARPABET_ID_MAP[name]=ph_id
            ID_ARPABET_MAP[ph_id]=name


def phoneme_to_offset(ph): 
    return ARPABET_ID_MAP[ph]

def offset_to_phoneme(ph_id): 
    return ID_ARPABET_MAP[ph_id]

def phoneme_to_enc(ph): 
    return chr(SCRIPT_RANGE_START+phoneme_to_offset(ph))

def enc_to_phoneme(ph): 
    return offset_to_phoneme(enc_to_offset(ph))

def enc_to_offset(c): 
    return ord(c)-SCRIPT_RANGE_START

def in_range(offset): 
    return offset>=SCRIPT_RANGE_START and offset<SCRIPT_RANGE_END 

def get_phonetic_info(lang): 
    return (ENGLISH_PHONETIC_DATA, ENGLISH_PHONETIC_VECTORS)

def invalid_vector():
    ##  TODO: check if np datatype is correct?
    return np.array([0]*PHONETIC_VECTOR_LENGTH)

def get_phonetic_feature_vector(p,lang):

    offset=enc_to_offset(p) 

    if not in_range(offset): 
        return invalid_vector()

    phonetic_data, phonetic_vectors= get_phonetic_info(lang)

    if phonetic_data.ix[offset,'Valid Vector Representation']==0: 
        return invalid_vector()

    return phonetic_vectors[offset]

