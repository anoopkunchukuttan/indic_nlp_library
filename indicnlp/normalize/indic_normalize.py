# -*- coding: utf-8 -*-

# 
#  Copyright (c) 2013-present, Anoop Kunchukuttan
#  All rights reserved.
#  
#  This source code is licensed under the MIT license found in the
#  LICENSE file in the root directory of this source tree.
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

    def _normalize_punctuations(self, text):
        """
        Normalize punctuations. 
        Applied many of the punctuation normalizations that are part of MosesNormalizer 
        from sacremoses
        """
        text=text.replace(NormalizerI.BYTE_ORDER_MARK,'')
        text=text.replace('„', r'"')
        text=text.replace('“', r'"')
        text=text.replace('”', r'"')
        text=text.replace('–', r'-')
        text=text.replace('—', r' - ')
        text=text.replace('´', r"'")
        text=text.replace('‘', r"'")
        text=text.replace('‚', r"'")
        text=text.replace('’', r"'")
        text=text.replace("''", r'"')
        text=text.replace('´´', r'"')
        text=text.replace('…', r'...')

        return text

    def normalize(self,text):
        pass 


class BaseNormalizer(NormalizerI):

    def __init__(self,lang,
            remove_nuktas=False,
            nasals_mode='do_nothing',
            do_normalize_chandras=False,
            do_normalize_vowel_ending=False):

        self.lang=lang
        self.remove_nuktas=remove_nuktas
        self.nasals_mode=nasals_mode
        self.do_normalize_chandras=do_normalize_chandras
        self.do_normalize_vowel_ending=do_normalize_vowel_ending

        self._init_normalize_chandras()
        self._init_normalize_nasals()
        self._init_normalize_vowel_ending()
        #self._init_visarga_correction()
        
    def _init_normalize_vowel_ending(self):

        if self.lang in langinfo.IE_LANGUAGES:
            self.fn_vowel_ending=self._normalize_word_vowel_ending_ie
        elif self.lang in langinfo.DRAVIDIAN_LANGUAGES:
            self.fn_vowel_ending=self._normalize_word_vowel_ending_dravidian
        else:
            self.fn_vowel_ending=lambda x: x

    def _init_normalize_chandras(self):

        substitution_offsets =\
            [
                [0x0d , 0x0f], # chandra e, independent
                [0x11 , 0x13], # chandra o, independent
                [0x45 , 0x47], # chandra e , 0xde],pendent
                [0x49 , 0x4b], # chandra o , 0xde],pendent
                # [0x72 , 0x0f], # mr: chandra e, independent

                [0x00 , 0x02], # chandrabindu
                [0x01 , 0x02], # chandrabindu
            ]

        self.chandra_substitutions =  [ 
                (langinfo.offset_to_char(x[0],self.lang), langinfo.offset_to_char(x[1],self.lang)) 
                    for x in substitution_offsets ]

    def _normalize_chandras(self,text):
        for match, repl in self.chandra_substitutions:
            text=text.replace(match,repl)
        return text

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

    def _normalize_nasals(self,text): 
        if self.nasals_mode == 'to_anusvaara_strict':
            return self._to_anusvaara_strict(text)
        elif self.nasals_mode == 'to_anusvaara_relaxed':
            return self._to_anusvaara_relaxed(text)
        elif self.nasals_mode == 'to_nasal_consonants':
            return self._to_nasal_consonants(text)
        else:
            return text

    
    def _normalize_word_vowel_ending_dravidian(self,word):
        """
        for Dravidian
        - consonant ending: add 'a' ki maatra
        - halant ending: no change
        - 'a' ki maatra: no change
        """
        if len(word)>0 and langinfo.is_consonant(word[-1],self.lang):
            return word+langinfo.offset_to_char(0x3e,self.lang)
        else:
            return word

    def _normalize_word_vowel_ending_ie(self,word):
        """
        for IE
        - consonant ending: add halant
        - halant ending: no change
        - 'a' ki maatra: no change
        """
        if len(word)>0 and langinfo.is_consonant(word[-1],self.lang):
            return word+langinfo.offset_to_char(langinfo.HALANTA_OFFSET,self.lang)
        else:
            return word 

    def _normalize_vowel_ending(self,text):
        return ' '.join([ self.fn_vowel_ending(w) for w in text.split(' ') ])

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
        
        text=self._normalize_punctuations(text)

        if self.do_normalize_chandras:
            text=self._normalize_chandras(text)
        text=self._normalize_nasals(text)
        if self.do_normalize_vowel_ending:
            text=self._normalize_vowel_ending(text)
        
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

    def __init__(self,lang='hi',remove_nuktas=False,nasals_mode='do_nothing',
            do_normalize_chandras=False,do_normalize_vowel_ending=False):
        super(DevanagariNormalizer,self).__init__(lang,remove_nuktas,nasals_mode,do_normalize_chandras,do_normalize_vowel_ending)

    def normalize(self,text): 

        # common normalization for Indic scripts 
        text=super(DevanagariNormalizer,self).normalize(text)

        # chandra a replacement for Marathi
        text=text.replace('\u0972','\u090f')

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

    VOWEL_NORM_MAPS={
        ## http://www.unicode.org/versions/Unicode12.1.0/ch12.pdf
        ## Table 12-16
        '\u0a05\u0a3e': '\u0a06',
        '\u0a72\u0a3f': '\u0a07',
        '\u0a72\u0a40': '\u0a08',
        '\u0a73\u0a41': '\u0a09',
        '\u0a73\u0a42': '\u0a0a',
        '\u0a72\u0a47': '\u0a0f',
        '\u0a05\u0a48': '\u0a10',
        '\u0a73\u0a4b': '\u0a13',
        '\u0a05\u0a4c': '\u0a14',            
    }

    def __init__(self,lang='pa',remove_nuktas=False,nasals_mode='do_nothing',do_normalize_chandras=False,
                do_normalize_vowel_ending=False,
                do_canonicalize_addak=False, 
                do_canonicalize_tippi=False, 
                do_replace_vowel_bases=False):
        super(GurmukhiNormalizer,self).__init__(lang,remove_nuktas,nasals_mode,do_normalize_chandras,do_normalize_vowel_ending)
        self.do_canonicalize_addak=do_canonicalize_addak
        self.do_canonicalize_tippi=do_canonicalize_tippi
        self.do_replace_vowel_bases=do_replace_vowel_bases


    def _normalize_vowels(self,text):
        """
        """

        ## standard vowel replacements as per suggestions in 
        ## http://www.unicode.org/versions/Unicode12.1.0/ch12.pdf
        ## Table 12-16

        for k,v in GurmukhiNormalizer.VOWEL_NORM_MAPS.items():
            text=text.replace(k,v)
        
        ## the above mappings should account for majority of the variantions, 
        ## Rest are handled via this generic rule which looks at the diacritic 
        ## following the 2 special characters 
        ## TBD: don't see evidence for this in Wikipedia corpus

        ## If these special characters occur without any diacritic, replace them with closet
        ## equivalent vowels
        if self.do_replace_vowel_bases:
            text=text.replace('\u0a72','\u0a07')
            text=text.replace('\u0a73','\u0a09')

        return text


    def normalize(self,text): 

        # Addak
        if self.do_canonicalize_addak:
            ## replace addak+consonant with consonat+halant+consonant
            text=re.sub(r'\u0a71(.)','\\1\u0a4d\\1',text)
            
        # Tippi 
        if self.do_canonicalize_tippi:
            text=text.replace('\u0a70','\u0a02') 

        # Vowels: Gurumuki has multiple ways of representing independent vowels due
        # to the characters 'iri' and 'ura'. 
        text=self._normalize_vowels(text)

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

    def __init__(self,lang='gu',remove_nuktas=False,nasals_mode='do_nothing',do_normalize_chandras=False,
                    do_normalize_vowel_ending=False):
        super(GujaratiNormalizer,self).__init__(lang,remove_nuktas,nasals_mode,do_normalize_chandras,do_normalize_vowel_ending)

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

    VOWEL_NORM_MAPS={
        ## See Table 12-22 in http://www.unicode.org/versions/Unicode12.1.0/ch12.pdf
        '\u0b05\u0b3e': '\u0b06',
        '\u0b0f\u0b57': '\u0b10',
        '\u0b13\u0b57': '\u0b14',
    }


    def __init__(self,lang='or',remove_nuktas=False,nasals_mode='do_nothing',do_normalize_chandras=False,
                do_normalize_vowel_ending=False,
                do_remap_wa=False):
        super(OriyaNormalizer,self).__init__(lang,remove_nuktas,nasals_mode,do_normalize_chandras,do_normalize_vowel_ending)
        self.do_remap_wa=do_remap_wa

    def normalize(self,text): 

        # common normalization for Indic scripts 
        text=super(OriyaNormalizer,self).normalize(text)

        ## standard vowel replacements as per suggestions in Unicode documents
        for k,v in OriyaNormalizer.VOWEL_NORM_MAPS.items():
            text=text.replace(k,v)

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
        text=text.replace('\u0b7c','\u0964')

        # replace wa with ba 
        if self.do_remap_wa:
            text=text.replace('\u0b71','\u0b2c')

        # replace va with ba 
        # NOTE: documentation (chapter on Indic scripts) and codepoint chart seem contradictory 
        # (this applied to wa to ba rule also above)
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

    def __init__(self,lang='bn',remove_nuktas=False,nasals_mode='do_nothing',do_normalize_chandras=False,
                    do_normalize_vowel_ending=False,
                    do_remap_assamese_chars=False):
        super(BengaliNormalizer,self).__init__(lang,remove_nuktas,nasals_mode,do_normalize_chandras,do_normalize_vowel_ending)
        self.do_remap_assamese_chars=do_remap_assamese_chars

    def normalize(self,text):

        # common normalization for Indic scripts 
        text=super(BengaliNormalizer,self).normalize(text)

        # decomposing Nukta based composite characters
        text=text.replace('\u09dc','\u09a1'+BengaliNormalizer.NUKTA)
        text=text.replace('\u09dd','\u09a2'+BengaliNormalizer.NUKTA)
        text=text.replace('\u09df','\u09af'+BengaliNormalizer.NUKTA)

        if self.remove_nuktas:
            text=text.replace(BengaliNormalizer.NUKTA,'')

        if self.do_remap_assamese_chars and self.lang=='as':
            text=text.replace('\u09f0','\u09b0')  #  'ra' character
            text=text.replace('\u09f1','\u09ac')  #  'va' character 

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
        text=text.replace('\u09c7\u09d7','\u09cc')

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

    def __init__(self,lang='ta',remove_nuktas=False,nasals_mode='do_nothing',
            do_normalize_chandras=False,do_normalize_vowel_ending=False):
        super(TamilNormalizer,self).__init__(lang,remove_nuktas,nasals_mode,do_normalize_chandras,do_normalize_vowel_ending)

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

    def __init__(self,lang='te',remove_nuktas=False,nasals_mode='do_nothing',
                do_normalize_chandras=False,do_normalize_vowel_ending=False):
        super(TeluguNormalizer,self).__init__(lang,remove_nuktas,nasals_mode,do_normalize_chandras,do_normalize_vowel_ending)

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

    def __init__(self,lang='kn',remove_nuktas=False,nasals_mode='do_nothing',
            do_normalize_chandras=False,do_normalize_vowel_ending=False):
        super(KannadaNormalizer,self).__init__(lang,remove_nuktas,nasals_mode,do_normalize_chandras,do_normalize_vowel_ending)


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

    CHILLU_CHAR_MAP= {
                    '\u0d7a': '\u0d23', 
                    '\u0d7b': '\u0d28',
                    '\u0d7c': '\u0d30',
                    '\u0d7d': '\u0d32',
                    '\u0d7e': '\u0d33',
                    '\u0d7f': '\u0d15',
                 }

    def _canonicalize_chillus(self,text):
        for chillu, char in MalayalamNormalizer.CHILLU_CHAR_MAP.items(): 
            text=text.replace(chillu,'{}\u0d4d'.format(char)) 
        return text

    def _correct_geminated_T(self,text):
        return text.replace('\u0d31\u0d4d\u0d31','\u0d1f\u0d4d\u0d1f')

    def __init__(self,lang='ml',remove_nuktas=False,nasals_mode='do_nothing',do_normalize_chandras=False,
                do_normalize_vowel_ending=False,
                do_canonicalize_chillus=False, do_correct_geminated_T=False):
        super(MalayalamNormalizer,self).__init__(lang,remove_nuktas,nasals_mode,do_normalize_chandras,do_normalize_vowel_ending)
        self.do_canonicalize_chillus=do_canonicalize_chillus
        self.do_correct_geminated_T=do_correct_geminated_T

    def normalize(self,text): 

        # Change from old encoding of chillus (till Unicode 5.0) to new encoding
        text=text.replace('\u0d23\u0d4d\u200d','\u0d7a')
        text=text.replace('\u0d28\u0d4d\u200d','\u0d7b')
        text=text.replace('\u0d30\u0d4d\u200d','\u0d7c')
        text=text.replace('\u0d32\u0d4d\u200d','\u0d7d')
        text=text.replace('\u0d33\u0d4d\u200d','\u0d7e')
        text=text.replace('\u0d15\u0d4d\u200d','\u0d7f')

        # Normalize chillus
        if self.do_canonicalize_chillus:
            text=self._canonicalize_chillus(text)

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
        text=text.replace('\u0d46\u0d57','\u0d4c')
        text=text.replace('\u0d57','\u0d4c')

        # correct geminated T
        if self.do_correct_geminated_T:
            text=self._correct_geminated_T(text)

        # correct visarga 
        text=re.sub(r'([\u0d00-\u0d7f]):','\\1\u0d03',text)

        return text

