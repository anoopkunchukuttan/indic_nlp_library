# Copyright Anoop Kunchukuttan 2013 - present
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

#Program for normalization of text written in Unicode. This is mainly geared towards Indic scripts 
#
# @author Anoop Kunchukuttan 
#

import sys, codecs, string, itertools, re
from indicnlp import langinfo


class NormalizerI(object):
    """
    The normalizer classes do the following: 

    * Some characters have multiple Unicode codepoints. The normalizer chooses a single standard representation
    * Some control characters are deleted
    * While typing using the Latin keyboard, certain typical mistakes occur which are corrected by the module

    Base class for normalizer. Performs some common normalization, which includes: 

    * Byte order mark, word joiner, etc. removal 
    * ZERO_WIDTH_NON_JOINER and ZERO_WIDTH_JOINER removal 
    * ZERO_WIDTH_SPACE and NO_BREAK_SPACE replaced by spaces 

    Script specific normalizers should derive from this class and override the normalize() method. 
    They can call the super class 'normalize() method to avail of the common normalization 

    """

    BYTE_ORDER_MARK='\uFEFF'
    BYTE_ORDER_MARK_2='\uFFFE'
    WORD_JOINER='\u2060'
    SOFT_HYPHEN='\u00AD'

    ZERO_WIDTH_SPACE='\u200B'
    NO_BREAK_SPACE='\u00A0'

    ZERO_WIDTH_NON_JOINER='\u200C'
    ZERO_WIDTH_JOINER='\u200D'

    def normalize(self,text):
        pass 


