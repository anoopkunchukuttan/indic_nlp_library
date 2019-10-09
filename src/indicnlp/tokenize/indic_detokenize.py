
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

#Program for detokenizing Indian language input 
#
# @author Anoop Kunchukuttan 
#

import argparse
import string, re, sys, codecs

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
pat_num_seq=re.compile(r'([0-9]+ [,.:/] )+[0-9]+')

### e-mail address
#pat_num=re.compile(ur'[a-zA-Z]+[ ]? 

def trivial_detokenize_indic(s): 
    """
    A trivial detokenizer
        - decides whether punctuation attaches to left/right or both
        - handles number sequences
        - smart handling of quotes
    returns a detokenized string
    """

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

def trivial_detokenize(s,lang='hi'): 
    """
    Trivial tokenizer for languages in the Indian sub-continent
    """
    if lang=='ur':
        raise IndicNlpException('No detokenizer available for Urdu')
    else:
        return trivial_detokenize_indic(s)

if __name__ == '__main__': 

    if len(sys.argv)<4:
        print("Usage: python indic_detokenize.py <infile> <outfile> <language>")
        print("       Set file to - for stdin/stdout")
        sys.exit(1)
    parser = argparse.ArgumentParser()
    parser.add_argument("infile", type = argparse.FileType('r', encoding="utf8"),  metavar='INFILE')
    parser.add_argument("outfile", type = argparse.FileType('w', encoding="utf8"),  metavar='OUTFILE')
    parser.add_argument("language", metavar='LANGUAGE')
    args = parser.parse_args()


    for line in args.infile:
        detokenized_line=trivial_detokenize(line,args.language)
        args.outfile.write(detokenized_line)
