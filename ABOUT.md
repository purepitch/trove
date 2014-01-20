History of this software
========================

This project started as a password management program (csspw) in
Yverdon-les-Bains during the Bacula Admin-I course in 2012. It combines the
advantages of version control with automatic encryption of a password file.
Previously, passwords were on paper: never up to date and often in many
conflicting versions.

The design goals were simple:

  * Encryption with bcrypt ensures that the password file can be decrypted
    without the program.
  * The user should have to enter the passphrase only one time (instead of
    three times, 1x for decryption and 2x for encryption)

Password data could now be stored easily and securely in a central Git
repository. The program ensured that confidential password information was
never commited unencrypted.

Shortcomings:
=============

Like all software, the csspw program is far from perfect:

  * Password database (encrypted file) and csspw program are in the same
    repository
  * With bcrypt you need a common passphrase that all team members have to know.
  * With Debian Wheezy bcrypt is not shipped any more. Starting with Ubuntu 13.04
    bcrypt creates an empty file when the passphrase is wrong instead of simply
    exciting. This case had to be handled special.
  * Git pull and push commands need to be done manually.
  * For each search, add and edit you need to type the passphrase again, because
    csspw code is serial in structure.

This project
============

The trove program will overcome the issues stated above and add new features:

  * Separate repositories for the program and the encrypted password data.
  * Switch to GPG encryption. Every user will need to provide a public key.
    No passphrase needs to be shared.
  * Automatically pull before and push after each change if the (configurable)
    directory is under version control.
  * Introduce continuous mode. Only ask once for private key passphrase.
  * Print only mnemonic by default.
  * Present selection dialog if your search has more than one match (csspw prints
    all results as a list, which can be long if the search term is generic).
  * Make the number and names of stored items configurable. Right now the program
    is only used to store passwords. In principle you can put any kind of
    information into a trove ;-)
  * Handle more than one file with encrypted information.

Future ideas
============

  * Graphical interface
  * Database instead of text file (local: sqlite? with version control, or
    central DB on internal server)
  * More sophisticated management of keys and rights (introduce hierachies)

  