class BaseNormalizer(NormalizerI):

    def __init__(self,lang,remove_nuktas=False,nasals_mode='do_nothing'):
        self.lang=lang
        self.remove_nuktas=remove_nuktas
        self.nasals_mode=nasals_mode

        self._init_normalize_nasals()

    def _init_to_anusvaara_strict(self):
        """
        `r1_nasal=re.compile(r'\\u0919\\u094D([\\u0915-\\u0918])')`
        """
    
        pat_signatures=\
            [
                 [0x19,0x15,0x18],
                 [0x1e,0x1a,0x1d],            
                 [0x23,0x1f,0x22],                        
                 [0x28,0x24,0x27],        
                 [0x29,0x24,0x27],                    
                 [0x2e,0x2a,0x2d],                    
            ]    
        
        halant_offset=0x4d
        anusvaara_offset=0x02
        
        pats=[]
        
        for pat_signature in pat_signatures:
            pat=re.compile(r'{nasal}{halant}([{start_r}-{end_r}])'.format(
                nasal=langinfo.offset_to_char(pat_signature[0],self.lang),
                halant=langinfo.offset_to_char(halant_offset,self.lang),
                start_r=langinfo.offset_to_char(pat_signature[1],self.lang),
                end_r=langinfo.offset_to_char(pat_signature[2],self.lang),
            ))
            pats.append(pat)
        
        repl_string='{anusvaara}\\1'.format(anusvaara=langinfo.offset_to_char(anusvaara_offset,self.lang))

        self.pats_repls=(pats,repl_string)
    
    def _to_anusvaara_strict(self,text):
        
        pats, repl_string = self.pats_repls
        for pat in pats:
            text=pat.sub(repl_string,text)
            
        return text

    def _init_to_anusvaara_relaxed(self):
        """
        `r1_nasal=re.compile(r'\\u0919\\u094D([\\u0915-\\u0918])')`
        """
            
        nasals_list=[0x19,0x1e,0x23,0x28,0x29,0x2e]    
        nasals_list_str=','.join([langinfo.offset_to_char(x,self.lang) for x in nasals_list])
        
        halant_offset=0x4d    
        anusvaara_offset=0x02    
        
        pat=re.compile(r'[{nasals_list_str}]{halant}'.format(
                nasals_list_str=nasals_list_str,
                halant=langinfo.offset_to_char(halant_offset,self.lang),
            ))
        
        repl_string='{anusvaara}'.format(anusvaara=langinfo.offset_to_char(anusvaara_offset,self.lang))

        self.pats_repls = (pat,repl_string)
    
    def _to_anusvaara_relaxed(self,text):
        pat, repl_string = self.pats_repls
        return pat.sub(repl_string,text)
    

    def _init_to_nasal_consonants(self):
        """
        `r1_nasal=re.compile(r'\\u0919\\u094D([\\u0915-\\u0918])')`
        """
    
        pat_signatures=\
            [
                 [0x19,0x15,0x18],
                 [0x1e,0x1a,0x1d],            
                 [0x23,0x1f,0x22],                        
                 [0x28,0x24,0x27],        
                 [0x29,0x24,0x27],                    
                 [0x2e,0x2a,0x2d],                    
            ]    
        
        halant_offset=0x4d
        anusvaara_offset=0x02 
        
        pats=[]
        repl_strings=[]
        
        for pat_signature in pat_signatures:
            pat=re.compile(r'{anusvaara}([{start_r}-{end_r}])'.format(
                anusvaara=langinfo.offset_to_char(anusvaara_offset,self.lang),
                start_r=langinfo.offset_to_char(pat_signature[1],self.lang),
                end_r=langinfo.offset_to_char(pat_signature[2],self.lang),
            ))
            pats.append(pat)
            repl_string='{nasal}{halant}\\1'.format(
                nasal=langinfo.offset_to_char(pat_signature[0],self.lang),
                halant=langinfo.offset_to_char(halant_offset,self.lang),
                )
            repl_strings.append(repl_string)
    
        self.pats_repls=list(zip(pats,repl_strings))

    def _to_nasal_consonants(self,text):
    
        for pat, repl in self.pats_repls:
            text=pat.sub(repl,text)
            
        return text

    def _init_normalize_nasals(self):

        if self.nasals_mode == 'to_anusvaara_strict':
            self._init_to_anusvaara_strict()
        elif self.nasals_mode == 'to_anusvaara_relaxed':
            self._init_to_anusvaara_relaxed()
        elif self.nasals_mode == 'to_nasal_consonants':
            self._init_to_nasal_consonants()

    def normalize_nasals(self,text): 
        if self.nasals_mode == 'to_anusvaara_strict':
            return self._to_anusvaara_strict(text)
        elif self.nasals_mode == 'to_anusvaara_relaxed':
            return self._to_anusvaara_relaxed(text)
        elif self.nasals_mode == 'to_nasal_consonants':
            return self._to_nasal_consonants(text)
        else:
            return text

    def normalize(self,text):
        """
        Method to be implemented for normalization for each script 
        """
        text=text.replace(NormalizerI.BYTE_ORDER_MARK,'')
        text=text.replace(NormalizerI.BYTE_ORDER_MARK_2,'')
        text=text.replace(NormalizerI.WORD_JOINER,'')
        text=text.replace(NormalizerI.SOFT_HYPHEN,'')

        text=text.replace(NormalizerI.ZERO_WIDTH_SPACE,' ') # ??
        text=text.replace(NormalizerI.NO_BREAK_SPACE,' ')

        text=text.replace(NormalizerI.ZERO_WIDTH_NON_JOINER, '')
        text=text.replace(NormalizerI.ZERO_WIDTH_JOINER,'')


        text=self.normalize_nasals(text)
        return text


    def get_char_stats(self,text):    
        print(len(re.findall(NormalizerI.BYTE_ORDER_MARK,text)))
        print(len(re.findall(NormalizerI.BYTE_ORDER_MARK_2,text)))
        print(len(re.findall(NormalizerI.WORD_JOINER,text)))
        print(len(re.findall(NormalizerI.SOFT_HYPHEN,text)))

        print(len(re.findall(NormalizerI.ZERO_WIDTH_SPACE,text) ))
        print(len(re.findall(NormalizerI.NO_BREAK_SPACE,text)))

        print(len(re.findall(NormalizerI.ZERO_WIDTH_NON_JOINER,text)))
        print(len(re.findall(NormalizerI.ZERO_WIDTH_JOINER,text)))

        #for mobj in re.finditer(NormalizerI.ZERO_WIDTH_NON_JOINER,text):
        #    print text[mobj.start()-10:mobj.end()+10].replace('\n', ' ').replace(NormalizerI.ZERO_WIDTH_NON_JOINER,'').encode('utf-8')
        #print hex(ord(text[mobj.end():mobj.end()+1]))

    def correct_visarga(self,text,visarga_char,char_range):
        text=re.sub(r'([\u0900-\u097f]):','\\1\u0903',text)
        


