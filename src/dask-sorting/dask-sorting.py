#!/usr/bin/env python3
"""
    For implementing experiments for gauging sorting performance with and
    without task stealing.  Tasks are randomly sleeping for so many seconds.

    usage: dask-sorting.py [-h] [--sorting {descending,ascending,none}]
                       [--stealing STEALING] [--minimum MINIMUM]
                       [--maximum MAXIMUM] [--output OUTPUT]
                       n

    This performs Dask timing experiments with sorting vs. task stealing.

    positional arguments:
      n                     Number of Dask tasks to randomly generate

    options:
      -h, --help            show this help message and exit
      --sorting {descending,ascending,none}
                            How do we want to sort Dask tasks
      --stealing STEALING   Do we want Dask stealing or not?
      --minimum MINIMUM     Minimum number of seconds to sort Dask tasks
      --maximum MAXIMUM     Maximum number of seconds to sort Dask tasks
      --output OUTPUT       Where to write the CSV output
"""
from time import time
from datetime import datetime
import random
import argparse
from rich import print


DESCRIPTION=\
"""
This performs Dask timing experiments with sorting vs. task stealing.
"""

DEFAULT_MINIMUM=5 # seconds minimum
DEFAULT_MAXIMUM=20 # seconds maximum


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument('--sorting', type=str,
                        default='descending',
                        choices=['descending', 'ascending', 'none'],
                        help='How do we want to sort Dask tasks')
    parser.add_argument('--stealing', type=bool,
                        default=True,
                        help='Do we want Dask stealing or not?')
    parser.add_argument('--minimum', type=int,
                        default=DEFAULT_MINIMUM,
                        help='Minimum number of seconds to sort Dask tasks')
    parser.add_argument('--maximum', type=int,
                        default=DEFAULT_MAXIMUM,
                        help='Maximum number of seconds to sort Dask tasks')
    parser.add_argument('--output', type=str,
                        help='Where to write the CSV output')
    parser.add_argument('n', type=int,
                        help='Number of Dask tasks to randomly generate')

    args = parser.parse_args()

    out_file_name = args.output

    if out_file_name is None:
        # Generate a filename based on the current date and time to ensure
        # that it's unique.
        out_file_name = datetime.now().strftime("%Y%m%d_%H%M") + ".csv"

    print(args)