class UrduNormalizer(NormalizerI):
    '''Uses UrduHack library.
    https://docs.urduhack.com/en/stable/_modules/urduhack/normalization/character.html#normalize
    '''

    def __init__(self, lang, remove_nuktas=True):
        self.lang = lang
        self.remove_nuktas = remove_nuktas
    
        from urduhack.normalization import (
            remove_diacritics,
            normalize_characters,
            normalize_combine_characters
        ) # TODO: Use only required normalizers
        from urduhack.preprocessing import (
            normalize_whitespace,
            digits_space,
            all_punctuations_space,
            english_characters_space
        )
        self.normalize_whitespace = normalize_whitespace
        self.digits_space = digits_space
        self.all_punctuations_space = all_punctuations_space
        self.english_characters_space = english_characters_space

        self.remove_diacritics = remove_diacritics
        self.normalize_characters = normalize_characters
        self.normalize_combine_characters = normalize_combine_characters

    def normalize(self, text):
        text = self._normalize_punctuations(text)
        text = self.normalize_whitespace(text)
        if self.remove_nuktas:
            text = self.remove_diacritics(text)
        text = self.normalize_characters(text)
        text = self.normalize_combine_characters(text)
        text = self.digits_space(text)
        text = self.all_punctuations_space(text)
        text = self.english_characters_space(text)
        return text


