# 
#  Copyright (c) 2013-present, Anoop Kunchukuttan
#  All rights reserved.
#  
#  This source code is licensed under the MIT license found in the
#  LICENSE file in the root directory of this source tree.
# 

import codecs, sys
from indicnlp.script import indic_scripts as si 
import re

chillu_char_map= {
                    '\u0d7a': '\u0d23', 
                    '\u0d7b': '\u0d28',
                    '\u0d7c': '\u0d30',
                    '\u0d7d': '\u0d32',
                    '\u0d7e': '\u0d33',
                    '\u0d7f': '\u0d15',
                 }

char_chillu_map= {}
for k,v in chillu_char_map.items():
    char_chillu_map[v]=k

def normalize_malayalam(word): 

    word_mask=re.sub(r'[0-9]','0',word)

    # instead of chillu characters, use consonant+halant 
    for chillu,char in chillu_char_map.items(): 
        word=word.replace(chillu,'{}\u0d4d'.format(char)) 
        word_mask=word_mask.replace(chillu,'41')

    word_mask=re.sub(r'[^0-9]','0',word_mask)

    return word, word_mask

def denormalize_malayalam(word, word_mask):

    word=list(word)
    word_mask=list(word_mask)

    ## pattern 4
    idx=0
    while idx>=0: 
        try: 
            idx=word_mask.index('4',idx)
            word[idx:idx+2]=char_chillu_map[word[idx]]
            word_mask[idx:idx+2]='0'
            start=idx            
        except ValueError as e: 
            break

    return ''.join(word)

def normalize_punjabi(word): 
    word_mask=re.sub(r'[0-9]','0',word)

    ## replace tippi with anusvaar
    word=word.replace('\u0a70','\u0a02')
    word_mask=word_mask.replace('\u0a70','2')

    ## replace addak+consonant with consonat+halant+consonant
    word=re.sub(r'\u0a71(.)','\\1\u0a4d\\1',word)
    word_mask=re.sub(r'\u0a71(.)','311',word_mask)

    word_mask=re.sub(r'[^0-9]','0',word_mask)

    return word, word_mask

def denormalize_punjabi(word, word_mask):
    
    word=list(word)
    word_mask=list(word_mask)

    ## pattern 2
    idx=0
    while idx>=0: 
        try: 
            idx=word_mask.index('2',idx)
            word[idx]='\u0a70'
            word_mask[idx]='0'
            start=idx            
        except ValueError as e: 
            break

    ## pattern 3
    idx=0
    while idx>=0: 
        try: 
            idx=word_mask.index('3',idx)
            word[idx:idx+3]='\u0a71{}'.format(word[idx])
            word_mask[idx:idx+3]='00'
            start=idx            
        except ValueError as e: 
            break

    return ''.join(word)

def char_backoff(syllables_list,vocab):
    syllables_final=[]    

    if vocab is None:
        syllables_final=syllables_list
    else:
        for s in syllables_list:
            if s in vocab: 
                syllables_final.append(s)
            else: 
                for x in s:
                    syllables_final.append(x)                    

    return syllables_final        


def orthographic_syllabify_improved(word,lang,vocab=None): 

    word_mask=['0']*len(word)

    if lang=='ml':
        word, word_mask = normalize_malayalam(word)
        word=word
    elif lang=='pa':
        word, word_mask = normalize_punjabi(word)

    p_vectors=[si.get_phonetic_feature_vector(c,lang) for c in word]

    syllables=[]
    syllables_mask=[]

    for i in range(len(word)): 
        v=p_vectors[i]

        syllables.append(word[i])
        syllables_mask.append(word_mask[i])

        ### simplified syllabification 
        #if i+1<len(word) and \
        #        (not si.is_valid(p_vectors[i+1]) or si.is_misc(p_vectors[i+1])):
        #    syllables.append(u' ')
        #    syllables_mask.append(u'0')

        #elif not si.is_valid(v) or si.is_misc(v) or si.is_vowel(v):
        #    syllables.append(u' ')
        #    syllables_mask.append(u'0')

        #elif i+1<len(word) and \
        #     (si.is_consonant(v) or si.is_nukta(v)) and \
        #     (si.is_consonant(p_vectors[i+1]) or si.is_anusvaar(p_vectors[i+1])):
        #    syllables.append(u' ')
        #    syllables_mask.append(u'0')

        #### better syllabification 
        if i+1<len(word) and (not si.is_valid(p_vectors[i+1]) or si.is_misc(p_vectors[i+1])):
            syllables.append(' ')
            syllables_mask.append('0')

        elif not si.is_valid(v) or si.is_misc(v) :
            syllables.append(' ')
            syllables_mask.append('0')

        elif si.is_vowel(v):

            anu_nonplos= ( i+2<len(word) and \
                           si.is_anusvaar(p_vectors[i+1]) and \
                           not si.is_plosive(p_vectors[i+2])\
                         )
            
            anu_eow= ( i+2==len(word) and \
                           si.is_anusvaar(p_vectors[i+1]) )

            if not(anu_nonplos or anu_eow):              
                syllables.append(' ')
                syllables_mask.append('0')

        elif i+1<len(word) and \
                (si.is_consonant(v) or si.is_nukta(v)): 
            if si.is_consonant(p_vectors[i+1]): 
                syllables.append(' ')
                syllables_mask.append('0')
            elif si.is_vowel(p_vectors[i+1]) and \
                    not si.is_dependent_vowel(p_vectors[i+1]): 
                syllables.append(' ')
                syllables_mask.append('0')
            elif si.is_anusvaar(p_vectors[i+1]):
                anu_nonplos= ( i+2<len(word) and \
                               not si.is_plosive(p_vectors[i+2])\
                             )
                
                anu_eow= i+2==len(word) 

                if not(anu_nonplos or anu_eow):              
                    syllables.append(' ')
                    syllables_mask.append('0')

    syllables_mask=''.join(syllables_mask)
    syllables=''.join(syllables)

    #assert len(syllables_mask) == len(syllables)
    #assert syllables_mask.find('01') == -1
    if syllables_mask.find('01') >= 0: 
        print('Warning')

    if lang=='ml': 
        syllables = denormalize_malayalam(syllables,syllables_mask)
    elif lang=='pa': 
        syllables = denormalize_punjabi(syllables,syllables_mask)

    syllables_list = syllables.strip().split(' ')  
    return(char_backoff(syllables_list,vocab))    

