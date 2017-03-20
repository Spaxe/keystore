#!/usr/bin/env python3
import os

from keystore import save, load, config_reader

def test_keystore():
  compare_dir = './test/compare'

  print('Testing keystore saving...')

  save.save(keystorerc='.keystorerc', verbose=True)

  if not os.path.exists(compare_dir):
    os.makedirs(compare_dir)

  print('Testing keystore loading...')

  load.load(keystore='testkeystore', copyto='./test/compare', verbose=True)

  print('Comparing before and after...')

  cf = config_reader.read('.keystorerc')
  for f in cf['folders']:
    for dirpath, dirnames, filenames in os.walk(os.path.expanduser(f)):
      original_dir = dirpath
      for filename in filenames:
        original_path = os.path.join(original_dir, os.path.basename(filename))
        copied_path = os.path.join('./test/compare', os.path.basename(filename))
        with open(original_path, 'r') as original, open(copied_path, 'r') as copy:
          assert(original.read() == copy.read())

  print('Test successful.')

if __name__ == '__main__':
  test_keystore()