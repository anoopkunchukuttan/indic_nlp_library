# 
#  Copyright (c) 2013-present, Anoop Kunchukuttan
#  All rights reserved.
#  
#  This source code is licensed under the MIT license found in the
#  LICENSE file in the root directory of this source tree.
# 

#Program for tokenizing Indian language input 
#
# @author Anoop Kunchukuttan 
#
"""
Tokenizer for Indian languages. Currently, simple punctuation-based tokenizers
are supported (see `trivial_tokenize`). Major Indian language punctuations are
handled. 
"""
import string, re, sys

from indicnlp.common import IndicNlpException

### tokenizer patterns 
triv_tokenizer_indic_pat=re.compile(r'(['+string.punctuation+r'\u0964\u0965\uAAF1\uAAF0\uABEB\uABEC\uABED\uABEE\uABEF\u1C7E\u1C7F'+r'])')
triv_tokenizer_urdu_pat=re.compile(r'(['+string.punctuation+r'\u0609\u060A\u060C\u061E\u066A\u066B\u066C\u066D\u06D4'+r'])')

## date, numbers, section/article numbering
pat_num_seq=re.compile(r'([0-9]+ [,.:/] )+[0-9]+')

def trivial_tokenize_indic(text): 
    """tokenize string for Indian language scripts using Brahmi-derived scripts

    A trivial tokenizer which just tokenizes on the punctuation boundaries. 
    This also includes punctuations for the Indian language scripts (the 
    purna virama and the deergha virama). This is a language independent 
    tokenizer

    Args:
        text (str): text to tokenize

    Returns:
        list: list of tokens

    """
    tok_str=triv_tokenizer_indic_pat.sub(r' \1 ',text.replace('\t',' '))
#     return re.sub(r'[ ]+',' ',tok_str).strip(' ').split(' ')

    s=re.sub(r'[ ]+',' ',tok_str).strip(' ')
    
    # do not tokenize numbers and dates
    new_s=''
    prev=0
    for m in pat_num_seq.finditer(s):
        start=m.start()
        end=m.end()
        if start>prev:
            new_s=new_s+s[prev:start]
            new_s=new_s+s[start:end].replace(' ','')
            prev=end
   
    new_s=new_s+s[prev:]
    s=new_s
    
    return s.split(' ')

def trivial_tokenize_urdu(text): 
    """tokenize Urdu string 

    A trivial tokenizer which just tokenizes on the punctuation boundaries. 
    This also includes punctuations for the Urdu script.
    These punctuations characters were identified from the Unicode database 
    for Arabic script by looking for punctuation symbols.

    Args:
        text (str): text to tokenize

    Returns:
        list: list of tokens
    """
    tok_str=triv_tokenizer_urdu_pat.sub(r' \1 ',text.replace('\t',' '))
    return re.sub(r'[ ]+',' ',tok_str).strip(' ').split(' ')
    # from urduhack.tokenization import word_tokenizer
    # return word_tokenizer(text)

def trivial_tokenize(text,lang='hi'): 
    """trivial tokenizer for Indian languages using Brahmi for Arabic scripts

    A trivial tokenizer which just tokenizes on the punctuation boundaries. 
    Major punctuations specific to Indian langauges are handled. 
    These punctuations characters were identified from the Unicode database. 

    Args:
        text (str): text to tokenize
        lang (str): ISO 639-2 language code

    Returns:
        list: list of tokens
    """
    if lang=='ur':
        return trivial_tokenize_urdu(text)
    else:
        return trivial_tokenize_indic(text)

# if __name__ == '__main__': 

#     if len(sys.argv)<4:
#         print("Usage: python indic_tokenize.py <infile> <outfile> <language>")
#         sys.exit(1)

#     with open(sys.argv[1],'r', encoding='utf-8') as ifile:
#         with open(sys.argv[2],'w', encoding='utf-8') as ofile:
#             for line in ifile:
#                 tokenized_line=' '.join(trivial_tokenize(line,sys.argv[3]))
#                 ofile.write(tokenized_line)
