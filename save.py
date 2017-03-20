#!/usr/bin/env python3
'''
  keystore - compress and encrypt your private keys
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
import traceback
import keystorerc

def save():
  '''create a keystore, compress and encrypt to file'''

  config = keystorerc.load()
  if not config:
    print('No configuration found.', file=sys.stderr)
    sys.exit(-1)

  verbose = False
  if 'verbose' in config and config['verbose']:
    verbose = True

  keystore_path = None
  if 'keystore' not in config:
    print('.keystorerc needs to specify a keystore file path.', file=sys.stderr)
    sys.exit(-1)
  elif not pathlib.Path(os.path.expanduser(config['keystore'])).is_file():
    # If keystore file does not exist already, attempt to create one
    try:
      pathlib.Path(os.path.expanduser(config['keystore'])).touch()
    except OSError as err:
      print('keystore cannot be accessed: {}\n{}'.format(config['keystore'], err), file=sys.stderr)
      sys.exit(-1)
  else:
    keystore_path = config['keystore']

  # iterate through keys and add them here

  keystore = {}
  try:
    for path in config['folders']:

      if verbose: print('Inspecting {}:'.format(path))
      for dirpath, dirnames, filenames in os.walk(os.path.expanduser(path)):
        for name in filenames:
          fullpath = os.path.join(dirpath, name)
          if verbose: print('Adding {} ...'.format(fullpath))
          with open(fullpath) as keyfile:
            keystore[fullpath] = keyfile.read()

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
    # TODO: Compression causes loader to error out.
    # stream = io.BytesIO()
    # with gzip.GzipFile(fileobj=stream, mode='wb') as compression:
    #   compression.write(serial_keystore.encode('utf-8'))
    # compressed_keystore = stream.getvalue()
    cryptor = rncryptor.RNCryptor()
    encrypted_keystore = cryptor.encrypt(serial_keystore, passphrase)
    writer_friendly_keystore = base64.encodebytes(encrypted_keystore).decode('utf-8')

    # save encrypted keystore to file

    with open(os.path.expanduser(keystore_path), 'w') as keystore_file:
      keystore_file.write(writer_friendly_keystore)

    if verbose: print('Keyring successfully created: ')
    if verbose: print(writer_friendly_keystore)

  except KeyError as err:
    print('.keystorerc config is missing `folders` attribute: {}'.format(err), file=sys.stderr)
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
  save()