class IndicNormalizerFactory(object):
    """
    Factory class to create language specific normalizers. 
    """

    def get_normalizer(self,language,**kwargs):
        """
            Call the get_normalizer function to get the language specific normalizer
            Paramters: 
            |language: language code
            |remove_nuktas: boolean, should the normalizer remove nukta characters 
        """
        normalizer=None
        if language in ['hi','mr','sa','kK','ne','sd']:
            normalizer=DevanagariNormalizer(lang=language, **kwargs)
        elif language in ['ur']:
            normalizer = UrduNormalizer(lang=language, **kwargs)
        elif language in ['pa']:
            normalizer=GurmukhiNormalizer(lang=language, **kwargs)
        elif language in ['gu']:
            normalizer=GujaratiNormalizer(lang=language, **kwargs)
        elif language in ['bn']:
            normalizer=BengaliNormalizer(lang=language, **kwargs)
        elif language in ['as']:
            normalizer=BengaliNormalizer(lang=language, **kwargs)
        elif language in ['or']:
            normalizer=OriyaNormalizer(lang=language, **kwargs)
        elif language in ['ml']:
            normalizer=MalayalamNormalizer(lang=language, **kwargs)
        elif language in ['kn']:
            normalizer=KannadaNormalizer(lang=language, **kwargs)
        elif language in ['ta']:
            normalizer=TamilNormalizer(lang=language, **kwargs)
        elif language in ['te']:
            normalizer=TeluguNormalizer(lang=language, **kwargs)
        else:    
            normalizer=BaseNormalizer(lang=language, **kwargs)

        return normalizer    

    def is_language_supported(self,language): 
        """
        Is the language supported?
        """
        if language in ['hi','mr','sa','kK','ne','sd',
                        'ur',
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
    normalizer=factory.get_normalizer(language,remove_nuktas=remove_nuktas,nasals_mode=normalize_nasals)

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
