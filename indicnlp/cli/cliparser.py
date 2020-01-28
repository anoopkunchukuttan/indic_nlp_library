import argparse 
import sys

from indicnlp import loader
from indicnlp.tokenize import indic_tokenize
from indicnlp.tokenize import indic_detokenize
from indicnlp.normalize import indic_normalize
from indicnlp.morph import unsupervised_morph
from indicnlp.tokenize import sentence_tokenize
from indicnlp.syllable import  syllabifier

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
        add_marker=False
        new_line = ' '.join(
                        [ ' '.join(syllabifier.orthographic_syllabify(w,args.lang)) 
                                for w in line.strip().split(' ')  ]
                    )
        args.outfile.write(new_line+'\n')

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


def get_parser():
    parser = argparse.ArgumentParser(prog='indicnlp')
    subparsers = parser.add_subparsers(help='sub-command help', dest='subcommand')
    add_tokenize_parser(subparsers)
    add_detokenize_parser(subparsers)
    add_sentence_split_parser(subparsers)
    add_normalize_parser(subparsers)
    add_morph_parser(subparsers)
    add_syllabify_parser(subparsers)
    return parser

def main():
    parser=get_parser()
    args=parser.parse_args()
    # print(args)
    args.func(args)

if __name__ == '__main__':
    loader.load()
    main()

    # # fmt: off
    # parser.add_argument('--no-progress-bar', action='store_true', help='disable progress bar')
    # parser.add_argument('--log-interval', type=int, default=1000, metavar='N',
    #                     help='log progress every N batches (when progress bar is disabled)')
    # parser.add_argument('--log-format', default=None, help='log format to use',
    #                     choices=['json', 'none', 'simple', 'tqdm'])
    # parser.add_argument('--tensorboard-logdir', metavar='DIR', default='',
    #                     help='path to save logs for tensorboard, should match --logdir '
    #                          'of running tensorboard (default: no tensorboard logging)')
    # parser.add_argument('--seed', default=1, type=int, metavar='N',
    #                     help='pseudo random number generator seed')
    # parser.add_argument('--cpu', action='store_true', help='use CPU instead of CUDA')
    # parser.add_argument('--fp16', action='store_true', help='use FP16')
    # parser.add_argument('--memory-efficient-fp16', action='store_true',
    #                     help='use a memory-efficient version of FP16 training; implies --fp16')
    # parser.add_argument('--fp16-no-flatten-grads', action='store_true',
    #                     help='don\'t flatten FP16 grads tensor')
    # parser.add_argument('--fp16-init-scale', default=2 ** 7, type=int,
    #                     help='default FP16 loss scale')
    # parser.add_argument('--fp16-scale-window', type=int,
    #                     help='number of updates before increasing loss scale')
    # parser.add_argument('--fp16-scale-tolerance', default=0.0, type=float,
    #                     help='pct of updates that can overflow before decreasing the loss scale')
    # parser.add_argument('--min-loss-scale', default=1e-4, type=float, metavar='D',
    #                     help='minimum FP16 loss scale, after which training is stopped')
    # parser.add_argument('--threshold-loss-scale', type=float,
    #                     help='threshold FP16 loss scale from below')
    # parser.add_argument('--user-dir', default=None,
    #                     help='path to a python module containing custom extensions (tasks and/or architectures)')
    # parser.add_argument('--empty-cache-freq', default=0, type=int,
    #                     help='how often to clear the PyTorch CUDA cache (0 to disable)')
    # parser.add_argument('--all-gather-list-size', default=16384, type=int,
    #                     help='number of bytes reserved for gathering stats from workers')

