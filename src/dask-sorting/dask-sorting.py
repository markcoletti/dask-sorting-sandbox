#!/usr/bin/env python3
"""
    For implementing experiments for gauging sorting performance with and
    without task stealing.  Tasks are randomly sleeping for so many seconds.

    usage: dask-sorting.py [-h] [--sorting {descending,ascending,none}]
                           [--stealing] [--no-stealing] [--minimum MINIMUM]
                           [--maximum MAXIMUM] [--output OUTPUT] [--job JOB]
                           n

    This performs Dask timing experiments with sorting vs. task stealing.

    positional arguments:
      n                     Number of Dask tasks to randomly generate

    options:
      -h, --help            show this help message and exit
      --sorting {descending,ascending,none}
                            How do we want to sort Dask tasks
      --stealing            We want Dask task stealing
      --no-stealing         We do not want Dask task stealing
      --minimum MINIMUM     Minimum number of seconds to sort Dask tasks
      --maximum MAXIMUM     Maximum number of seconds to sort Dask tasks
      --output OUTPUT       Where to write the CSV output
      --job JOB             Optional job identifier to be incorporated into CSV
                            output
"""
from time import time, sleep
from datetime import datetime
import random
import argparse
from rich import print
from rich.progress import track
from distributed import Client, as_completed
from dask import config
import polars as pl


DESCRIPTION=\
"""
This performs Dask timing experiments with sorting vs. task stealing.
"""

DEFAULT_MINIMUM=5 # seconds minimum
DEFAULT_MAXIMUM=20 # seconds maximum


def do_sleep(n):
    start = time()
    sleep(n)
    end = time()
    return n, start, end



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument('--sorting', type=str,
                        default='descending',
                        choices=['descending', 'ascending', 'none'],
                        help='How do we want to sort Dask tasks')
    parser.add_argument('--stealing',
                        action='store_true',
                        help='We want Dask task stealing')
    parser.add_argument('--no-stealing',
                        dest='stealing',
                        action='store_false',
                        help='We do not want Dask task stealing')
    parser.add_argument('--minimum', type=int,
                        default=DEFAULT_MINIMUM,
                        help='Minimum number of seconds to sort Dask tasks')
    parser.add_argument('--maximum', type=int,
                        default=DEFAULT_MAXIMUM,
                        help='Maximum number of seconds to sort Dask tasks')
    parser.add_argument('--output', type=str,
                        help='Where to write the CSV output')
    parser.add_argument('--job', type=str,
                        help='Optional job identifier to be incorporated '
                             'into CSV output')
    parser.add_argument('n', type=int,
                        help='Number of Dask tasks to randomly generate')
    parser.set_defaults(stealing=True)  # Steal tasks by default

    args = parser.parse_args()

    out_file_name = args.output

    if out_file_name is None:
        # Generate a filename based on the current date and time to ensure
        # that it's unique.
        out_file_name = datetime.now().strftime("%Y%m%d_%H%M") + ".csv"

    print(args)

    # Generate the random sequence of seconds to sleep
    sequence = [random.randint(args.minimum, args.maximum) for _ in range(args.n)]

    if args.sorting == 'descending':
        sequence.sort(reverse=True)
    elif args.sorting == 'ascending':
        sequence.sort()

    if not args.stealing:
        # Disable task stealing
        print('Disabling Dask scheduler task stealing.')
        config.set({'distributed.scheduler.work-stealing': False})
    else:
        print('Using default of Dask scheduler task stealing.')

    with Client() as client:
        futures = client.map(do_sleep, sequence)

        future_itr = as_completed(futures)

        output = [] # We'll append records to this list

        # What the records will look like
        row = {'order' : args.sorting,
               'stealing' : args.stealing,
               'seconds' : 0,
               'start' : 0,
               'stop' : 0,}

        if args.job is not None:
            row['job'] = args.job

        for future in track(future_itr, total=args.n,
                            description='Processing tasks ... '):
            result = future.result()

            curr_row = row.copy()
            curr_row['seconds'] = result[0]
            curr_row['start'] = result[1]
            curr_row['stop'] = result[2]

            output.append(curr_row)

    output_df = pl.DataFrame(output)
    print(f'Writing to {out_file_name}')
    output_df.write_csv(out_file_name)





