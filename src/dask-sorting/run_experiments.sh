#!/usr/bin/env bash
#
# Serially run all the experiments

# How many tasks to run
n=3000

# do 30 iterations for each experimental level
for i in {1..30}; do
  echo "Iteration $i"

  python dask-sorting.py --job $i --output=descending_stealing.csv $n
  python dask-sorting.py --job $i --sorting=ascending --output=ascending_stealing.csv $n
  python dask-sorting.py --job $i --sorting=none --output=none_stealing.csv $n

  python dask-sorting.py --job $i --no-stealing --output=descending_nostealing.csv $n
  python dask-sorting.py --job $i --no-stealing --sorting=ascending --output=ascending_nostealing.csv $n
  python dask-sorting.py --job $i --no-stealing --sorting=none --output=none_nostealing.csv $n

done

echo "Done!"
say "Your script has finished"