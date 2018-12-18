
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

#Program for tokenizing Indian language input 
#
# @author Anoop Kunchukuttan 
#

import string, re, sys, codecs

from indicnlp.common import IndicNlpException

## detokenizer patterns 
left_attach=u'!%)\]},./:;>?\\\u0964\u0965'
pat_la=re.compile(ur'[ ](['+left_attach+ur'])')

right_attach=u'#$(\[{<@'
pat_ra=re.compile(ur'(['+right_attach+ur'])[ ]')

lr_attach=u'-'
pat_lra=re.compile(ur'[ ](['+lr_attach+ur'])[ ]')

#donknow=u'&*+=^_|~'

def trivial_detokenize_indic(s): 
    """
    A trivial detokenizer which just tokenizes on the punctuation boundaries. 
    This also includes punctuations for the Indian language scripts
      - the purna virama and the deergha virama
    returns a detokenized string
    """

    ### some normalizations 
    #numbers and dates

    ###  consective single quotes or backslashes become double quotes
    #s=s.replace("' '", "''")
    #s=s.replace("` `", '``')

    s=pat_la.sub(u'\\1',s)
    s=pat_ra.sub(u'\\1',s)
    s=pat_lra.sub(u'\\1',s)

    # assumes well formedness of quotes and alternates between right and left attach

    alt_attach=u'\'"`'
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
        print "Usage: python indic_detokenize.py <infile> <outfile> <language>"
        sys.exit(1)

    with codecs.open(sys.argv[1],'r','utf-8') as ifile:
        with codecs.open(sys.argv[2],'w','utf-8') as ofile:
            for line in ifile:
                tokenized_line=trivial_detokenize(line,sys.argv[3])
                ofile.write(tokenized_line)
