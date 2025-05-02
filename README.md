# dask-sorting-sandbox
Where I will do scaling experiments with Dask by sorting tasks by size and 
observing impact of task stealing.

These are the experiment levels:

* with task stealing
  * with sorting descending
  * with sorting ascending
  * with no sorting
* without task stealing
  * with sorting descending
  * with sorting ascending
  * with no sorting

The implementation will randomly generate a sequence of sleep times where Dask
tasks will sleep for a given number of seconds.  These sequences will be sorted
by time and run with and without task stealing.

The results for each run will be in a CSV file with these columns:

* order: 'descending', 'ascending', 'none'
* seconds: [0,30]
* start time: unix epoch
* stop time: unix epoch

Will run this locally.

Salient package versions:

dask               2025.4.1
distributed        2025.4.1
numpy              2.2.5
