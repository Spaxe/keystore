#!/usr/bin/env python3
'''
  keyring - compress and encrypt your private keys
  author: Xavier Ho <contact@xavierho.com>

  License: MIT
'''
import io
import os
import sys
import json
import gzip
import base64
import pathlib
import getpass
import rncryptor
import keyringrc

def load():
  '''decrypt and write out a keyring'''

  config = keyringrc.load()
  if not config:
    print('No configuration found.', file=sys.stderr)
    sys.exit(-1)

  verbose = False
  if 'verbose' in config and config['verbose']:
    verbose = True

  keyring_path = None
  if 'keyring' not in config:
    print('.keyringrc needs to specify a keyring file path.', file=sys.stderr)
    sys.exit(-1)
  elif not pathlib.Path(os.path.expanduser(config['keyring'])).is_file():
    # If keyring file does not exist, nothing to load and exits
    print('keyring does not exist: {}'.format(config['keyring']), file=sys.stderr)
    sys.exit(-1)
  else:
    keyring_path = config['keyring']

  # load and attempt to unencrypt keyring by passphrase

  encrypted_keyring = None
  try:
    with open(os.path.expanduser(keyring_path), 'r') as keyring_file:
      reader_friendly_keyring = keyring_file.read()
      encrypted_keyring = base64.decodebytes(reader_friendly_keyring.encode('utf-8'))

    if verbose: print('Located encrypted keyring at {}:'.format(keyring_path))
    # if verbose: print(reader_friendly_keyring)

    cryptor = rncryptor.RNCryptor()
    decrypted = False
    decrypted_keyring = None
    while not decrypted:
      try:
        passphrase = getpass.getpass('Please enter the passphrase: ')
        decrypted_keyring = cryptor.decrypt(encrypted_keyring, passphrase)

        # NOTE, at this point the file might not have decrypted properly, but
        # we just happen to have gotten a valid UTF-8 string.
        decrypted = True
      except rncryptor.DecryptionError as err:
        print('Invalid passphrase. Please try again.')
      except UnicodeDecodeError as err:
        print('Keyring cannot be decrypted.\nError: {}'.format(err), file=sys.stderr)
        sys.exit(-1)

  except OSError as err:
    print('keyring cannot be opened: {}'.format(err), file=sys.stderr)
    sys.exit(-1)

  # attempt to uncompress the keyring

  # TODO: Compression results in Error -3 while decompressing data: incorrect header check

  # try:
  #   stream = io.BytesIO(decrypted_keyring)
  #   with gzip.GzipFile(fileobj=stream, mode='rb') as decompression:
  #     decompressed_keyring = decompression.read().decode('utf-8')
  # except Exception as err:
  #   print('Passphrase is incorrect. Error: {}'.format(err))
  #   sys.exit(-1)

  decompressed_keyring = decrypted_keyring

  # attempt to unserialise the keyring

  try:
    keyring = json.loads(decompressed_keyring)
  except json.decoder.JSONDecodeError as err:
    print('Either the keyring was not written properly or the passphrase is incorrect.')
    print('Please contact the author about this as it is a serious problem.')
    sys.exit(-1)

  if verbose: print('Keyring decrypted successfully.')

  count = 0
  for filepath, key in keyring.items():
    if os.path.isfile(os.path.expanduser(filepath)):
      confirmed = False
      overwrite = False
      while not confirmed:
        overwrite = input('File {} exists. Are you sure you want to overwrite? (y)/n: '.format(filepath))
        if overwrite == '' or overwrite == 'y' or overwrite == 'Y':
          overwrite = True
          confirmed = True
        elif overwrite == 'n' or overwrite == 'N':
          overwrite = False
          confirmed = True
        else:
          print('Please enter y or n.')
      if not overwrite:
        continue

    # key ready to be created
    if verbose: print('Writing key to {} ...'.format(filepath))
    try:
      with open(filepath, 'w') as keyfile:
        keyfile.write(key)
      count += 1
    except OSError as err:
      print('File system threw an error: {}'.format(err), file=sys.stderr)
      print('Skipping {}'.format(filepath))

  if verbose: print('Keyring loaded. Restored {} keys.'.format(count))

if __name__ == '__main__':
  load()