Keystore - keeps your keys in one place.
----------------------------------------

THIS IS AN EXPERIMENT. DO NOT USE IN PRODUCTION.
================================================

Prerequisites
=============
Python 3.4+.

Install
=======
You can install straight from `pip`.

    pip install keystore

Before using it for the first time, you will need to setup a `~/.keystorerc` in
your home directory.

    {
      "keystore": "~/Dropbox/keystore",
      "files": [
        "~/.ssh",
        "~/.gnupg/gpg-agent.conf",
        "~/.gnupg/gpg.conf",
        "~/.gnupg/private-keys-v1.d",
        "~/.gnupg/pubring.gpg",
        "~/.gnupg/secring.gpg",
        "~/.gnupg/trustdb.gpg",
      ],
      "verbose": true
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

**Loading keys to the same directory (useful for a new machine):**

    $ mkdir keys
    $ keystore-load --copy-to keys

    Located encrypted keystore at ~/Dropbox/keystore:
    Please enter the passphrase:
    Keyring decrypted successfully.
    Writing key to /Users/spaxe/keys/id_rsa ...
    Writing key to /Users/spaxe/keys/id_rsa.pub ...
    Writing key to /Users/spaxe/keys/known_hosts ...
    Keyring loaded. Restored 3 keys.

**Running tests:**

    python3 test.py

License
=======
© Xavier Ho <contact@xavierho.com>

License under MIT License.
