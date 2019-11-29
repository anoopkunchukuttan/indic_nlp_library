import sys
from indicnlp import common
common.set_resources_path(INDIC_NLP_RESOURCES)

from indicnlp import loader
from indicnlp.normalize import indic_normalize
from indicnlp.transliterate import unicode_transliterate

if __name__ == '__main__': 
    """
    This script transliterates Hindi to Kannada. It removes/remaps 
    characters only found in Hindi. It also adds halanta to words ending
    with consonant - as is the convention in Kannada
    """

    infname=sys.argv[1]  # one sentence/word per line. Sentences should be space-tokenized
    outfname=sys.agv[2]
    loader.load()

    normalizer_factory=indic_normalize.IndicNormalizerFactory()
    normalizer=normalizer_factory.get_normalizer('hi')

    with open(infname,'r',encoding='utf-8') as infile, \
         open(outfname,'w',encoding='utf-8') as outfile:
        for line in infile: 
            line=line.strip()
            line=normalizer.normalize(line)
    
            ## replace chandrabindus with anusvara
            line=line.replace('\u0900','\u0902')
            line=line.replace('\u0901','\u0902')
    
            ### replace chandra e and o diacritics with e and o respectively
            #line=line.replace('\u0945','\u0947')
            #line=line.replace('\u0949','\u094b')
   
            ### replace chandra e and o diacritics with a diacritic
            ## this seems to be general usage
            line=line.replace('\u0945','\u093e')
            line=line.replace('\u0949','\u093e')
   
            ## remove nukta 
            line=line.replace('\u093c','')

            ## add halant if word ends with consonant
            #if isc.is_consonant(isc.get_phonetic_feature_vector(line[-1],'hi')):
            #    line=line+'\u094d'
            words=line.split(' ')
            outwords=[]
            for word in line.split(' '):
                if isc.is_consonant(isc.get_phonetic_feature_vector(word[-1],'hi')):
                    word=word+'\u094d'
            outwords.append(word)
            line=' '.join(outwords)

    
            ## script conversion 
            line=unicode_transliterate.UnicodeIndicTransliterator.transliterate(line,'hi','kn')
            
            outfile.write(line+'\n')


