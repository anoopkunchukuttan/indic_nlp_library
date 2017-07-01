# Copyright Anoop Kunchukuttan 2016 - present
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

import codecs, sys
from indicnlp.script import indic_scripts as si 
import re

chillu_char_map= {
                    u'\u0d7a': u'\u0d23', 
                    u'\u0d7b': u'\u0d28',
                    u'\u0d7c': u'\u0d30',
                    u'\u0d7d': u'\u0d32',
                    u'\u0d7e': u'\u0d33',
                    u'\u0d7f': u'\u0d15',
                 }

char_chillu_map= {}
for k,v in chillu_char_map.iteritems():
    char_chillu_map[v]=k

def normalize_malayalam(word): 

    word_mask=re.sub(ur'[0-9]',u'0',word)

    # instead of chillu characters, use consonant+halant 
    for chillu,char in chillu_char_map.iteritems(): 
        word=word.replace(chillu,u'{}\u0d4d'.format(char)) 
        word_mask=word_mask.replace(chillu,u'41')

    word_mask=re.sub(ur'[^0-9]',u'0',word_mask)

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
            word_mask[idx:idx+2]=u'0'
            start=idx            
        except ValueError as e: 
            break

    return u''.join(word)

def normalize_punjabi(word): 
    word_mask=re.sub(ur'[0-9]',u'0',word)

    ## replace tippi with anusvaar
    word=word.replace(u'\u0a70',u'\u0a02')
    word_mask=word_mask.replace(u'\u0a70',u'2')

    ## replace addak+consonant with consonat+halant+consonant
    word=re.sub(ur'\u0a71(.)',u'\\1\u0a4d\\1',word)
    word_mask=re.sub(ur'\u0a71(.)',u'311',word_mask)

    word_mask=re.sub(ur'[^0-9]',u'0',word_mask)

    return word, word_mask

def denormalize_punjabi(word, word_mask):
    
    word=list(word)
    word_mask=list(word_mask)

    ## pattern 2
    idx=0
    while idx>=0: 
        try: 
            idx=word_mask.index('2',idx)
            word[idx]=u'\u0a70'
            word_mask[idx]=u'0'
            start=idx            
        except ValueError as e: 
            break

    ## pattern 3
    idx=0
    while idx>=0: 
        try: 
            idx=word_mask.index('3',idx)
            word[idx:idx+3]=u'\u0a71{}'.format(word[idx])
            word_mask[idx:idx+3]=u'00'
            start=idx            
        except ValueError as e: 
            break

    return u''.join(word)

def orthographic_syllabify_improved(word,lang): 

    word_mask=['0']*len(word)

    if lang=='ml':
        word, word_mask = normalize_malayalam(word)
        word=word
    elif lang=='pa':
        word, word_mask = normalize_punjabi(word)

    p_vectors=[si.get_phonetic_feature_vector(c,lang) for c in word]

    syllables=[]
    syllables_mask=[]

    for i in xrange(len(word)): 
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
            syllables.append(u' ')
            syllables_mask.append(u'0')

        elif not si.is_valid(v) or si.is_misc(v) :
            syllables.append(u' ')
            syllables_mask.append(u'0')

        elif si.is_vowel(v):

            anu_nonplos= ( i+2<len(word) and \
                           si.is_anusvaar(p_vectors[i+1]) and \
                           not si.is_plosive(p_vectors[i+2])\
                         )
            
            anu_eow= ( i+2==len(word) and \
                           si.is_anusvaar(p_vectors[i+1]) )

            if not(anu_nonplos or anu_eow):              
                syllables.append(u' ')
                syllables_mask.append(u'0')

        elif i+1<len(word) and \
                (si.is_consonant(v) or si.is_nukta(v)): 
            if si.is_consonant(p_vectors[i+1]): 
                syllables.append(u' ')
                syllables_mask.append(u'0')
            elif si.is_vowel(p_vectors[i+1]) and \
                    not si.is_dependent_vowel(p_vectors[i+1]): 
                syllables.append(u' ')
                syllables_mask.append(u'0')
            elif si.is_anusvaar(p_vectors[i+1]):
                anu_nonplos= ( i+2<len(word) and \
                               not si.is_plosive(p_vectors[i+2])\
                             )
                
                anu_eow= i+2==len(word) 

                if not(anu_nonplos or anu_eow):              
                    syllables.append(u' ')
                    syllables_mask.append(u'0')

    syllables_mask=u''.join(syllables_mask)
    syllables=u''.join(syllables)

    #assert len(syllables_mask) == len(syllables)
    #assert syllables_mask.find('01') == -1
    if syllables_mask.find('01') >= 0: 
        print 'Warning'

    if lang=='ml': 
        syllables = denormalize_malayalam(syllables,syllables_mask)
    elif lang=='pa': 
        syllables = denormalize_punjabi(syllables,syllables_mask)

    return syllables.strip().split(u' ')        

def orthographic_syllabify(word,lang): 

    p_vectors=[si.get_phonetic_feature_vector(c,lang) for c in word]

    syllables=[]

    for i in xrange(len(word)): 
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
            syllables.append(u' ')

        elif not si.is_valid(v) or si.is_misc(v) :
            syllables.append(u' ')

        elif si.is_vowel(v):

            anu_nonplos= ( i+2<len(word) and \
                           si.is_anusvaar(p_vectors[i+1]) and \
                           not si.is_plosive(p_vectors[i+2])\
                         )
            
            anu_eow= ( i+2==len(word) and \
                           si.is_anusvaar(p_vectors[i+1]) )

            if not(anu_nonplos or anu_eow):              
                syllables.append(u' ')

        elif i+1<len(word) and \
                (si.is_consonant(v) or si.is_nukta(v)): 
            if si.is_consonant(p_vectors[i+1]): 
                syllables.append(u' ')
            elif si.is_vowel(p_vectors[i+1]) and \
                    not si.is_dependent_vowel(p_vectors[i+1]): 
                syllables.append(u' ')
            elif si.is_anusvaar(p_vectors[i+1]):
                anu_nonplos= ( i+2<len(word) and \
                               not si.is_plosive(p_vectors[i+2])\
                             )
                
                anu_eow= i+2==len(word) 

                if not(anu_nonplos or anu_eow):              
                    syllables.append(u' ')

    return u''.join(syllables).strip().split(u' ')        

def orthographic_simple_syllabify(word,lang): 

    p_vectors=[si.get_phonetic_feature_vector(c,lang) for c in word]

    syllables=[]

    for i in xrange(len(word)): 
        v=p_vectors[i]

        syllables.append(word[i])

        ## simplified syllabification 
        if i+1<len(word) and \
                (not si.is_valid(p_vectors[i+1]) or si.is_misc(p_vectors[i+1])):
            syllables.append(u' ')

        elif not si.is_valid(v) or si.is_misc(v) or si.is_vowel(v):
            syllables.append(u' ')

        elif i+1<len(word) and \
             (si.is_consonant(v) or si.is_nukta(v)) and \
             (si.is_consonant(p_vectors[i+1]) or si.is_anusvaar(p_vectors[i+1])):
            syllables.append(u' ')


    return u''.join(syllables).strip().split(u' ')        

