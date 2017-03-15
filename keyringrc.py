#!/usr/bin/env python3
'''
  keyring - compress and encrypt your private keys
  author: Xavier Ho <contact@xavierho.com>

  License: MIT
'''
import os
import sys
import json

def load():
  path = None

  try:
    if os.path.isfile('./.keyringrc'):
      path = './.keyringrc'
    elif os.path.isfile('~/.keyringrc'):
      path = '~/.keyringrc'
    else:
      raise OSError('The config file .keyringrc is not found in home or local working directory.')

    with open(path) as f:
      conf = json.loads(f.read())
      return conf

  except OSError as err:
    print('Unable to open config: {}'.format(err), file=sys.stderr)
    return None

  except json.JSONDecodeError as err:
    print('Unable to parse config: {}'.format(err), file=sys.stderr)
    return None