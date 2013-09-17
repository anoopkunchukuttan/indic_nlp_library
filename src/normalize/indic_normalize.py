# Program for normalization of text written in Unicode. This is mainly geared towards Indic scripts 
#
# @author Anoop Kunchukuttan 
#

import sys, codecs, string, itertools, re

class NormalizerI(object):
    """
    Base class for normalizer. Performs some common normalization, which includes: 
        - Byte order mark, word joiner, etc. removal 
        - ZERO_WIDTH_NON_JOINER and ZERO_WIDTH_JOINER removal 
        - ZERO_WIDTH_SPACE and NO_BREAK_SPACE replaced by spaces 

    Script specific normalizers should derive from this class and override the normalize() method. 
    They can call the super class 'normalize() method to avail of the common normalization 

    """

    BYTE_ORDER_MARK=u'\uFEFF'
    BYTE_ORDER_MARK_2=u'\uFFFE'
    WORD_JOINER=u'\u2060'
    SOFT_HYPHEN=u'\u00AD'

    ZERO_WIDTH_SPACE=u'\u200B'
    NO_BREAK_SPACE=u'\u00A0'

    ZERO_WIDTH_NON_JOINER=u'\u200C'
    ZERO_WIDTH_JOINER=u'\u200D'

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


class DevanagariNormalizer(NormalizerI): 
    """
    Normalizer for the Devanagari script. In addition to basic normalization by the super class, 
    - Replaces the composite characters containing nuktas by their decomposed form 
    
    """

    NUKTA=u'\u093C' 

    def __init__(self,remove_nuktas=False):
        self.remove_nuktas=remove_nuktas

    def normalize(self,text): 

        # common normalization for Indic scripts 
        text=super(DevanagariNormalizer,self).normalize(text)

        # decomposing Nukta based composite characters
        text=text.replace(u'\u0929',u'\u0928'+DevanagariNormalizer.NUKTA)
        text=text.replace(u'\u0931',u'\u0930'+DevanagariNormalizer.NUKTA)
        text=text.replace(u'\u0934',u'\u0933'+DevanagariNormalizer.NUKTA)
        text=text.replace(u'\u0958',u'\u0915'+DevanagariNormalizer.NUKTA)
        text=text.replace(u'\u0959',u'\u0916'+DevanagariNormalizer.NUKTA)
        text=text.replace(u'\u095A',u'\u0917'+DevanagariNormalizer.NUKTA)
        text=text.replace(u'\u095B',u'\u091C'+DevanagariNormalizer.NUKTA)
        text=text.replace(u'\u095C',u'\u0921'+DevanagariNormalizer.NUKTA)
        text=text.replace(u'\u095D',u'\u0922'+DevanagariNormalizer.NUKTA)
        text=text.replace(u'\u095E',u'\u092B'+DevanagariNormalizer.NUKTA)
        text=text.replace(u'\u095F',u'\u092F'+DevanagariNormalizer.NUKTA)

        if self.remove_nuktas:
            text=text.replace(DevanagariNormalizer.NUKTA,'')
            
        return text

    def get_char_stats(self,text):
        super(DevanagariNormalizer,self).get_char_stats(text)

        print(len(re.findall(u'\u0929',text)))
        print(len(re.findall(u'\u0931',text)))
        print(len(re.findall(u'\u0934',text)))
        print(len(re.findall(u'\u0958',text)))
        print(len(re.findall(u'\u0959',text)))
        print(len(re.findall(u'\u095A',text)))
        print(len(re.findall(u'\u095B',text)))
        print(len(re.findall(u'\u095C',text)))
        print(len(re.findall(u'\u095D',text)))
        print(len(re.findall(u'\u095E',text)))
        print(len(re.findall(u'\u095F',text)))

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

        #print(u'\u0929')
        #print(u'\u0931')
        #print(u'\u0934')
        #print(u'\u0958')
        #print(u'\u0959')
        #print(u'\u095A')
        #print(u'\u095B')
        #print(u'\u095C')
        #print(u'\u095D')
        #print(u'\u095E')
        #print(u'\u095F')

class GurmukhiNormalizer(NormalizerI): 
    """
    Normalizer for the Gurmukhi script. In addition to basic normalization by the super class, 
    - Replaces the composite characters containing nuktas by their decomposed form 
    - Replace the reserved character for poorna virama (if used) with the 
    recommended generic Indic scripts poorna virama 
    """

    NUKTA=u'\u0A3C' 

    def __init__(self,remove_nuktas=False):
        self.remove_nuktas=remove_nuktas

    def normalize(self,text): 

        # common normalization for Indic scripts 
        text=super(GurmukhiNormalizer,self).normalize(text)

        # decomposing Nukta based composite characters
        text=text.replace(u'\u0a33',u'\u0a32'+GurmukhiNormalizer.NUKTA)
        text=text.replace(u'\u0a36',u'\u0a38'+GurmukhiNormalizer.NUKTA)
        text=text.replace(u'\u0a59',u'\u0a16'+GurmukhiNormalizer.NUKTA)
        text=text.replace(u'\u0a5a',u'\u0a17'+GurmukhiNormalizer.NUKTA)
        text=text.replace(u'\u0a5b',u'\u0a1c'+GurmukhiNormalizer.NUKTA)
        text=text.replace(u'\u0a5e',u'\u0a2b'+GurmukhiNormalizer.NUKTA)

        if self.remove_nuktas:
            text=text.replace(GurmukhiNormalizer.NUKTA,'')

        # replace the poorna virama codes specific to script 
        # with generic Indic script codes
        text=text.replace(u'\u0a64',u'\u0964')
        text=text.replace(u'\u0a65',u'\u0965')

        return text