class DevanagariNormalizer(BaseNormalizer): 
    """
    Normalizer for the Devanagari script. In addition to basic normalization by the super class, 

    * Replaces the composite characters containing nuktas by their decomposed form 
    * replace pipe character '|' by poorna virama character
    * replace colon ':' by visarga if the colon follows a charcter in this script 
    
    """

    NUKTA='\u093C' 

    def __init__(self,lang='hi',remove_nuktas=False,nasals_mode='do_nothing'):
        super(DevanagariNormalizer,self).__init__(lang,remove_nuktas,nasals_mode)

    def normalize(self,text): 

        # common normalization for Indic scripts 
        text=super(DevanagariNormalizer,self).normalize(text)

        # decomposing Nukta based composite characters
        text=text.replace('\u0929','\u0928'+DevanagariNormalizer.NUKTA)
        text=text.replace('\u0931','\u0930'+DevanagariNormalizer.NUKTA)
        text=text.replace('\u0934','\u0933'+DevanagariNormalizer.NUKTA)
        text=text.replace('\u0958','\u0915'+DevanagariNormalizer.NUKTA)
        text=text.replace('\u0959','\u0916'+DevanagariNormalizer.NUKTA)
        text=text.replace('\u095A','\u0917'+DevanagariNormalizer.NUKTA)
        text=text.replace('\u095B','\u091C'+DevanagariNormalizer.NUKTA)
        text=text.replace('\u095C','\u0921'+DevanagariNormalizer.NUKTA)
        text=text.replace('\u095D','\u0922'+DevanagariNormalizer.NUKTA)
        text=text.replace('\u095E','\u092B'+DevanagariNormalizer.NUKTA)
        text=text.replace('\u095F','\u092F'+DevanagariNormalizer.NUKTA)

        if self.remove_nuktas:
            text=text.replace(DevanagariNormalizer.NUKTA,'')

        # replace pipe character for poorna virama 
        text=text.replace('\u007c','\u0964')

        # correct visarga 
        text=re.sub(r'([\u0900-\u097f]):','\\1\u0903',text)

        return text

    def get_char_stats(self,text):
        super(DevanagariNormalizer,self).get_char_stats(text)

        print((len(re.findall('\u0929',text))))
        print((len(re.findall('\u0931',text))))
        print((len(re.findall('\u0934',text))))
        print((len(re.findall('\u0958',text))))
        print((len(re.findall('\u0959',text))))
        print((len(re.findall('\u095A',text))))
        print((len(re.findall('\u095B',text))))
        print((len(re.findall('\u095C',text))))
        print((len(re.findall('\u095D',text))))
        print((len(re.findall('\u095E',text))))
        print((len(re.findall('\u095F',text))))

        #print(len(re.findall(u'\u0928'+DevanagariNormalizer.NUKTA,text)))
        #print(len(re.findall(u'\u0930'+DevanagariNormalizer.NUKTA,text)))
        #print(len(re.findall(u'\u0933'+DevanagariNormalizer.NUKTA,text)))
        #print(len(re.findall(u'\u0915'+DevanagariNormalizer.NUKTA,text)))
        #print(len(re.findall(u'\u0916'+DevanagariNormalizer.NUKTA,text)))
        #print(len(re.findall(u'\u0917'+DevanagariNormalizer.NUKTA,text)))
        #print(len(re.findall(u'\u091C'+DevanagariNormalizer.NUKTA,text)))
        #print(len(re.findall(u'\u0921'+DevanagariNormalizer.NUKTA,text)))
        #print(len(re.findall(u'\u0922'+DevanagariNormalizer.NUKTA,text)))
        #print(len(re.findall(u'\u092B'+DevanagariNormalizer.NUKTA,text)))
        #print(len(re.findall(u'\u092F'+DevanagariNormalizer.NUKTA,text)))

