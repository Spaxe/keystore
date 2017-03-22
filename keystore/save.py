#!/usr/bin/env python3
'''keystore - compress and encrypt your private keys
  author: Xavier Ho <contact@xavierho.com>

Usage:
  save.py [options] --keystorerc <keystorerc>
  save.py [options] <keystore> <files>...
  save.py (-h | --help)
  save.py --version

Options:
  --keystorerc <keystorerc>   Specify .keystorerc file path.
  -v --verbose                Print out extra information.
  -h --help                   Show this screen.
  --version                   Show version.
'''
import io
import os
import sys
import json
import gzip
import base64
import pathlib
import getpass
import traceback

import simplecrypt
from docopt import docopt

from keystore import config_reader, __version__

def save(keystorerc=None, keystore=None, files=[], verbose=False):
  '''create a keystore, compress and encrypt to file'''

  config = None
  if keystorerc:
    config = config_reader.read(keystorerc)
    if not config:
      print('No configuration found.', file=sys.stderr)
      sys.exit(-1)
  elif keystore and len(files) > 0:
    config = {
      'keystore': keystore,
      'files': files
    }

  if 'verbose' in config and config['verbose']:
    verbose = True

  keystore_path = None
  if 'keystore' not in config:
    print('.keystorerc needs to specify a keystore file path.', file=sys.stderr)
    sys.exit(-1)

  keystore_path = os.path.expanduser(config['keystore'])
  if os.path.isdir(keystore_path):
    print('keystore cannot be a folder: {}'.format(config['keystore']), file=sys.stderr)
    sys.exit(-1)
  elif not os.path.isfile(keystore_path):
    # If keystore file does not exist already, attempt to create one
    try:
      pathlib.Path(keystore_path).touch()
    except OSError as err:
      print('keystore cannot be accessed: {}\n{}'.format(config['keystore'], err), file=sys.stderr)
      sys.exit(-1)

  # iterate through keys and add them here

  keystore = {}
  try:
    for p in config['files']:

      expanded_path = os.path.expanduser(p)
      path = pathlib.Path(expanded_path)
      if verbose: print('Inspecting {}:'.format(expanded_path))

      if not path.exists():
        print('Error: File or folder does not exist: {}'.format(p), file=sys.stderr)
        sys.exit(-1)
      if path.is_dir():
        for dirpath, dirnames, filenames in os.walk(expanded_path):
          for name in filenames:
            fullpath = os.path.join(dirpath, name)
            if verbose: print('Adding {} ...'.format(fullpath))
            with open(fullpath, 'rb') as keyfile:
              b64_bytes = base64.encodebytes(keyfile.read()).decode('utf-8')
              keystore[fullpath] = b64_bytes
      elif path.is_file():
        fullpath = expanded_path
        if verbose: print('Adding {} ...'.format(fullpath))
        with open(fullpath, 'rb') as keyfile:
          b64_bytes = base64.encodebytes(keyfile.read()).decode('utf-8')
          keystore[fullpath] = b64_bytes

    if verbose: print('Added {} key(s) to keystore.\n'.format(len(keystore)))

    # prompt user for a one-time passphase for encryption

    do_passphrases_match = False
    passphrase = None
    print('This passphrase is used to decrypt your keystore. Please remember it.')
    while not do_passphrases_match:
      passphrase = getpass.getpass('Please enter a passphrase: ')
      passphrase_verify = getpass.getpass('Please verify your passphrase: ')
      do_passphrases_match = passphrase != '' and passphrase == passphrase_verify
      if passphrase == '':
        print('Passphrase cannot be empty.')
      elif not do_passphrases_match:
        print('Passphrases do not match. Please try again.')
    if verbose: print('Passphrase accepted. Encrypting ...')

    # serialise, compress, encrypt

    serial_keystore = json.dumps(keystore)
    compressed_keystore = gzip.compress(serial_keystore.encode('utf-8'))
    try:
      encrypted_keystore = simplecrypt.encrypt(passphrase, compressed_keystore)
    except simplecrypt.EncryptionException as err:
      print('You managed to bump into a very, very rare issue with AES.\nPlease contact the author. {}'.format(err), file=sys.stder)
      sys.exit(-1)

    # save encrypted keystore to file
    keystore_path = os.path.expanduser(keystore_path)
    if verbose: print('Writing to keystore file {}'.format(keystore_path))

    with open(keystore_path, 'wb') as keystore_file:
      keystore_file.write(encrypted_keystore)

    if verbose: print('Keystore successfully created: ')
    if verbose: print(encrypted_keystore)

  except KeyError as err:
    print('.keystorerc config is missing `files` attribute: {}'.format(err), file=sys.stderr)
    sys.exit(-1)
  except TypeError as err:
    print('Error: {}'.format(err), file=sys.stderr)
    traceback.print_exc()
    sys.exit(-1)
  except OSError as err:
    print('The file system gave an error: {}'.format(err), file=sys.stderr)
    sys.exit(-1)
  except Exception as err:
    print('Serious error. Please report this bug to the author: {}'.format(err), file=sys.stderr)
    sys.exit(-1)

if __name__ == '__main__':
  arguments = docopt(__doc__, version=__version__)

  if arguments['--keystorerc']:
    save(
      keystorerc=arguments['--keystorerc'],
      verbose=arguments['--verbose']
    )
  elif arguments['<keystore>'] and arguments['<files>']:
    save(
      keystore=arguments['<keystore>'],
      files=arguments['<files>'],
      verbose=arguments['--verbose']
    )