class GujaratiNormalizer(NormalizerI): 
    """
    Normalizer for the Gujarati script. In addition to basic normalization by the super class, 
    - Replace the reserved character for poorna virama (if used) with the 
    recommended generic Indic scripts poorna virama 
    """

    NUKTA=u'\u0ABC' 

    def __init__(self,remove_nuktas=False):
        self.remove_nuktas=remove_nuktas

    def normalize(self,text): 

        # common normalization for Indic scripts 
        text=super(GujaratiNormalizer,self).normalize(text)

        # decomposing Nukta based composite characters
        if self.remove_nuktas:
            text=text.replace(GujaratiNormalizer.NUKTA,'')


        # replace the poorna virama codes specific to script 
        # with generic Indic script codes
        text=text.replace(u'\u0ae4',u'\u0964')
        text=text.replace(u'\u0ae5',u'\u0965')

        return text


class OriyaNormalizer(NormalizerI): 
    """
    Normalizer for the Oriya script. In addition to basic normalization by the super class, 
    - Replaces the composite characters containing nuktas by their decomposed form 
    - Replace the reserved character for poorna virama (if used) with the 
    recommended generic Indic scripts poorna virama 
    - Canonicalize two part dependent vowels
    - Replace 'va' with 'ba'
    """

    NUKTA=u'\u0B3C' 

    def __init__(self,remove_nuktas=False):
        self.remove_nuktas=remove_nuktas

    def normalize(self,text): 

        # common normalization for Indic scripts 
        text=super(OriyaNormalizer,self).normalize(text)

        # decomposing Nukta based composite characters
        text=text.replace(u'\u0b5c',u'\u0b21'+OriyaNormalizer.NUKTA)
        text=text.replace(u'\u0b5d',u'\u0b22'+OriyaNormalizer.NUKTA)

        if self.remove_nuktas:
            text=text.replace(OriyaNormalizer.NUKTA,'')


        # replace the poorna virama codes specific to script 
        # with generic Indic script codes
        text=text.replace(u'\u0b64',u'\u0964')
        text=text.replace(u'\u0b65',u'\u0965')

        # replace va with ba 
        text=text.replace(u'\u0b35',u'\u0b2c')

        # AI dependent vowel sign 
        text=text.replace(u'\u0b47\u0b56',u'\u0b58')

        # two part dependent vowels
        text=text.replace(u'\u0b47\u0b3e',u'\u0b4b')
        text=text.replace(u'\u0b47\u0b57',u'\u0b4c')

        # additional consonant - not clear how to handle this
        # ignore

        return text


class BengaliNormalizer(NormalizerI): 
    """
    Normalizer for the Bengali script. In addition to basic normalization by the super class, 
    - Replaces the composite characters containing nuktas by their decomposed form 
    - Replace the reserved character for poorna virama (if used) with the 
    recommended generic Indic scripts poorna virama 
    - Canonicalize two part dependent vowels
    """

    NUKTA=u'\u09BC' 

    def __init__(self,remove_nuktas=False):
        self.remove_nuktas=remove_nuktas

    def normalize(self,text): 

        # common normalization for Indic scripts 
        text=super(BengaliNormalizer,self).normalize(text)

        # decomposing Nukta based composite characters
        text=text.replace(u'\u09dc',u'\u09a1'+BengaliNormalizer.NUKTA)
        text=text.replace(u'\u09dd',u'\u09a2'+BengaliNormalizer.NUKTA)
        text=text.replace(u'\u09df',u'\u09af'+BengaliNormalizer.NUKTA)

        if self.remove_nuktas:
            text=text.replace(BengaliNormalizer.NUKTA,'')


        # replace the poorna virama codes specific to script 
        # with generic Indic script codes
        text=text.replace(u'\u09e4',u'\u0964')
        text=text.replace(u'\u09e5',u'\u0965')

        # two part dependent vowels
        text=text.replace(u'\u09c7\u09be',u'\u09cb')
        text=text.replace(u'\u09c7\u0bd7',u'\u0bcc')

        return text


