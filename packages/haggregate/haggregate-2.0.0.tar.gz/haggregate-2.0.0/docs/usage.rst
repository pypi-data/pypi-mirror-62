.. _usage:

=====
Usage
=====

Synopsis
========

``haggregate [--traceback] config_file``

Description and quick start
===========================

``haggregate`` gets the data of time series from files and creates time
series of a larger time step, storing the result in files.  The
details of its operation are specified in the configuration file
specified on the command line.

Installation
------------

``pip install haggregate``

How to run it
-------------

First, you need to create a configuration file with a text editor such
as ``vim``, ``emacs``, ``notepad``, or whatever. Create such a file
and name it, for example, :file:`/var/tmp/haggregate.conf`, with
the following contents (the contents don't matter at this stage, just
copy and paste them from below)::

    [General]
    loglevel = INFO

Then, open a command prompt and give it this command::

    haggregate /var/tmp/haggregate.conf

If you have done everything correctly, it should output an error message
complaining that something in its configuration file isn't right.

Configuration file example
--------------------------

Take a look at the following example configuration file and read the
explanatory comments that follow it:

.. code-block:: ini

    [General]
    loglevel = INFO
    logfile = /var/log/haggregate/haggregate.log
    base_dir = /var/cache/timeseries/
    target_step = 1H
    min_count = 2
    missing_flag = DATEINSERT

    [temperature]
    source_file = temperature-10min.hts
    target_file = temperature-hourly.hts
    method = mean

    [rainfall]
    source_file = rainfall-10min.hts
    target_file = rainfall-hourly.hts
    method = sum

With the above configuration file, ``haggregate`` will log information
in the file specified by :option:`logfile`. It will aggregate the
specified time series into hourly (``1H``). The filenames specified with
:option:`source_file` and :option:`target_file` are relative to
:option:`base_dir`. For the temperature, source records will be
averaged, whereas for rainfall they will be summed.

Configuration file reference
============================

The configuration file has the format of INI files. There is a
``[General]`` section with general parameters, and any number of other
sections, which we will call "time series sections", each time series
section referring to one time series.

General parameters
------------------

.. option:: loglevel

   Optional. Can have the values ``ERROR``, ``WARNING``, ``INFO``,
   ``DEBUG``.  The default is ``WARNING``.

.. option:: logfile

   Optional. The full pathname of a log file. If unspecified, log
   messages will go to the standard error.

.. option:: base_dir

   Optional. ``haggregate`` will change directory to this directory, so
   any relative filenames will be relative to this directory. If
   unspecified, relative filenames will be relative to the directory
   from which ``haggregate`` was started.

.. option:: target_step

   A string specifying the target time step, as a pandas "frequency".
   Examples of steps are "1D" for day, "1H" for hour, "1T" or "1min" for
   minute. You can also use larger multipliers, like "30T" for 30 minutes.
   The program hasn't been tested for monthly or larger time steps.

.. option:: target_timestamp_offset

   Optional. A string specifying the resulting timestamp offset, as a
   pandas "frequency". For example, for ``target_timestamp_offset=1D``,
   if we set ``target_timestamp_offset=1min``, the resulting time stamps
   will be ending in 23:59. This does not modify the calculations; it
   only offsets the timestamp. For example, if without
   ``target_timestamp_offset`` one of the resulting timeseries records
   is ``2019-12-05 00:00, 3.14``, then with
   ``target_timestamp_offset=-10min`` the same processing will result in
   ``2019-12-05 00:10, 3.14``.

.. option:: min_count
            missing_flag

   If some of the source records corresponding to a destination record
   are missing, :option:`min_count` specifies what will be done. If
   there are fewer than :option:`min_count` source records corresponding
   to a destination record, the resulting destination record is null;
   otherwise, the destination record is derived even though some records
   are missing. In that case, the flag specified by
   :option:`missing_flag` is raised in the destination record.

Time series sections
--------------------

The name of the section is ignored.

.. option:: source_file

   The filename of the source file with the time series, in `file
   format`_; it must be absolute or relative to :option:`base_dir`.

.. option:: target_file

   The filename of the target file, which will be written in `file
   format`_; it must be absolute or relative to :option:`base_dir`. In
   this version of ``haggregate``, all the aggregation is repeated even
   if it or part of it has been done in the past, and the file is
   entirely overwritten if it already exists.

.. option:: method

   How the aggregation will be performed; one of "mean", "sum",
   "max" and "min".

.. _file format: https://github.com/openmeteo/htimeseries/#file-format

How the aggregation is performed
================================

The aggregation is performed in two steps:

1. Regularization
-----------------

The source time series must not be entirely irregular; it must have a
time step, but this time step may have disturbances.  For example, it
may be a ten-minute time series like this::

   2008-02-07 10:10 10.54 
   2008-02-07 10:20 10.71 
   2008-02-07 10:41 10.93 
   2008-02-07 10:50 11.10 
   2008-02-07 11:00 11.23 

The above has a missing record (10:30) and a disturbance in the time
stamp of another record (10:41). The first step of the process,
regularization, would convert it to this::

   2008-02-07 10:10 10.54 
   2008-02-07 10:20 10.71 
   2008-02-07 10:30 empty
   2008-02-07 10:40 10.93
   2008-02-07 10:50 11.10 
   2008-02-07 11:00 11.23 

That is, the result of regularization is a time series with a regular
time step from beginning to end, with no missing records.

A **regular timestamp** is one that falls exactly on the round time
step; e.g. for a ten-minute step, regular timestamps are 10:10,
10:20, etc., whereas irregular timestamps are 10:11, 10:25, etc. For
hourly time step, regular timestamps end in :00.

The regularization does not perform any interpolation or otherwise
modify the time series values; it only modifies the time stamps, leaving
the values as is.

Specifically, the resulting regularized time series begins with the
regular timestamp A which is nearest to the timestamp of the first
record of the source time series, and ends at the timestamp B which is
nearest to the last record of the source time series. Between A and B,
the resulting time series contains records for all regular timestamps,
although some may be empty.  The value and flags for each resulting
record with (regular) timestamp *t* are determined as follows:

* If a record exists in the source time series and has timestamp *t*,
  that record's value and flags are used.
* Otherwise, if a single nonempty record exists in the source time
  series such that its timestamp is between ``t - time_step/2``
  (inclusive) and ``t + time_step/2`` (non-inclusive), then the value
  and flags of this record are used (plus ``DATEINSERT``, explained
  below).
* Otherwise, the value is empty and no flags are set.

Whenever the algorithm results in creating a nonempty record whose
timestamp does not have an exact match in the source time series, the
``DATEINSERT`` flag is set in the destination record.

2. Aggregation
--------------

After regularization is complete, aggregation is trivial. The timestamp
in an aggregated record is the end of the interval.

For example, if you aggregate a ten-minute time series to hourly, the
record with timestamp ``11:00`` is the average or sum or max or min of
time stamps ``10:10``, ``10:20``, ..., ``10:50``, ``11:00``.

Likewise, if you aggregate an hourly time series to daily, the record
with timestamp ``2020-01-25 00:00`` is the average or sum or max or min
of time stamps ``2020-01-24 00:10``, ..., ``2020-01-25 00:00``.

Thus, the daily time series with timestamp ``2020-01-25 00:00`` is
actually aggregated from 2020-01-24 (the previous day). This can be
confusing, so it may be a good idea to use ``2020-01-24 23:59`` as the
resulting timestamp instead. This can be achieved by setting
``target_timestamp_offset`` to ``1min``.
