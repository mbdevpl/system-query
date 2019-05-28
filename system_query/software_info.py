

import logging
import shutil
import subprocess

_LOG = logging.getLogger(__name__)

DEFAULT_VERSION_QUERY_FLAG = '--version'

VERSION_QUERY_FLAGS = {
    # compilers
    'gcc': None,
    'g++': None,
    'gfortran': None,
    'clang': None,
    'clang++': None,
    'flang': None,
    'pgcc': None,
    'pgc++': None,
    'pgfortran': None,
    'icc': None,
    'icpc': None,
    'ifort': None,
    'mpicc': None,
    'mpic++': None,
    'mpifort': None,
    # python
    'python': None,
    'python2': None,
    'python3': None,
    'python3.6': None,
    'python3.7': None,
    'pip': None,
    'pip2': None,
    'pip3': None,
    'pip3.6': None,
    'pip3.7': None,
    # other
    'java': '-version',
    'ruby': None,
    'nvcc': None,
    'mpirun': None,
    'spack': None}

PYTHON_PACKAGES = [
    'chainer', 'Cython', 'h5py', 'ipython', 'mpi4py', 'Nuitka', 'numba', 'numpy',
    'pandas', 'pycuda', 'pyopencl', 'scikit-learn', 'scipy', 'tensorflow']


def _run_version_query(cmd, **kwargs) -> str:
    try:
        result = subprocess.run(
            cmd, timeout=5, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, **kwargs)
    except subprocess.TimeoutExpired:
        return None
    except subprocess.CalledProcessError:
        return None
    except FileNotFoundError:  # on Windows
        return None
    version_raw = result.stdout.decode()
    if not version_raw:
        version_raw = result.stderr.decode()
    try:
        version = version_raw.splitlines()[0]
    except IndexError:
        version = version_raw
    return version


def query_software():
    software_info = {}
    for program, flag in VERSION_QUERY_FLAGS.items():
        path = shutil.which(program)
        if path is None:
            continue
        if flag is None:
            flag = DEFAULT_VERSION_QUERY_FLAG
        cmd = [program, flag]
        _LOG.debug('running "%s"', cmd)
        version = _run_version_query(cmd)
        software_info[program] = {'path': path, 'version': version}

    # python packages
    for py_ver in ('python', 'python2', 'python3', 'python3.6', 'python3.7'):
        if py_ver not in software_info:
            continue
        py_packages = {}
        for package in PYTHON_PACKAGES:
            version = _run_version_query(
                '{} -m pip freeze | grep "{}"'.format(py_ver, package), shell=True)
            if version is None:
                continue
            py_packages[package] = {'version': version}
        software_info[py_ver]['packages'] = py_packages
    return software_info
