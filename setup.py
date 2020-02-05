"""Setup script for system_query package."""

import setup_boilerplate


class Package(setup_boilerplate.Package):
    """Package metadata."""

    name = 'system-query'
    description = 'comprehensive and concise system information querying tool'
    url = 'https://github.com/mbdevpl/system-query'
    author = 'Aleksandr Drozd, Mateusz Bysiek'
    maintainer = 'Mateusz Bysiek'
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Education',
        'Topic :: Scientific/Engineering',
        'Topic :: Utilities'
        ]
    keywords = ['system', 'software', 'hardware']
    extras_require = {
        'all': ['pint ~= 0.10.1', 'psutil ~= 5.6', 'py-cpuinfo == 5.*', 'pycuda >= 2019.1',
                'pyudev ~= 0.22.0'],
        'cpu': ['pint ~= 0.10.1', 'psutil ~= 5.6', 'py-cpuinfo == 5.*'],
        'gpu': ['pycuda >= 2019.1'],
        'hdd': ['pyudev ~= 0.22.0'],
        'ram': ['psutil ~= 5.6'],
        'swap': ['psutil ~= 5.6']}


if __name__ == '__main__':
    Package.setup()