class GurmukhiNormalizer(BaseNormalizer): 
    """
    Normalizer for the Gurmukhi script. In addition to basic normalization by the super class, 

    * Replaces the composite characters containing nuktas by their decomposed form 
    * Replace the reserved character for poorna virama (if used) with the recommended generic Indic scripts poorna virama 
    * replace pipe character '|' by poorna virama character
    * replace colon ':' by visarga if the colon follows a charcter in this script 
    """

    NUKTA='\u0A3C' 

    def __init__(self,lang='pa',remove_nuktas=False,nasals_mode='do_nothing'):
        super(GurmukhiNormalizer,self).__init__(lang,remove_nuktas,nasals_mode)

    def normalize(self,text): 

        # common normalization for Indic scripts 
        text=super(GurmukhiNormalizer,self).normalize(text)

        # decomposing Nukta based composite characters
        text=text.replace('\u0a33','\u0a32'+GurmukhiNormalizer.NUKTA)
        text=text.replace('\u0a36','\u0a38'+GurmukhiNormalizer.NUKTA)
        text=text.replace('\u0a59','\u0a16'+GurmukhiNormalizer.NUKTA)
        text=text.replace('\u0a5a','\u0a17'+GurmukhiNormalizer.NUKTA)
        text=text.replace('\u0a5b','\u0a1c'+GurmukhiNormalizer.NUKTA)
        text=text.replace('\u0a5e','\u0a2b'+GurmukhiNormalizer.NUKTA)

        if self.remove_nuktas:
            text=text.replace(GurmukhiNormalizer.NUKTA,'')

        # replace the poorna virama codes specific to script 
        # with generic Indic script codes
        text=text.replace('\u0a64','\u0964')
        text=text.replace('\u0a65','\u0965')

        ## replace pipe character for poorna virama 
        text=text.replace('\u007c','\u0964')

        # correct visarge 
        text=re.sub(r'([\u0a00-\u0a7f]):','\\1\u0a03',text)

        return text


class GujaratiNormalizer(BaseNormalizer): 
    """
    Normalizer for the Gujarati script. In addition to basic normalization by the super class, 

    * Replace the reserved character for poorna virama (if used) with the recommended generic Indic scripts poorna virama 
    * replace colon ':' by visarga if the colon follows a charcter in this script 
    """

    NUKTA='\u0ABC' 

    def __init__(self,lang='gu',remove_nuktas=False,nasals_mode='do_nothing'):
        super(GujaratiNormalizer,self).__init__(lang,remove_nuktas,nasals_mode)

    def normalize(self,text): 

        # common normalization for Indic scripts 
        text=super(GujaratiNormalizer,self).normalize(text)

        # decomposing Nukta based composite characters
        if self.remove_nuktas:
            text=text.replace(GujaratiNormalizer.NUKTA,'')


        # replace the poorna virama codes specific to script 
        # with generic Indic script codes
        text=text.replace('\u0ae4','\u0964')
        text=text.replace('\u0ae5','\u0965')

        # correct visarge 
        text=re.sub(r'([\u0a80-\u0aff]):','\\1\u0a83',text)

        return text


class OriyaNormalizer(BaseNormalizer): 
    """
    Normalizer for the Oriya script. In addition to basic normalization by the super class, 

    * Replaces the composite characters containing nuktas by their decomposed form 
    * Replace the reserved character for poorna virama (if used) with the recommended generic Indic scripts poorna virama 
    * Canonicalize two part dependent vowels
    * Replace 'va' with 'ba'
    * replace pipe character '|' by poorna virama character
    * replace colon ':' by visarga if the colon follows a charcter in this script 
    """

    NUKTA='\u0B3C' 

    def __init__(self,lang='or',remove_nuktas=False,nasals_mode='do_nothing'):
        super(OriyaNormalizer,self).__init__(lang,remove_nuktas,nasals_mode)

    def normalize(self,text): 

        # common normalization for Indic scripts 
        text=super(OriyaNormalizer,self).normalize(text)

        # decomposing Nukta based composite characters
        text=text.replace('\u0b5c','\u0b21'+OriyaNormalizer.NUKTA)
        text=text.replace('\u0b5d','\u0b22'+OriyaNormalizer.NUKTA)

        if self.remove_nuktas:
            text=text.replace(OriyaNormalizer.NUKTA,'')


        # replace the poorna virama codes specific to script 
        # with generic Indic script codes
        text=text.replace('\u0b64','\u0964')
        text=text.replace('\u0b65','\u0965')

        # replace pipe character for poorna virama 
        text=text.replace('\u007c','\u0964')

        # replace va with ba 
        text=text.replace('\u0b35','\u0b2c')

        # AI dependent vowel sign 
        text=text.replace('\u0b47\u0b56','\u0b58')

        # two part dependent vowels
        text=text.replace('\u0b47\u0b3e','\u0b4b')
        text=text.replace('\u0b47\u0b57','\u0b4c')

        # additional consonant - not clear how to handle this
        # ignore

        # correct visarge 
        text=re.sub(r'([\u0b00-\u0b7f]):','\\1\u0b03',text)

        return text


