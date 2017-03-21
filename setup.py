#!/usr/bin/env python3

from setuptools import setup
with open('README.md') as readme:
    setup(
        name = 'keystore',
        packages = ['keystore'],
        version = '0.1.5',
        description = 'Command line tools to compress and encrypt your private keys',
        author = 'Xavier Ho',
        author_email = 'contact@xavierho.com',
        url = 'https://github.com/Spaxe/keystore',
        download_url = 'https://github.com/Spaxe/keystore/archive/master.zip',
        keywords = ['keys', 'tokens', 'archive'],
        scripts=['keystore-load', 'keystore-save'],
        classifiers = [
            'Programming Language :: Python',
            'Programming Language :: Python :: 3',
            'Development Status :: 2 - Pre-Alpha',
            'Environment :: Console',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Operating System :: MacOS',
            'Operating System :: POSIX',
            'Operating System :: Unix',
            'Topic :: System :: Archiving :: Backup',
            'Topic :: System :: Archiving :: Compression',
            'Topic :: Security',
            'Topic :: Security :: Cryptography',
            ],
        long_description = readme.read()
    )