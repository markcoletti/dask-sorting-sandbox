#!/usr/bin/env bash
#
# Serially run all the experiments

# How many tasks to run
n=1000

python ./dask-sorting --output=descending_stealing.csv $n
python ./dask-sorting --sorting=ascending --output=ascending_stealing.csv $n
python ./dask-sorting --sorting=non --output=none_stealing.csv $n

python ./dask-sorting --stealing=False --output=descending_nostealing.csv $n
python ./dask-sorting --stealing=False  --sorting=ascending --output=ascending_nostealing.csv $n
python ./dask-sorting --stealing=False  --sorting=non --output=none_nostealing.csv $n


say "Your script has finished"