class BengaliNormalizer(BaseNormalizer): 
    """
    Normalizer for the Bengali script. In addition to basic normalization by the super class, 

    * Replaces the composite characters containing nuktas by their decomposed form 
    * Replace the reserved character for poorna virama (if used) with the recommended generic Indic scripts poorna virama 
    * Canonicalize two part dependent vowels
    * replace pipe character '|' by poorna virama character
    * replace colon ':' by visarga if the colon follows a charcter in this script 

    """

    NUKTA='\u09BC' 

    def __init__(self,lang='bn',remove_nuktas=False,nasals_mode='do_nothing'):
        super(BengaliNormalizer,self).__init__(lang,remove_nuktas,nasals_mode)

    def normalize(self,text): 

        # common normalization for Indic scripts 
        text=super(BengaliNormalizer,self).normalize(text)

        # decomposing Nukta based composite characters
        text=text.replace('\u09dc','\u09a1'+BengaliNormalizer.NUKTA)
        text=text.replace('\u09dd','\u09a2'+BengaliNormalizer.NUKTA)
        text=text.replace('\u09df','\u09af'+BengaliNormalizer.NUKTA)

        if self.remove_nuktas:
            text=text.replace(BengaliNormalizer.NUKTA,'')


        # replace the poorna virama codes specific to script 
        # with generic Indic script codes
        text=text.replace('\u09e4','\u0964')
        text=text.replace('\u09e5','\u0965')

        # replace pipe character for poorna virama 
        text=text.replace('\u007c','\u0964')
        # replace bengali currency numerator four for poorna virama  (it looks similar and is used as a substitute)
        text=text.replace('\u09f7','\u0964')

        # two part dependent vowels
        text=text.replace('\u09c7\u09be','\u09cb')
        text=text.replace('\u09c7\u0bd7','\u0bcc')

        # correct visarge 
        text=re.sub(r'([\u0980-\u09ff]):','\\1\u0983',text)

        return text


class TamilNormalizer(BaseNormalizer): 
    """
    Normalizer for the Tamil script. In addition to basic normalization by the super class, 

    * Replace the reserved character for poorna virama (if used) with the recommended generic Indic scripts poorna virama 
    * canonicalize two-part dependent vowel signs
    * replace colon ':' by visarga if the colon follows a charcter in this script 
    """

    def __init__(self,lang='ta',remove_nuktas=False,nasals_mode='do_nothing'):
        super(TamilNormalizer,self).__init__(lang,remove_nuktas,nasals_mode)

    def normalize(self,text): 

        # common normalization for Indic scripts 
        text=super(TamilNormalizer,self).normalize(text)

        # replace the poorna virama codes specific to script 
        # with generic Indic script codes
        text=text.replace('\u0be4','\u0964')
        text=text.replace('\u0be5','\u0965')

        # two part dependent vowels
        text=text.replace('\u0b92\u0bd7','\u0b94')
        text=text.replace('\u0bc6\u0bbe','\u0bca')
        text=text.replace('\u0bc7\u0bbe','\u0bcb')
        text=text.replace('\u0bc6\u0bd7','\u0bcc')

        # correct visarge 
        text=re.sub(r'([\u0b80-\u0bff]):','\\1\u0b83',text)

        return text


