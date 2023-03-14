# 
#  Copyright (c) 2013-present, Anoop Kunchukuttan
#  All rights reserved.
#  
#  This source code is licensed under the MIT license found in the
#  LICENSE file in the root directory of this source tree.
# 

#Program for detokenizing Indian language input 
#
# @author Anoop Kunchukuttan 
#
"""
De-tokenizer for Indian languages.
"""

import string, re, sys
from indicnlp.common import IndicNlpException

## detokenizer patterns 
left_attach=r'!%)\]},.:;>?\u0964\u0965'
pat_la=re.compile(r'[ ](['+left_attach+r'])')

right_attach=r'#$(\[{<@'
pat_ra=re.compile(r'(['+right_attach+r'])[ ]')

lr_attach=r'-/\\'
pat_lra=re.compile(r'[ ](['+lr_attach+r'])[ ]')

#donknow=u'&*+=^_|~'

## date, numbers, section/article numbering
## TODO: handle indic numbers
pat_num_seq=re.compile(r'([0-9]+ [,.:/] )+[0-9]+')

### e-mail address
#pat_num=re.compile(ur'[a-zA-Z]+[ ]? 

def trivial_detokenize_indic(text): 
    """detokenize string for Indian language scripts using Brahmi-derived scripts

    A trivial detokenizer which:

        - decides whether punctuation attaches to left/right or both
        - handles number sequences
        - handles quotes smartly (deciding left or right attachment)

    Args:
        text (str): tokenized text to process 

    Returns:
        str: detokenized string
    """

    s=text
    ### some normalizations 

    #numbers and dates
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

    ###  consective single quotes or backslashes become double quotes
    #s=s.replace("' '", "''")
    #s=s.replace("` `", '``')

    s=pat_lra.sub('\\1',s)
    s=pat_la.sub('\\1',s)
    s=pat_ra.sub('\\1',s)

    # assumes well formedness of quotes and alternates between right and left attach

    alt_attach='\'"`'
    for punc in alt_attach: 
        cnt=0
        out_str=[]
        for c in s:
            if c == punc:
                if cnt%2==0:
                    out_str.append('@RA')
                else:
                    out_str.append('@LA')
                cnt+=1    
            else:
                out_str.append(c)

        s=''.join(out_str).replace('@RA ',punc).replace(' @LA',punc
                ).replace('@RA',punc).replace('@LA',punc)

    return s

def trivial_detokenize(text,lang='hi'): 
    """detokenize string for languages of the Indian subcontinent 

    A trivial detokenizer which:

        - decides whether punctuation attaches to left/right or both
        - handles number sequences
        - handles quotes smartly (deciding left or right attachment)

    Args:
        text (str): tokenized text to process 

    Returns:
        str: detokenized string

    Raises:
        IndicNlpException: If language is not supported        
    """
    return trivial_detokenize_indic(text)

# if __name__ == '__main__': 

#     if len(sys.argv)<4:
#         print("Usage: python indic_detokenize.py <infile> <outfile> <language>")
#         sys.exit(1)

#     with open(sys.argv[1],'r', encoding='utf-8') as ifile:
#         with open(sys.argv[2],'w', encoding='utf-8') as ofile:
#             for line in ifile:
#                 detokenized_line=trivial_detokenize(line,sys.argv[3])
#                 ofile.write(detokenized_line)
