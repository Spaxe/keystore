# Keyring - keeps your keys in one place.

## THIS IS AN EXPERIMENT. DO NOT USE IN PRODUCTION.

### Example usage:

**Saving keys:**

    Inspecting ~/.ssh:
    Adding /Users/spaxe/.ssh/id_rsa ...
    Adding /Users/spaxe/.ssh/id_rsa.pub ...
    Adding /Users/spaxe/.ssh/known_hosts ...
    Added 3 key(s) to keyring.

    This passphrase is used to decrypt your keyring. Please remember it.
    Please enter a passphrase:
    Please verify your passphrase:
    Passphrase accepted. Encrypting ...
    Keyring successfully created:
    AwGd2MtDWRkOFdyJoRZTdFApvKnoBQ2PXsqqE
    [...]

**Loading keys:**

    Located encrypted keyring at ~/Dropbox/keyring:
    Please enter the passphrase:
    Keyring decrypted successfully.
    File /Users/spaxe/.ssh/id_rsa exists. Are you sure you want to overwrite? (y)/n:
    Writing key to /Users/spaxe/.ssh/id_rsa ...
    File /Users/spaxe/.ssh/id_rsa.pub exists. Are you sure you want to overwrite? (y)/n:
    Writing key to /Users/spaxe/.ssh/id_rsa.pub ...
    File /Users/spaxe/.ssh/known_hosts exists. Are you sure you want to overwrite? (y)/n:
    Writing key to /Users/spaxe/.ssh/known_hosts ...
    Keyring loaded. Restored 3 keys.

# License
© Xavier Ho <contact@xavierho.com>

License under MIT License.
