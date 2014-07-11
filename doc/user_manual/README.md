# Trove: How does this program work?

## Start of the program

When started for the first time, trove will look for a config file (trove.conf)
in the same directory where trove.py resides (the location of trove.conf will
change soon to $HOME/.trove/trove.conf).

If it does not find the config file, it will create it.

It will look for a section named [General] in the config file. If it is not
there, it will add one, and write the extended config file to disk.

## You do not have a file encrypted with bcrypt?

When there is no other section than [General] or there is no encrypted file
defined, trove will automatically add another section [Passwords] with default
values to the config file and it will create an empty encrypted file
'passwd.bfe' in the same directory where trove.py resides (the default location
of encrypted storages will change soon to $HOME/.trove/repositories/repo_name).

## You already have a file encrypted with bcrypt?

You should write a trove.conf file yourself with an entry of the following form:

    [Repository name, e.g. Work, Private ...]
    path: /path/to/encrypted/file
    file: encrypted_file_name.bfe
    type: bcrypt

Trove will look for this section in the config file and read it in. When an
encrypted file is defined (up to now only bcrypt is supported), it will ask for
the passphrase, decrypt the file, store its content internally and encrypt the
file again.

The encrypted file should be an ASCII file with one or more entries of the form:

    [ Papa Smurf (Root) ]                                                       
    user: root                                                                  
    password: Mh4_l,ifw2as                                                      
    help: Mary had a little lamb, its fleece was white as snow                  
    description: Root access to main smurf computer

The file should be encrypted with bcrypt using a strong passphrase.

If you have an encrypted file and have started Trove without writing a config
file first, just edit the trove.conf that was created automatically. Enter the
path and filename of your encrypted file and start the program again.


