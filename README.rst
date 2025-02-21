.. role:: bash(code)
    :language: bash

.. role:: python(code)
    :language: python


============
system_query
============

Comprehensive and concise system information querying tool.

.. image:: https://img.shields.io/pypi/v/system-query.svg
    :target: https://pypi.org/project/system-query
    :alt: package version from PyPI

.. image:: https://github.com/mbdevpl/system-query/actions/workflows/python.yml/badge.svg?branch=main
    :target: https://github.com/mbdevpl/system-query/actions
    :alt: build status from GitHub

.. image:: https://codecov.io/gh/mbdevpl/system-query/branch/main/graph/badge.svg
    :target: https://codecov.io/gh/mbdevpl/system-query
    :alt: test coverage from Codecov

.. image:: https://api.codacy.com/project/badge/Grade/b44e2fc42fcd4301bcd0fb11938a89da
    :target: https://app.codacy.com/gh/mbdevpl/system-query
    :alt: grade from Codacy

.. image:: https://img.shields.io/github/license/mbdevpl/system-query.svg
    :target: NOTICE
    :alt: license

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


Motivation
==========

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
by typing a feature scope instead of ``all``.
You can choose from ``cpu``, ``gpu``, ``hdd``, ``ram`` and ``swap``.
E.g. :bash:`pip3 install system-query[gpu]`. You can also select more than one feature
at the same time, e.g. :bash:`pip3 install system-query[cpu,hdd,ram]`.


As library
----------

.. code:: python

    In [1]: import system_query

Usage examples are below and in `<examples.ipynb>`_.

system_query.query_all()
~~~~~~~~~~~~~~~~~~~~~~~~

This will get basic host and OS information and launch most of below functions,
and then assemble the results into a single dictionary.

.. code:: python

    In [2]: system_query.query_all()
    Out[2]:
    {'host': 'hostname',
     'os': 'Linux-6.8.0-47-generic-x86_64-with-glibc2.35',
     'cpu': {'brand': 'Intel(R) Core(TM) i7-9750H CPU @ 2.60GHz',
      'logical_cores': 12,
      'physical_cores': 6,
      'clock': 4131.882833333333,
      'clock_min': 800.0,
      'clock_max': 4500.0,
      'cache': {1: 196608, 2: 1572864, 3: 12582912}},
     'gpus': [{'brand': 'NVIDIA GeForce RTX 2060',
       'memory': 6214516736,
       'memory_clock': 7001000,
       'compute_capability': 7.5,
       'clock': 1200000,
       'multiprocessors': 30,
       'cores': None,
       'warp_size': 32}],
     'ram': {'total': 16631603200},
     'hdds': {'/dev/sdb': {'size': 0, 'model': '1081C'},
      '/dev/sdc': {'size': 0, 'model': '1081C'},
      '/dev/sda': {'size': 1953525168, 'model': 'WDC WD10SPZX-24Z'},
      '/dev/nvme0n1': {'size': 2000409264, 'model': 'SAMSUNG MZVLB1T0HBLR-000L2'}},
     'swap': {'total': 17179865088}}

system_query.query_cpu()
~~~~~~~~~~~~~~~~~~~~~~~~

To be able to see details like cache size, clock speed and core counts,
install Python packages ``pint`` and ``psutil``.

.. code:: python

    In [3]: system_query.query_cpu()
    Out[3]:
    {'brand': 'Intel(R) Core(TM) i7-9750H CPU @ 2.60GHz',
     'logical_cores': 12,
     'physical_cores': 6,
     'clock': 4182.955000000001,
     'clock_min': 800.0,
     'clock_max': 4500.0,
     'cache': {1: 196608, 2: 1572864, 3: 12582912}}

system_query.query_gpus()
~~~~~~~~~~~~~~~~~~~~~~~~~

To be able to see GPUs in the system, make sure you have CUDA installed
and install Python package ``pycuda``.

.. code:: python

    In [4]: system_query.query_gpus()
    Out[4]:
    [{'brand': 'NVIDIA GeForce RTX 2060',
      'memory': 6214516736,
      'memory_clock': 7001000,
      'compute_capability': 7.5,
      'clock': 1200000,
      'multiprocessors': 30,
      'cores': None,
      'warp_size': 32}]

system_query.query_hdds()
~~~~~~~~~~~~~~~~~~~~~~~~~

To be able to see HDDs in the system, make sure you have libudev installed
and install Python package ``pyudev``.

.. code:: python

    In [5]: system_query.query_hdds()
    Out[5]:
    {'/dev/sdb': {'size': 0, 'model': '1081C'},
     '/dev/sdc': {'size': 0, 'model': '1081C'},
     '/dev/sda': {'size': 1953525168, 'model': 'WDC WD10SPZX-24Z'},
     '/dev/nvme0n1': {'size': 2000409264, 'model': 'SAMSUNG MZVLB1T0HBLR-000L2'}}

