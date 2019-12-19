# 
#  Copyright (c) 2013-present, Anoop Kunchukuttan
#  All rights reserved.
#  
#  This source code is licensed under the MIT license found in the
#  LICENSE file in the root directory of this source tree.
# 

from indicnlp import loader
from indicnlp import langinfo
from indicnlp.script.indic_scripts import * 
import numpy as np
import gzip
import pandas as pd
import sys 

def equal(v1,v2): 
    return 0.0 if  np.sum( xor_vectors(v1, v2)) > 0  else 1.0

def dice(v1,v2):
    dotprod=2*float(np.dot( v1, v2.T ))
    return dotprod/float(len(v1)+len(v2))

def jaccard(v1,v2):
    dotprod=float(np.dot( v1, v2.T ))
    return dotprod/float(len(v1)+len(v2)-dotprod)

def cosine(v1,v2):
    dotprod=float(np.dot( v1, v2.T ))
    norm1=float(np.dot( v1, v1.T ))
    norm2=float(np.dot( v2, v2.T ))
    return ((dotprod)/(np.sqrt(norm1*norm2)+0.00001))

def dotprod(v1,v2): 
    return float(np.dot( v1, v2.T ))

def sim1(v1,v2,base=5.0): 
    return np.power(base,dotprod(v1,v2)) 

def softmax(v1,v2): 
    return sim1(v1,v2,np.e)

def create_similarity_matrix(sim_func,slang,tlang,normalize=True):

    dim=langinfo.COORDINATED_RANGE_END_INCLUSIVE-langinfo.COORDINATED_RANGE_START_INCLUSIVE+1    
    sim_mat=np.zeros((dim,dim))    

    for offset1 in range(langinfo.COORDINATED_RANGE_START_INCLUSIVE, langinfo.COORDINATED_RANGE_END_INCLUSIVE+1): 
        v1=get_phonetic_feature_vector(offset_to_char(offset1,slang),slang)
        for offset2 in range(langinfo.COORDINATED_RANGE_START_INCLUSIVE, langinfo.COORDINATED_RANGE_END_INCLUSIVE+1): 
            v2=get_phonetic_feature_vector(offset_to_char(offset2,tlang),tlang)
            sim_mat[offset1,offset2]=sim_func(v1,v2)

    if normalize: 
        sums=np.sum(sim_mat, axis=1)
        sim_mat=(sim_mat.transpose()/sums).transpose()

    return sim_mat