class TamilNormalizer(NormalizerI): 
    """
    Normalizer for the Tamil script. In addition to basic normalization by the super class, 
    - Replace the reserved character for poorna virama (if used) with the 
    recommended generic Indic scripts poorna virama 
    - canonicalize two-part dependent vowel signs
    """

    def normalize(self,text): 

        # common normalization for Indic scripts 
        text=super(TamilNormalizer,self).normalize(text)

        # replace the poorna virama codes specific to script 
        # with generic Indic script codes
        text=text.replace(u'\u0be4',u'\u0964')
        text=text.replace(u'\u0be5',u'\u0965')

        # two part dependent vowels
        text=text.replace(u'\u0b92\u0bd7',u'\u0b94')
        text=text.replace(u'\u0bc6\u0bbe',u'\u0bca')
        text=text.replace(u'\u0bc7\u0bbe',u'\u0bcb')
        text=text.replace(u'\u0bc6\u0bd7',u'\u0bcc')

        return text


class TeluguNormalizer(NormalizerI): 
    """
    Normalizer for the Teluguscript. In addition to basic normalization by the super class, 
    - Replace the reserved character for poorna virama (if used) with the 
    recommended generic Indic scripts poorna virama 
    - canonicalize two-part dependent vowel signs
    """

    def __init__(self,remove_nuktas=False):
        self.remove_nuktas=remove_nuktas

    def normalize(self,text): 

        # common normalization for Indic scripts 
        text=super(TeluguNormalizer,self).normalize(text)

        # replace the poorna virama codes specific to script 
        # with generic Indic script codes
        text=text.replace(u'\u0c64',u'\u0964')
        text=text.replace(u'\u0c65',u'\u0965')

        # dependent vowels
        text=text.replace(u'\u0c46\u0c56',u'\u0c48')

        return text

    def get_char_stats(self,text):
        pass 

class KannadaNormalizer(NormalizerI): 
    """
    Normalizer for the Kannada script. In addition to basic normalization by the super class, 
    - Replace the reserved character for poorna virama (if used) with the 
    recommended generic Indic scripts poorna virama 
    - canonicalize two-part dependent vowel signs
    """

    def normalize(self,text): 

        # common normalization for Indic scripts 
        text=super(KannadaNormalizer,self).normalize(text)

        # replace the poorna virama codes specific to script 
        # with generic Indic script codes
        text=text.replace(u'\u0ce4',u'\u0964')
        text=text.replace(u'\u0ce5',u'\u0965')

        # dependent vowels
        text=text.replace(u'\u0cbf\u0cd5',u'\u0cc0')
        text=text.replace(u'\u0cc6\u0cd5',u'\u0cc7')
        text=text.replace(u'\u0cc6\u0cd6',u'\u0cc8')
        text=text.replace(u'\u0cc6\u0cc2',u'\u0cca')
        text=text.replace(u'\u0cca\u0cd5',u'\u0ccb')

        return text


class MalayalamNormalizer(NormalizerI): 
    """
    Normalizer for the Malayalam script. In addition to basic normalization by the super class, 
    - Replace the reserved character for poorna virama (if used) with the 
    recommended generic Indic scripts poorna virama 
    - canonicalize two-part dependent vowel signs
    """

    def normalize(self,text): 

        # common normalization for Indic scripts 
        text=super(MalayalamNormalizer,self).normalize(text)

        # replace the poorna virama codes specific to script 
        # with generic Indic script codes
        text=text.replace(u'\u0d64',u'\u0964')
        text=text.replace(u'\u0d65',u'\u0965')

        # dependent vowels
        text=text.replace(u'\u0d46\u0d3e',u'\u0d4a')
        text=text.replace(u'\u0d47\u0d3e',u'\u0d4b')

        # au forms
        text=text.replace(u'\u0d46\u0d57',u'\u0d57')
        text=text.replace(u'\u0d57',u'\u0d4c')

        return text


class IndicNormalizerFactory(object):
    def get_normalizer(self,language,remove_nuktas=False):
        normalizer=None
        if language in ['hi','mr','sa','kK','ne']:
            normalizer=DevanagariNormalizer(remove_nuktas)
        elif language in ['pa']:
            normalizer=GurmukhiNormalizer(remove_nuktas)
        elif language in ['gu']:
            normalizer=GujaratiNormalizer(remove_nuktas)
        elif language in ['bn','as']:
            normalizer=BengaliNormalizer(remove_nuktas)
        elif language in ['or']:
            normalizer=OriyaNormalizer(remove_nuktas)
        elif language in ['ml']:
            normalizer=MalayalamNormalizer()
        elif language in ['kn']:
            normalizer=KannadaNormalizer()
        elif language in ['ta']:
            normalizer=TamilNormalizer()
        elif language in ['te']:
            normalizer=TeluguNormalizer()
        else:    
            normalizer=NormalizerI()

        return normalizer    

    def is_language_supported(self,language): 
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
        print "Usage: python normalize.py <infile> <outfile> <language> [<replace_nukta(True,False>]"
        sys.exit(1)

    language=sys.argv[3]
    remove_nuktas=False
    if len(sys.argv)>=5:
        remove_nuktas=bool(sys.argv[4])

    # create normalizer
    factory=IndicNormalizerFactory()
    normalizer=factory.get_normalizer(language,remove_nuktas)

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
