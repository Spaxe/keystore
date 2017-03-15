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
import traceback
import keyringrc

def save():
  '''create a keyring, compress and encrypt to file'''

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
    # If keyring file does not exist already, attempt to create one
    try:
      pathlib.Path(os.path.expanduser(config['keyring'])).touch()
    except OSError as err:
      print('keyring cannot be accessed: {}\n{}'.format(config['keyring'], err), file=sys.stderr)
      sys.exit(-1)
  else:
    keyring_path = config['keyring']

  # iterate through keys and add them here

  keyring = {}
  try:
    for path in config['folders']:

      if verbose: print('Inspecting {}:'.format(path))
      for dirpath, dirnames, filenames in os.walk(os.path.expanduser(path)):
        for name in filenames:
          fullpath = os.path.join(dirpath, name)
          if verbose: print('Adding {} ...'.format(fullpath))
          with open(fullpath) as keyfile:
            keyring[fullpath] = keyfile.read()

    if verbose: print('Added {} key(s) to keyring.\n'.format(len(keyring)))

    # prompt user for a one-time passphase for encryption

    do_passphrases_match = False
    passphrase = None
    print('This passphrase is used to decrypt your keyring. Please remember it.')
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

    serial_keyring = json.dumps(keyring)
    # TODO: Compression causes loader to error out.
    # stream = io.BytesIO()
    # with gzip.GzipFile(fileobj=stream, mode='wb') as compression:
    #   compression.write(serial_keyring.encode('utf-8'))
    # compressed_keyring = stream.getvalue()
    cryptor = rncryptor.RNCryptor()
    encrypted_keyring = cryptor.encrypt(serial_keyring, passphrase)
    writer_friendly_keyring = base64.encodebytes(encrypted_keyring).decode('utf-8')

    # save encrypted keyring to file

    with open(os.path.expanduser(keyring_path), 'w') as keyring_file:
      keyring_file.write(writer_friendly_keyring)

    if verbose: print('Keyring successfully created: ')
    if verbose: print(writer_friendly_keyring)

  except KeyError as err:
    print('.keyringrc config is missing `folders` attribute: {}'.format(err), file=sys.stderr)
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