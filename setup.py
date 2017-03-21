#!/usr/bin/env python3

from setuptools import setup
setup(
    name = 'keystore',
    packages = ['keystore'],
    version = '0.1.0',
    description = 'Compress and encrypt your private keys',
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
    long_description = '''\
Keystore - Compress and encrypt your private keys
-------------------------------------------------
Keystore requires Python 3.4+.

Install
=======

    pip install -r requirements.txt

Setup your Keystore file in `~/.keystorerc`:

    {
      'keystore': '~/Dropbox/Keystore',
      'folders': [
        '~/.ssh',
      ],
      'verbose': true
    }

Example usage
=============

**Saving keys:**

    $ keystore-save

    Inspecting ~/.ssh:
    Adding /Users/spaxe/.ssh/id_rsa ...
    Adding /Users/spaxe/.ssh/id_rsa.pub ...
    Adding /Users/spaxe/.ssh/known_hosts ...
    Added 3 key(s) to keystore.

    This passphrase is used to decrypt your keystore. Please remember it.
    Please enter a passphrase:
    Please verify your passphrase:
    Passphrase accepted. Encrypting ...
    Keyring successfully created:
    AwGd2MtDWRkOFdyJoRZTdFApvKnoBQ2PXsqqE
    [...]

**Loading keys:**

    $ keystore-load

    Located encrypted keystore at ~/Dropbox/keystore:
    Please enter the passphrase:
    Keyring decrypted successfully.
    File /Users/spaxe/.ssh/id_rsa exists. Are you sure you want to overwrite? (y)/n:
    Writing key to /Users/spaxe/.ssh/id_rsa ...
    File /Users/spaxe/.ssh/id_rsa.pub exists. Are you sure you want to overwrite? (y)/n:
    Writing key to /Users/spaxe/.ssh/id_rsa.pub ...
    File /Users/spaxe/.ssh/known_hosts exists. Are you sure you want to overwrite? (y)/n:
    Writing key to /Users/spaxe/.ssh/known_hosts ...
    Keyring loaded. Restored 3 keys.

**Running tests:**

    python test.py
'''
)