import argparse 
import sys

from indicnlp import loader
from indicnlp.tokenize import indic_tokenize
from indicnlp.tokenize import indic_detokenize
from indicnlp.normalize import indic_normalize
from indicnlp.morph import unsupervised_morph
from indicnlp.tokenize import sentence_tokenize
from indicnlp.syllable import  syllabifier
from indicnlp.transliterate import unicode_transliterate
from indicnlp.transliterate import script_unifier

DEFAULT_ENCODING='utf-8'

def run_detokenize(args):
    for line in args.infile:
        args.outfile.write(indic_detokenize.trivial_detokenize(line,args.lang))

def run_tokenize(args):
    for line in args.infile:
        args.outfile.write(' '.join(
            indic_tokenize.trivial_tokenize(line,args.lang)))

def run_sentence_split(args):            
    text=' '.join([  l.replace('\n','').replace('\r','') for l in args.infile])
    outlines=sentence_tokenize.sentence_split(text,args.lang)
    for line in outlines:
        args.outfile.write(line+'\n')

def run_normalize(args):

    # TODO: add more options to cli
    remove_nuktas=False
    normalize_nasals='do_nothing'

    # create normalizer
    factory=indic_normalize.IndicNormalizerFactory()
    normalizer=factory.get_normalizer(args.lang,
            remove_nuktas=remove_nuktas,
            nasals_mode=normalize_nasals)

    # DO normalization 
    for line in args.infile:
        normalized_line=normalizer.normalize(line)
        args.outfile.write(normalized_line)

def run_morph(args):

    add_marker=False
    analyzer=unsupervised_morph.UnsupervisedMorphAnalyzer(args.lang,add_marker)
    for line in args.infile:
        morph_tokens=analyzer.morph_analyze_document(line.strip().split(' '))
        args.outfile.write(' '.join(morph_tokens) + '\n')

def run_syllabify(args):
    for line in args.infile:
        new_line = ' '.join(
                        [ ' '.join(syllabifier.orthographic_syllabify(w,args.lang)) 
                                for w in line.strip().split(' ')  ]
                    )
        args.outfile.write(new_line+'\n')

def run_wc(args):
    # if args.l==False and args.w==False and args.c==False:
    #     args.l, args.w, args.c= True, True, True 
    
    nl=0
    nw=0
    nc=0

    for line in args.infile:
        nl+=1
        nw+=len(line.strip(' ').split(' '))
        nc+=len(line)

    print('{} {} {}'.format(nl,nw,nc))

def run_indic2roman(args):
    for line in args.infile:
        transliterated_line=unicode_transliterate.ItransTransliterator.to_itrans(
            line,args.lang)
        args.outfile.write(transliterated_line)      

def run_roman2indic(args):
    for line in args.infile:
        transliterated_line=unicode_transliterate.ItransTransliterator.from_itrans(
            line,args.lang)
        args.outfile.write(transliterated_line)    

def run_script_unify(args):

    unifier=None

    if args.mode=='aggressive':
        unifier=script_unifier.AggressiveScriptUnifier(nasals_mode='to_anusvaara_relaxed', common_lang=args.common_lang)

    elif args.mode=='basic':
        unifier=script_unifier.BasicScriptUnifier(nasals_mode='do_nothing',
                                common_lang=args.common_lang)

    elif args.mode=='naive':
        unifier=script_unifier.NaiveScriptUnifier(common_lang=args.common_lang)

    assert(unifier is not None)

    for line in args.infile:
        transliterated_line=unifier.transform(line,args.lang)
        args.outfile.write(transliterated_line)     

def run_script_convert(args):
    for line in args.infile:
        transliterated_line=unicode_transliterate.UnicodeIndicTransliterator.transliterate(
            line,args.srclang,args.tgtlang)
        args.outfile.write(transliterated_line)    

def add_common_monolingual_args(task_parser):
    task_parser.add_argument('infile', 
                type=argparse.FileType('r',encoding=DEFAULT_ENCODING),
                nargs='?',
                default=sys.stdin,
                help='Input File path',
            )
    task_parser.add_argument('outfile', 
                type=argparse.FileType('w',encoding=DEFAULT_ENCODING),
                nargs='?',
                default=sys.stdout,                
                help='Output File path',
            )
    task_parser.add_argument('-l', '--lang', 
                help='Language',
            )