class TeluguNormalizer(BaseNormalizer): 
    """
    Normalizer for the Teluguscript. In addition to basic normalization by the super class, 

    * Replace the reserved character for poorna virama (if used) with the recommended generic Indic scripts poorna virama 
    * canonicalize two-part dependent vowel signs
    * replace colon ':' by visarga if the colon follows a charcter in this script 
    """

    def __init__(self,lang='te',remove_nuktas=False,nasals_mode='do_nothing'):
        super(TeluguNormalizer,self).__init__(lang,remove_nuktas,nasals_mode)

    def normalize(self,text): 

        # common normalization for Indic scripts 
        text=super(TeluguNormalizer,self).normalize(text)

        # replace the poorna virama codes specific to script 
        # with generic Indic script codes
        text=text.replace('\u0c64','\u0964')
        text=text.replace('\u0c65','\u0965')

        # dependent vowels
        text=text.replace('\u0c46\u0c56','\u0c48')

        # correct visarge 
        text=re.sub(r'([\u0c00-\u0c7f]):','\\1\u0c03',text)

        return text

    def get_char_stats(self,text):
        pass 

class KannadaNormalizer(BaseNormalizer): 
    """
    Normalizer for the Kannada script. In addition to basic normalization by the super class, 

    * Replace the reserved character for poorna virama (if used) with the recommended generic Indic scripts poorna virama 
    * canonicalize two-part dependent vowel signs
    * replace colon ':' by visarga if the colon follows a charcter in this script 
    """

    def __init__(self,lang='kn',remove_nuktas=False,nasals_mode='do_nothing'):
        super(KannadaNormalizer,self).__init__(lang,remove_nuktas,nasals_mode)


    def normalize(self,text): 

        # common normalization for Indic scripts 
        text=super(KannadaNormalizer,self).normalize(text)

        # replace the poorna virama codes specific to script 
        # with generic Indic script codes
        text=text.replace('\u0ce4','\u0964')
        text=text.replace('\u0ce5','\u0965')

        # dependent vowels
        text=text.replace('\u0cbf\u0cd5','\u0cc0')
        text=text.replace('\u0cc6\u0cd5','\u0cc7')
        text=text.replace('\u0cc6\u0cd6','\u0cc8')
        text=text.replace('\u0cc6\u0cc2','\u0cca')
        text=text.replace('\u0cca\u0cd5','\u0ccb')

        # correct visarge 
        text=re.sub(r'([\u0c80-\u0cff]):','\\1\u0c83',text)

        return text


class MalayalamNormalizer(BaseNormalizer): 
    """
    Normalizer for the Malayalam script. In addition to basic normalization by the super class, 

    * Replace the reserved character for poorna virama (if used) with the recommended generic Indic scripts poorna virama 
    * canonicalize two-part dependent vowel signs
    * Change from old encoding of chillus (till Unicode 5.0) to new encoding
    * replace colon ':' by visarga if the colon follows a charcter in this script 
    """

    def __init__(self,lang='ml',remove_nuktas=False,nasals_mode='do_nothing'):
        super(MalayalamNormalizer,self).__init__(lang,remove_nuktas,nasals_mode)

    def normalize(self,text): 

        # Change from old encoding of chillus (till Unicode 5.0) to new encoding
        text=text.replace('\u0d23\u0d4d\u200d','\u0d7a')
        text=text.replace('\u0d28\u0d4d\u200d','\u0d7b')
        text=text.replace('\u0d30\u0d4d\u200d','\u0d7c')
        text=text.replace('\u0d32\u0d4d\u200d','\u0d7d')
        text=text.replace('\u0d33\u0d4d\u200d','\u0d7e')
        text=text.replace('\u0d15\u0d4d\u200d','\u0d7f')

        # TODO: Normalize chillus

        # common normalization for Indic scripts 
        text=super(MalayalamNormalizer,self).normalize(text)

        # replace the poorna virama codes specific to script 
        # with generic Indic script codes
        text=text.replace('\u0d64','\u0964')
        text=text.replace('\u0d65','\u0965')

        # dependent vowels
        text=text.replace('\u0d46\u0d3e','\u0d4a')
        text=text.replace('\u0d47\u0d3e','\u0d4b')

        # au forms
        text=text.replace('\u0d46\u0d57','\u0d57')
        text=text.replace('\u0d57','\u0d4c')

        # correct visarge 
        text=re.sub(r'([\u0d00-\u0d7f]):','\\1\u0d03',text)

        return text