def orthographic_syllabify(word,lang,vocab=None): 

    p_vectors=[si.get_phonetic_feature_vector(c,lang) for c in word]

    syllables=[]

    for i in range(len(word)): 
        v=p_vectors[i]

        syllables.append(word[i])

        ### simplified syllabification 
        #if i+1<len(word) and \
        #        (not si.is_valid(p_vectors[i+1]) or si.is_misc(p_vectors[i+1])):
        #    syllables.append(u' ')

        #elif not si.is_valid(v) or si.is_misc(v) or si.is_vowel(v):
        #    syllables.append(u' ')

        #elif i+1<len(word) and \
        #     (si.is_consonant(v) or si.is_nukta(v)) and \
        #     (si.is_consonant(p_vectors[i+1]) or si.is_anusvaar(p_vectors[i+1])):
        #    syllables.append(u' ')

        #### better syllabification 
        if i+1<len(word) and (not si.is_valid(p_vectors[i+1]) or si.is_misc(p_vectors[i+1])):
            syllables.append(' ')

        elif not si.is_valid(v) or si.is_misc(v) :
            syllables.append(' ')

        elif si.is_vowel(v):

            anu_nonplos= ( i+2<len(word) and \
                           si.is_anusvaar(p_vectors[i+1]) and \
                           not si.is_plosive(p_vectors[i+2])\
                         )
            
            anu_eow= ( i+2==len(word) and \
                           si.is_anusvaar(p_vectors[i+1]) )

            if not(anu_nonplos or anu_eow):              
                syllables.append(' ')

        elif i+1<len(word) and \
                (si.is_consonant(v) or si.is_nukta(v)): 
            if si.is_consonant(p_vectors[i+1]): 
                syllables.append(' ')
            elif si.is_vowel(p_vectors[i+1]) and \
                    not si.is_dependent_vowel(p_vectors[i+1]): 
                syllables.append(' ')
            elif si.is_anusvaar(p_vectors[i+1]):
                anu_nonplos= ( i+2<len(word) and \
                               not si.is_plosive(p_vectors[i+2])\
                             )
                
                anu_eow= i+2==len(word) 

                if not(anu_nonplos or anu_eow):              
                    syllables.append(' ')

    syllables_list = ''.join(syllables).strip().split(' ') 
    return(char_backoff(syllables_list,vocab))

def orthographic_simple_syllabify(word,lang,vocab=None): 

    p_vectors=[si.get_phonetic_feature_vector(c,lang) for c in word]

    syllables=[]

    for i in range(len(word)): 
        v=p_vectors[i]

        syllables.append(word[i])

        ## simplified syllabification 
        if i+1<len(word) and \
                (not si.is_valid(p_vectors[i+1]) or si.is_misc(p_vectors[i+1])):
            syllables.append(' ')

        elif not si.is_valid(v) or si.is_misc(v) or si.is_vowel(v):
            syllables.append(' ')

        elif i+1<len(word) and \
             (si.is_consonant(v) or si.is_nukta(v)) and \
             (si.is_consonant(p_vectors[i+1]) or si.is_anusvaar(p_vectors[i+1])):
            syllables.append(' ')

    syllables_list = ''.join(syllables).strip().split(' ') 
    return(char_backoff(syllables_list,vocab))
