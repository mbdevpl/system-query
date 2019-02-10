.. role:: bash(code)
    :language: bash

.. role:: python(code)
    :language: python


============
system_query
============

.. image:: https://img.shields.io/pypi/v/system-query.svg
    :target: https://pypi.org/project/system-query
    :alt: package version from PyPI

.. image:: https://travis-ci.org/mbdevpl/system-query.svg?branch=master
    :target: https://travis-ci.org/mbdevpl/system-query
    :alt: build status from Travis CI

.. image:: https://ci.appveyor.com/api/projects/status/github/mbdevpl/system-query?branch=master&svg=true
    :target: https://ci.appveyor.com/project/mbdevpl/system-query
    :alt: build status from AppVeyor

.. image:: https://api.codacy.com/project/badge/Grade/b44e2fc42fcd4301bcd0fb11938a89da
    :target: https://www.codacy.com/app/mbdevpl/system-query
    :alt: grade from Codacy

.. image:: https://codecov.io/gh/mbdevpl/system-query/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/mbdevpl/system-query
    :alt: test coverage from Codecov

.. image:: https://img.shields.io/github/license/mbdevpl/system-query.svg
    :target: https://github.com/mbdevpl/system-query/blob/master/NOTICE
    :alt: license

Comprehensive and concise system information tool.

The goal is to gather all relevant:

*   hardware information (processors, accelerators, memory, networks, drives)
*   static operating system information (name, version, hostname)
*   runtime information (environment, libraries, system load, etc.)

and provide them in a concise form that's both machine- and human-readable.

Another important goal is to also be fail-safe, even with unexpected hardware configurations,
low-level tool errors and deal with incomplete information.

You can use *system-query* as a library and as a command-line tool.

.. contents::
    :backlinks: none


Motiviation
===========

Where am I running?
-------------------

One of the main motivations for creating *system-query* is to assist with answering the question
"what is the actual hardware and software configuration of the system I'm using?"
regardless of the official specification.


How to rerun this experiment?
-----------------------------

The *system-query* was also created to assist with the computational experiment reproducibility
and verification of results. Only if you know exactly where you ran your experiment,
you can reason about its results and be able to reproduce them.


Using
=====

Installing *system-query* doesn't enable all the features by default. Some of the query functions
will work only on **some** systems. To attempt installation with all features enables,
run :bash:`pip3 install system-query[all]`. If something brakes, you can narrow down the features
by typing a feature scope instead of :bash:`all`.
You can choose from :bash:`cpu`, :bash:`gpu`, :bash:`hdd`, :bash:`ram` and :bash:`swap`.
E.g. :bash:`pip3 install system-query[gpu]`.


As library
----------

.. code:: python

    In [1]: from system_query import query_cpu
            query_cpu()

    Out[1]: {'brand': 'Intel(R) Core(TM) i7-3770K CPU @ 3.50GHz',
             'clock': 1771.0370000000003,
             'clock_max': 3900.0,
             'clock_min': 1600.0,
             'logical_cores': 8,
             'physical_cores': 4}

More examples in `<examples.ipynb>`_.


system_query.query_all()
~~~~~~~~~~~~~~~~~~~~~~~~

This will launch all below functions and assemble results into a dictionary.


system_query.query_cpu()
~~~~~~~~~~~~~~~~~~~~~~~~

To be able to see details like clock speed and core counts, install Python package :bash:`psutil`.


system_query.query_gpu()
~~~~~~~~~~~~~~~~~~~~~~~~

To be able to see GPUs in the system, make sure you have CUDA installed
and install Python package :bash:`pycuda`.


system_query.query_hdd()
~~~~~~~~~~~~~~~~~~~~~~~~

To be able to see HDDs in the system, make sure you have libudev installed
and install Python package :bash:`pyudev`.


system_query.query_ram()
~~~~~~~~~~~~~~~~~~~~~~~~

To be able to see amount of memory, install Python package :bash:`psutil`.


system_query.query_swap()
~~~~~~~~~~~~~~~~~~~~~~~~~

To be able to see amount of swap space, install Python package :bash:`psutil`.


As command-line tool
--------------------

For example:

.. code:: bash

    $ python3 -m system_query
    {'cpu': {'brand': 'Intel(R) Core(TM) i7-3770K CPU @ 3.50GHz',
             'clock': 1725.031125,
             'clock_max': 3900.0,
             'clock_min': 1600.0,
             'logical_cores': 8,
             'physical_cores': 4},
     'gpus': [],
     'host': 'TestMachine',
     'os': 'Linux-4.4.0-109-generic-x86_64-with-debian-stretch-sid',
     'ram': {'total': 33701269504},
     'swap': 0}

Usage information:

.. code::

    $ python3 -m system_query -h
    usage: system_query [-h] [-s {all,cpu,gpu,ram}] [-f {raw,json}] [-t TARGET]
                        [--version]

    Comprehensive and concise system information tool. Query a given hardware
    and/or softawre scope of your system and get results in human- and machine-
    readable formats.

    optional arguments:
      -h, --help            show this help message and exit
      -s {all,cpu,gpu,ram}, --scope {all,cpu,gpu,ram}
                            Scope of the query (default: all)
      -f {raw,json}, --format {raw,json}
                            Format of the results of the query. (default: raw)
      -t TARGET, --target TARGET
                            File path where to write the results of the query.
                            Special values: "stdout" and "stderr" to write to
                            stdout and stderr, respectively. (default: stdout)
      --version             show program's version number and exit

    Copyright 2017-2018 by the contributors, Apache License 2.0,
    https://github.com/mbdevpl/system-query


Requirements
============

Python version 3.5 or later.

Python libraries as specified in `<requirements.txt>`_.
Recommended (but optional) packages are listed in `<optional_requirements.txt>`_.

Building and running tests additionally requires packages listed in `<test_requirements.txt>`_.

Tested on Linux, OS X and Windows.

Additionally, for all features to work you should have the following libraries
installed in your system:

*   CUDA
*   libudev


Contributors
============

Aleksandr Drozd

Mateusz Bysiek

For licensing information, please see `<LICENSE>`_ and `<NOTICE>`_.
