import argparse 

def run_tokenize(args):
    print('hello tokenize')
    print('Sub-command: {}'.format(args.subcommand))
    args.outfile.write(args.infile.read())

def run_normalize(args):
    print('hello normalize')
    print('Sub-command: {}'.format(args.subcommand))

def add_tokenize_parser(subparsers):
    task_parser=subparsers.add_parser('tokenize', 
                    help='tokenizer help')

    task_parser.add_argument('infile', 
                type=argparse.FileType('r',encoding='utf-8'),
                help='Input File path',
            )
    task_parser.add_argument('outfile', 
                type=argparse.FileType('w',encoding='utf-8'),
                help='Output File path',
            )
    task_parser.add_argument('lang', 
                help='Language',
            )
    task_parser.set_defaults(func=run_tokenize)


def add_normalize_parser(subparsers):
    task_parser=subparsers.add_parser('normalize', help='tokenizer help')

    task_parser.add_argument('infile', 
                type=argparse.FileType('r',encoding='utf-8'),
                help='Input File path',
            )
    task_parser.add_argument('outfile', 
                type=argparse.FileType('w',encoding='utf-8'),
                help='Output File path',
            )
    task_parser.add_argument('lang', 
                help='Language',
            )
    task_parser.set_defaults(func=run_normalize)


def get_parser():
    parser = argparse.ArgumentParser(prog='indicnlp')
    subparsers = parser.add_subparsers(help='sub-command help', dest='subcommand')
    add_tokenize_parser(subparsers)
    add_normalize_parser(subparsers)
    return parser

def main():
    parser=get_parser()
    args=parser.parse_args()
    print(args)

    args.func(args)

if __name__ == '__main__':
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

