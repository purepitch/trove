 - when a `passwd.bfe` file doesn't exist, we should create one, set the
   master passphrase and let the program start
 - test program flow from the user's perspective by using the `popen3`
   command.  The `edit`, `search`, `add` etc. commands can thus be
   automatically tested in this manner.

Here is example code for what I mean:

    import os
    (fh_stdin, fh_stdout, fh_stderr) = os.popen3("python trove.py")
    output = fh_stdout.readlines()
    fh_stdin.write('exit')
    fh_stdin.close()
    fh_stdout.close()
    fh_stderr.close()

 - add usage information to the README.  How is one supposed to use the
   program?
 - first start -> look in home dir for a .trove dir with passwd file
 - do you want to start a password file? (if not available)
 - multiple repositories
 - how does search work with multiple repos?
 - use a db such as sqlite instead of a simple text file for the passwd repo?
 - handle privelege levels for users e.g. a new group member should only
   read *some* passwords but not others