def add_common_bilingual_args(task_parser):
    task_parser.add_argument('infile', 
                type=argparse.FileType('r',encoding=DEFAULT_ENCODING),
                nargs='?',
                default=sys.stdin,
                help='Input File path',
            )
    task_parser.add_argument('outfile', 
                type=argparse.FileType('w',encoding=DEFAULT_ENCODING),
                nargs='?',
                default=sys.stdout,                
                help='Output File path',
            )
    task_parser.add_argument('-s', '--srclang', 
                help='Source Language',
            )

    task_parser.add_argument('-t', '--tgtlang', 
                help='Target Language',
            )

def add_tokenize_parser(subparsers):
    task_parser=subparsers.add_parser('tokenize', 
                    help='tokenizer help')
    add_common_monolingual_args(task_parser)
    task_parser.set_defaults(func=run_tokenize)

def add_detokenize_parser(subparsers):
    task_parser=subparsers.add_parser('detokenize', 
                    help='de-tokenizer help')
    add_common_monolingual_args(task_parser)
    task_parser.set_defaults(func=run_detokenize)

def add_sentence_split_parser(subparsers):
    task_parser=subparsers.add_parser('sentence_split', help='sentence split help')
    add_common_monolingual_args(task_parser)
    task_parser.set_defaults(func=run_sentence_split)

def add_normalize_parser(subparsers):
    task_parser=subparsers.add_parser('normalize', help='normalizer help')
    add_common_monolingual_args(task_parser)
    task_parser.set_defaults(func=run_normalize)

def add_morph_parser(subparsers):
    task_parser=subparsers.add_parser('morph', help='morph help')
    add_common_monolingual_args(task_parser)
    task_parser.set_defaults(func=run_morph)

def add_syllabify_parser(subparsers):
    task_parser=subparsers.add_parser('syllabify', help='syllabify help')
    add_common_monolingual_args(task_parser)
    task_parser.set_defaults(func=run_syllabify)

def add_wc_parser(subparsers):
    task_parser=subparsers.add_parser('wc', help='wc help')

    task_parser.add_argument('infile', 
                type=argparse.FileType('r',encoding=DEFAULT_ENCODING),
                nargs='?',
                default=sys.stdin,
                help='Input File path',
            )
    # task_parser.add_argument('-l', action='store_true')
    # task_parser.add_argument('-w', action='store_true')
    # task_parser.add_argument('-c', action='store_true')
    # task_parser.set_defaults(l=False)
    # task_parser.set_defaults(w=False)
    # task_parser.set_defaults(c=False)

    task_parser.set_defaults(func=run_wc)    

def add_indic2roman_parser(subparsers):
    task_parser=subparsers.add_parser('indic2roman', help='indic2roman help')
    add_common_monolingual_args(task_parser)
    task_parser.set_defaults(func=run_indic2roman)

def add_roman2indic_parser(subparsers):
    task_parser=subparsers.add_parser('roman2indic', help='roman2indic help')
    add_common_monolingual_args(task_parser)
    task_parser.set_defaults(func=run_indic2roman)

def add_script_unify_parser(subparsers):
    task_parser=subparsers.add_parser('script_unify', help='script_unify help')
    add_common_monolingual_args(task_parser)
    task_parser.add_argument('-m','--mode', 
                default='basic',               
                choices=['naive', 'basic', 'aggressive'] ,
                help='Script unification mode',
            )   
    task_parser.add_argument('-c','--common_lang', 
                default='hi',                
                help='Common language in which all languages are represented',
            )  

    task_parser.set_defaults(func=run_script_unify)    

def add_script_convert_parser(subparsers):
    task_parser=subparsers.add_parser('script_convert', help='script convert help')
    add_common_bilingual_args(task_parser)
    task_parser.set_defaults(func=run_script_convert)

def get_parser():
    parser = argparse.ArgumentParser(prog='indicnlp')
    subparsers = parser.add_subparsers(help='Invoke each operation with one of the subcommands', dest='subcommand')

    add_tokenize_parser(subparsers)
    add_detokenize_parser(subparsers)
    add_sentence_split_parser(subparsers)
    add_normalize_parser(subparsers)

    add_morph_parser(subparsers)
    add_syllabify_parser(subparsers)

    add_wc_parser(subparsers)

    add_indic2roman_parser(subparsers)
    add_roman2indic_parser(subparsers)
    add_script_unify_parser(subparsers)

    add_script_convert_parser(subparsers)

    return parser

def main():
    parser=get_parser()
    args=parser.parse_args()
    # print(args)
    args.func(args)

if __name__ == '__main__':
    loader.load()
    main()

