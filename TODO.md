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
