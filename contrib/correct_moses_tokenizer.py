import sys
from indicnlp import langinfo
from indicnlp import loader 

if __name__ == '__main__':
    """
        This script corrects the incorrect tokenization done by Moses tokenizer.
        The Moses tokenizer splits on nukta and halant characters
        Usage: python correct_moses_tokenizer.py <infname> <outfname> <langcode>
    """

    loader.load()

    infname=sys.argv[1]
    outfname=sys.argv[2]
    lang=sys.argv[3]

    halant_char=langinfo.offset_to_char(langinfo.HALANTA_OFFSET,lang)
    nukta_char=langinfo.offset_to_char(langinfo.NUKTA_OFFSET,lang)

    with open(infname,'r',encoding='utf-8') as infile, \
         open(outfname,'w',encoding='utf-8') as outfile:
        for line in infile:
            outfile.write(
                    line.replace(
                        ' {} '.format(halant_char), halant_char).replace(
                        ' {} '.format(nukta_char), nukta_char).replace(
                        ' {}{}'.format(nukta_char,halant_char),'{}{}'.format(nukta_char,halant_char))    
                    )
