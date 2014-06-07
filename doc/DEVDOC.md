# Developer documentation

## Password file INI format

    [ entry_name ]   # free string
    connection_name: either FQDN, URL, SSID, URI # currently on wishlist
    user:
    password:
    help:            # aka "mnemonic"
    description:
    eid:             # SHA1 hash, calculated from the other info


### Examples

Root user on a Linux/Unix system:

    [ Papa Smurf (Root) ]
    connection_name: papa.smurf.smurf
    user: root
    password: Mh4_l,ifw2as
    help: Mary had a little lamb, its fleece was white as snow
    description: Root access to main smurf computer

MySQL user:

    [ Smurfette DB (MySQL) ]
    connection_name: smurfette_db.smurf.smurf
    user: root
    password: Lah,5la,lah,4la
    help: Lah lah, la la la la, lah, la la la la
    description: Admin access to Smurfette database

GitHub:

    [ Brainy GitHub ]
    connection_name: http://github.com
    user: brainy_smurf
    password: Hmf=iP5?
    help: How much further is it Papa Smurf?
    description: Brainy's account on http://github.com

Wireless internet in a coffee shop:

    [ Hefty Smurf's Heavy Coffee ]
    ssid: HeftyCoffee
    password: smurfilischous
    description: Access info for Hefty's wireless internet

## Startup process

1. startup
2. look for an existing GnuPG setup
    1. if it doesn't exist, ask user to set up GnuPG -> exit
    2. if it exists, how many keys exist
    3. if multiple keys exist, ask which key should be used for en/decryption
3. look for a `.trove` directory
    1. if it doesn't exist, create in `$HOME`
    2. if it exists...
4. look for config file
    1. if it doesn't exist, create
    2. if it exists, read and parse
    3. what to do, if parsing fails?
5. check that "compartments" (defined in config) exist
    1. for each compartment, check that it is a Git repo
    2. for each Git repo, check that it has a remote tracking branch (for optional, automatic git pushes)
6. look for password file
    1. if it doesn't exist -> command loop
    2. if it exists, read and decrypt
7. ask for user passphrase
8. go into command loop

## Encryption process

1. get the list of recipients
2. pass the recipient list to the `gpg` module
3. encrypt the file, appending the `.gpg` extension

## Trove directory structure

    $HOME/.trove/
                 work/    # as an example...
                 private/ # as an example...
                 web/
                     passwords.gpg
                     gpg_recipients.ini
                     keys/
                          bob.asc
                          alice.asc
                          eve.asc