class IndicNormalizerFactory(object):
    """
    Factory class to create language specific normalizers. 

    """

    def get_normalizer(self,language,remove_nuktas=False,nasals_mode='do_nothing'):
        """
            Call the get_normalizer function to get the language specific normalizer

            Paramters: 
            |language: language code
            |remove_nuktas: boolean, should the normalizer remove nukta characters 
        """
        normalizer=None
        if language in ['hi','mr','sa','kK','ne','sd']:
            normalizer=DevanagariNormalizer(lang=language, remove_nuktas=remove_nuktas, nasals_mode=nasals_mode)
        elif language in ['pa']:
            normalizer=GurmukhiNormalizer(lang=language, remove_nuktas=remove_nuktas, nasals_mode=nasals_mode)
        elif language in ['gu']:
            normalizer=GujaratiNormalizer(lang=language, remove_nuktas=remove_nuktas, nasals_mode=nasals_mode)
        elif language in ['bn','as']:
            normalizer=BengaliNormalizer(lang=language, remove_nuktas=remove_nuktas, nasals_mode=nasals_mode)
        elif language in ['or']:
            normalizer=OriyaNormalizer(lang=language, remove_nuktas=remove_nuktas, nasals_mode=nasals_mode)
        elif language in ['ml']:
            normalizer=MalayalamNormalizer(lang=language, remove_nuktas=remove_nuktas, nasals_mode=nasals_mode)
        elif language in ['kn']:
            normalizer=KannadaNormalizer(lang=language, remove_nuktas=remove_nuktas, nasals_mode=nasals_mode)
        elif language in ['ta']:
            normalizer=TamilNormalizer(lang=language, remove_nuktas=remove_nuktas, nasals_mode=nasals_mode)
        elif language in ['te']:
            normalizer=TeluguNormalizer(lang=language, remove_nuktas=remove_nuktas, nasals_mode=nasals_mode)
        else:    
            normalizer=BaseNormalizer(lang=language, remove_nuktas=remove_nuktas, nasals_mode=nasals_mode)

        return normalizer    

    def is_language_supported(self,language): 
        """
        Is the language supported?
        """
        if language in ['hi','mr','sa','kK','ne',
                        'pa',
                        'gu',
                        'bn','as',
                        'or',
                        'ml',
                        'kn',
                        'ta',
                        'te']:
            return True
        else:
            return False


if __name__ == '__main__': 

    if len(sys.argv)<4:
        print("Usage: python normalize.py <infile> <outfile> <language> [<replace_nukta(True,False)>] [<normalize_nasals(do_nothing|to_anusvaara_strict|to_anusvaara_relaxed|to_nasal_consonants)>]") 
        sys.exit(1)

    language=sys.argv[3]
    remove_nuktas=False
    normalize_nasals='do_nothing'
    if len(sys.argv)>=5:
        remove_nuktas=bool(sys.argv[4])
    if len(sys.argv)>=6:
        normalize_nasals=sys.argv[5]

    # create normalizer
    factory=IndicNormalizerFactory()
    normalizer=factory.get_normalizer(language,remove_nuktas,normalize_nasals)

    # DO normalization 
    with codecs.open(sys.argv[1],'r','utf-8') as ifile:
        with codecs.open(sys.argv[2],'w','utf-8') as ofile:
            for line in ifile.readlines():
                normalized_line=normalizer.normalize(line)
                ofile.write(normalized_line)
   
    ## gather status about normalization 
    #with codecs.open(sys.argv[1],'r','utf-8') as ifile:
    #    normalizer=DevanagariNormalizer()
    #    text=string.join(ifile.readlines(),sep='')
    #    normalizer.get_char_stats(text)