system_query.query_ram()
~~~~~~~~~~~~~~~~~~~~~~~~

To be able to see amount of memory, install Python package ``psutil``.

.. code:: python

    In [6]: system_query.query_ram()
    Out[6]: {'total': 16631603200}

When given an optional argument ``sudo``, more information will be shown.

.. code:: python

    In [7]: system_query.query_ram(sudo=True)
    [sudo] password for user: ...
    Out[7]:
    {'total': 16632750080,
     'banks': [{'memory': 8589934592, 'clock': 2667000000},
      {'memory': 8589934592, 'clock': 2667000000}]}

system_query.query_software()
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This will attempt to gather version information of various common programs,
assuming their executables are in system path.

.. code:: python

    In [8]: system_query.query_software()
    Out[8]:
    {'gcc': {'path': '/usr/bin/gcc',
      'version': 'gcc (Ubuntu 11.4.0-1ubuntu1~22.04) 11.4.0'},
     'g++': {'path': '/usr/bin/g++',
      'version': 'g++ (Ubuntu 11.4.0-1ubuntu1~22.04) 11.4.0'},
     'gfortran': {'path': '/usr/bin/gfortran',
      'version': 'GNU Fortran (Ubuntu 11.4.0-1ubuntu1~22.04) 11.4.0'},
     'clang': {'path': '/usr/bin/clang',
      'version': 'Ubuntu clang version 14.0.0-1ubuntu1.1'},
     'clang++': {'path': '/usr/bin/clang++',
      'version': 'Ubuntu clang version 14.0.0-1ubuntu1.1'},
     'python': {'path': '/home/user/Software/Spack/opt/spack/linux-ubuntu22.04-skylake/gcc-12.3.0/python-3.11.6-pkgqipsrm2re32eisko6o7xa2xnwwzyh/bin/python',
      'version': 'Python 3.11.6',
      'packages': {'ipython': {'version': 'ipython==8.26.0'},
       'numpy': {'version': 'numpy @ file:///tmp/user/spack-stage/spack-stage-py-numpy-1.26.2-bpjavwbbxmsgiutvjzijlkjf5si5ki2v/spack-src'},
       'pandas': {'version': 'pandas==1.5.3'},
       'pycuda': {'version': 'pycuda==2024.1'},
       'scipy': {'version': 'scipy==1.13.0'}}},
     'python3': {'path': '/home/user/Software/Spack/opt/spack/linux-ubuntu22.04-skylake/gcc-12.3.0/python-3.11.6-pkgqipsrm2re32eisko6o7xa2xnwwzyh/bin/python3',
      'version': 'Python 3.11.6',
      'packages': {'ipython': {'version': 'ipython==8.26.0'},
       'numpy': {'version': 'numpy @ file:///tmp/user/spack-stage/spack-stage-py-numpy-1.26.2-bpjavwbbxmsgiutvjzijlkjf5si5ki2v/spack-src'},
       'pandas': {'version': 'pandas==1.5.3'},
       'pycuda': {'version': 'pycuda==2024.1'},
       'scipy': {'version': 'scipy==1.13.0'}}},
     'python3.10': {'path': '/usr/bin/python3.10',
      'version': 'Python 3.10.12',
      'packages': {}},
     'python3.11': {'path': '/home/user/Software/Spack/opt/spack/linux-ubuntu22.04-skylake/gcc-12.3.0/python-3.11.6-pkgqipsrm2re32eisko6o7xa2xnwwzyh/bin/python3.11',
      'version': 'Python 3.11.6',
      'packages': {'ipython': {'version': 'ipython==8.26.0'},
       'numpy': {'version': 'numpy @ file:///tmp/user/spack-stage/spack-stage-py-numpy-1.26.2-bpjavwbbxmsgiutvjzijlkjf5si5ki2v/spack-src'},
       'pandas': {'version': 'pandas==1.5.3'},
       'pycuda': {'version': 'pycuda==2024.1'},
       'scipy': {'version': 'scipy==1.13.0'}}},
     'pip': {'path': '/home/user/Software/Spack/opt/spack/linux-ubuntu22.04-skylake/gcc-12.3.0/python-3.11.6-pkgqipsrm2re32eisko6o7xa2xnwwzyh/bin/pip',
      'version': 'pip 24.2 from /home/user/Software/Spack/opt/spack/linux-ubuntu22.04-skylake/gcc-12.3.0/python-3.11.6-pkgqipsrm2re32eisko6o7xa2xnwwzyh/lib/python3.11/site-packages/pip (python 3.11)'},
     'pip3': {'path': '/home/user/Software/Spack/opt/spack/linux-ubuntu22.04-skylake/gcc-12.3.0/python-3.11.6-pkgqipsrm2re32eisko6o7xa2xnwwzyh/bin/pip3',
      'version': 'pip 24.2 from /home/user/Software/Spack/opt/spack/linux-ubuntu22.04-skylake/gcc-12.3.0/python-3.11.6-pkgqipsrm2re32eisko6o7xa2xnwwzyh/lib/python3.11/site-packages/pip (python 3.11)'},
     'pip3.11': {'path': '/home/user/Software/Spack/opt/spack/linux-ubuntu22.04-skylake/gcc-12.3.0/python-3.11.6-pkgqipsrm2re32eisko6o7xa2xnwwzyh/bin/pip3.11',
      'version': 'pip 24.2 from /home/user/Software/Spack/opt/spack/linux-ubuntu22.04-skylake/gcc-12.3.0/python-3.11.6-pkgqipsrm2re32eisko6o7xa2xnwwzyh/lib/python3.11/site-packages/pip (python 3.11)'},
     'java': {'path': '/usr/lib/jvm/java-11-openjdk-amd64/bin/java',
      'version': 'openjdk version "11.0.24" 2024-07-16'},
     'ruby': {'path': '/usr/bin/ruby',
      'version': 'ruby 3.0.2p107 (2021-07-07 revision 0db68f0233) [x86_64-linux-gnu]'},
     'nvcc': {'path': '/usr/bin/nvcc',
      'version': 'nvcc: NVIDIA (R) Cuda compiler driver'},
     'spack': {'path': '/home/user/Software/Scripts/spack', 'version': None}}

