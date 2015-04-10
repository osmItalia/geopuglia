import sys
sys.path.append('../core/')

import argparse
from sit_puglia_utils import *


def get_args():
    parser = argparse.ArgumentParser(description="Download SIT Puglia CTR")
    parser.add_argument('--fogli', type=str, nargs='+', choices=set(FOGLI_ALL.keys()), default=set(FOGLI_ALL.keys()))
    parser.add_argument('--tavolette', type=int, nargs='+', choices=TAVOLETTE_ALL, default=TAVOLETTE_ALL)
    parser.add_argument('--quadranti', type=int, nargs='+', choices=QUADRANTI_ALL, default=QUADRANTI_ALL)
    parser.add_argument('--download', type=str, nargs='+', choices=set(URLS.keys()), default=set(URLS.keys()))

    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()
    orchestrator(args.download, args.fogli, args.tavolette, args.quadranti)

