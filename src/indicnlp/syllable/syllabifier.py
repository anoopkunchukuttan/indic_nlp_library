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

