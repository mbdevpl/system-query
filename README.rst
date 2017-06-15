.. role:: bash(code)
   :language: bash

.. role:: python(code)
   :language: python

============
system_query
============

.. image:: https://travis-ci.org/mbdevpl/system-query.svg?branch=master
    :target: https://travis-ci.org/mbdevpl/system-query
    :alt: build status from Travis CI

.. image:: https://ci.appveyor.com/api/projects/status/github/mbdevpl/system-query?branch=master&svg=true
    :target: https://ci.appveyor.com/project/mbdevpl/system-query
    :alt: build status from AppVeyor

.. image:: https://coveralls.io/repos/github/mbdevpl/system-query/badge.svg?branch=master
    :target: https://coveralls.io/github/mbdevpl/system-query
    :alt: test coverage from Coveralls

.. image:: https://img.shields.io/github/license/mbdevpl/system-query.svg
    :target: https://github.com/mbdevpl/system-query
    :alt: license

Comprehensive and concise system information tool.

It is also attempting to be fail-safe.

Usable as library and as a commandline tool.


as library
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


as commandline tool
-------------------

For example:

.. code:: bash

    $ python3 -m system_query
    {'cpu': {'brand': 'Intel(R) Core(TM) i7-3770K CPU @ 3.50GHz',
             'clock': 1736.1565,
             'clock_max': 3900.0,
             'clock_min': 1600.0,
             'logical_cores': 8,
             'physical_cores': 4},
     'gpus': [{'brand': 'GeForce GTX 580',
               'clock': 1544000,
               'cores': 512,
               'compute_capability': 2.0,
               'memory': 1543766016,
               'memory_clock': 2004000,
               'multiprocessors': 16,
               'warp_size': 32}],
     'host': 'mbLab',
     'os': 'Linux-4.4.0-78-generic-x86_64-with-debian-stretch-sid',
     'ram': {'banks': [], 'total': 33701339136},
     'swap': 0}

Usage information:

.. code:: bash

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

    Copyright 2017 by the system-query package contributors, Apache License 2.0,
    https://github.com/mbdevpl/system-query


requirements
------------

As defined in `<requirements.txt>`_. Reccomended (but optional) packages are listed in
`<optional_requirements.txt>`_.

Additionally, building and testing requires packages listed in `<dev_requirements.txt>`_.


contributors
------------

Aleksandr Drozd

Mateusz Bysiek

For licensing information, please see `<LICENSE>`_ and `<NOTICE>`_.
