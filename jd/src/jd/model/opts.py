import argparse

_parser = argparse.ArgumentParser()

_parser.add_argument('--w2v-data-maxlen', type=int, default=250, help='maximum length of data which \
                                                                       tokenized with Word2Vec')

_parser.add_argument('--num-categories', type=int, default=4, help='number of jd\'s categories')
_parser.add_argument('--lstm-epochs', type=int, default=5, help='lstm train epoch')
_parser.add_argument('--lstm-batch-size', type=int, default=32, help='lstm train batch size')

opt = _parser.parse_args()
