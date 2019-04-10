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

#Program for sentence splitting of Indian language input 
#
# @author Anoop Kunchukuttan 
#


import re

DELIM_PAT=re.compile(r'[\.\?!\u0964\u0965]')

def sentence_split(text,delim_pat=DELIM_PAT):

    line = text
    
    ### Phase 1: break on sentence delimiters.
    cand_sentences=[]
    begin=0
    text = text.strip()
    for mo in delim_pat.finditer(text):
        p1=mo.start()
        p2=mo.end()

        end=p1+1
        s= text[begin:end].strip()
        if len(s)>0:
            cand_sentences.append(s)
        begin=p1+1

    s= text[begin:].strip()
    if len(s)>0:
        cand_sentences.append(s)

#     return cand_sentences

    ### Phase 2: Address the fact that '.' may not always be a sentence delimiter
    ### Method: If there is a run of lines containing only a word (optionally) and '.',
    ### merge these lines as well one sentence preceding and succeeding this run of lines.
    final_sentences=[]
    sen_buffer=''        
    bad_state=False

    for i, sentence in enumerate(cand_sentences): 
        words=sentence.split(' ')
        #if len(words)<=2 and words[-1]=='.':
        if len(words)==1 and sentence[-1]=='.':
            bad_state=True
            sen_buffer = sen_buffer + ' ' + sentence
        elif bad_state:
            sen_buffer = sen_buffer + ' ' + sentence
            if len(sen_buffer)>0:
                final_sentences.append(sen_buffer)
            sen_buffer=''
            bad_state=False
        else:                     
            if len(sen_buffer)>0:
                final_sentences.append(sen_buffer)
            sen_buffer=sentence
            bad_state=False

    if len(sen_buffer)>0:
        final_sentences.append(sen_buffer)
    
    return final_sentences