system_query.query_swap()
~~~~~~~~~~~~~~~~~~~~~~~~~

To be able to see amount of swap space, install Python package ``psutil``.

.. code:: python

    In [9]: system_query.query_swap()
    Out[9]: {'total': 17179865088}

system_query.query_and_export()
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This function is for convenience of running the query and outputting the results
in a designated format, to a designated location.

.. code:: python

    In [10]: import pathlib
    In [11]: system_query.query_and_export('all', 'json', pathlib.Path('/tmp/system_info.json'))

As command-line tool
--------------------

Below will run :python:`system_query.query_all()` and output results to stdout:

.. code::

    $ python3 -m system_query
    {'cpu': {'brand': 'Intel(R) Core(TM) i7-9750H CPU @ 2.60GHz',
             'cache': {1: 196608, 2: 1572864, 3: 12582912},
             'clock': 3685.686166666667,
             'clock_max': 4500.0,
             'clock_min': 800.0,
             'logical_cores': 12,
             'physical_cores': 6},
     'gpus': [{'brand': 'NVIDIA GeForce RTX 2060',
               'clock': 1200000,
               'compute_capability': 7.5,
               'cores': None,
               'memory': 6214516736,
               'memory_clock': 7001000,
               'multiprocessors': 30,
               'warp_size': 32}],
     'hdds': {'/dev/nvme0n1': {'model': 'SAMSUNG MZVLB1T0HBLR-000L2',
                               'size': 2000409264},
              '/dev/sda': {'model': 'WDC WD10SPZX-24Z', 'size': 1953525168},
              '/dev/sdb': {'model': '1081C', 'size': 0},
              '/dev/sdc': {'model': '1081C', 'size': 0}},
     'host': 'mbLegion',
     'os': 'Linux-6.8.0-47-generic-x86_64-with-glibc2.35',
     'ram': {'total': 16631603200},
     'swap': {'total': 17179865088}}

Please use ``-h`` to see usage information:

.. code::

    $ python3 -m system_query -h
    usage: system_query [-h] [-s {all,cpu,gpu,ram,swap}] [-f {raw,json}]
                        [-t TARGET] [--version]

    Comprehensive and concise system information tool. Query a given hardware
    and/or software scope of your system and get results in human- and machine-
    readable formats.

    options:
      -h, --help            show this help message and exit
      -s {all,cpu,gpu,ram,swap}, --scope {all,cpu,gpu,ram,swap}
                            Scope of the query (default: all)
      -f {raw,json}, --format {raw,json}
                            Format of the results of the query. (default: raw)
      -t TARGET, --target TARGET
                            File path where to write the results of the query.
                            Special values: "stdout" and "stderr" to write to
                            stdout and stderr, respectively. (default: stdout)
      --version             show program's version number and exit

    Copyright 2017-2025 by the contributors, Apache License 2.0,
    https://github.com/mbdevpl/system-query

Requirements
============

Python version 3.9 or later.

Python libraries as specified in `<requirements.txt>`_.
Recommended (but optional) packages are listed in `<requirements_optional.txt>`_.

Building and running tests additionally requires packages listed in `<requirements_test.txt>`_.

Tested on Linux, macOS and Windows.

Additionally, for all features to work you should have the following libraries
installed in your system:

*   CUDA
*   libudev


Contributors
============

Aleksandr Drozd

Emil Vatai

Mateusz Bysiek

For licensing information, please see `<LICENSE>`_ and `<NOTICE>`_.
