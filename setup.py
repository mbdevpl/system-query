"""Setup script for system_query package."""

import boilerplates.setup


class Package(boilerplates.setup.Package):
    """Package metadata."""

    name = 'system-query'
    description = 'Comprehensive and concise system information querying tool.'
    url = 'https://github.com/mbdevpl/system-query'
    author = 'Aleksandr Drozd, Emil Vatai, Mateusz Bysiek'
    maintainer = 'Mateusz Bysiek'
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: System :: Hardware',
        'Topic :: System :: Monitoring',
        'Topic :: System :: Operating System',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities',
        'Typing :: Typed']
    keywords = ['system', 'software', 'hardware']
    extras_require = {
        'all': boilerplates.setup.parse_requirements('requirements_all.txt'),
        'cpu': boilerplates.setup.parse_requirements('requirements_cpu.txt'),
        'gpu': boilerplates.setup.parse_requirements('requirements_gpu.txt'),
        'hdd': boilerplates.setup.parse_requirements('requirements_hdd.txt'),
        'ram': boilerplates.setup.parse_requirements('requirements_memory.txt'),
        'swap': boilerplates.setup.parse_requirements('requirements_memory.txt')}


if __name__ == '__main__':
    Package.setup()
