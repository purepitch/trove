# -*- coding: utf-8 -*-

"""
A module containing the model-related functionality
"""

import ConfigParser
import hashlib
import subprocess
import re
import os

class TroveEntry:
    def __init__(self):
        self.eid = ""
        self.name = ""
        self.user = ""
        self.passwd = ""
        self.helptext = ""
        self.description = ""

class Model():
    """
    Model for the trove program.
    This class handles all business logic.
    """
    def __init__(self):
        """
        Initializes the Model class for trove with empty member variables.
        """
        self.program_name = ""
        self.version = ""
        self.config = None
        self.entry_dict = {}
        return None

    def calculate_hash(self, entry):
        return hashlib.sha1(entry.name + entry.user + entry.passwd +
                            entry.helptext).hexdigest()

    def check_choice(self, type, choice, maximum = 0):
        """
        Method to verify a user input. Two modes are available:
        1) Integer mode allows for verification of a given integer
        to (a) be an integer indeed and (b) lie within a given range.
        Returns True in this case, False in all other cases.
        2) Boolean mode returns True if the user types either 'y',
        'Y', 'yes' or 'Yes', and returns False in all other cases.
        """
        if type == 'integer':
            if not self.is_int(choice):
                return False
            if (int(choice) > maximum):
                return False
            elif (int(choice) < 1):
                return False
            else:
                return True
        elif type == 'boolean':
            if choice == 'y' or choice == 'Y':
                return True
            elif choice == 'yes' or choice == 'Yes':
                return True
            else:
                return  False
        else:
            return False

    def decrypt_file(self, filename, passwd):
        f = open(os.devnull, 'w')
        decrypt = subprocess.Popen(['bcrypt',filename], stdin=subprocess.PIPE, stdout=f, stderr=f)
        decrypt.stdin.write(passwd + "\n")
        decrypt.wait()
        f.close()

    def is_int(self, s):
        """
        Takes a string s and checks if is an integer
        """
        try:
            int(s)
            return True
        except ValueError:
            return False

    # XXX: this method isn't called anywhere
    # XXX: what does the config file look like?
    # XXX: what config items are we expecting here?
    # XXX: should this method raise an error if the config file doesn't exist?
    def get_config(self, config_file):
        """
        Reads in the trove configuration file.
        Not used just yet.
        """
        config = ConfigParser.ConfigParser()
        config.read(config_file)
        # Fill dictionary with config information:
        section_dict = {}
        for section in config.sections():
            options = config.options(section)
            param_dict = {}
            for option in options:
                param_dict[option] = config.get(section, option)
            section_dict[section] = param_dict
        self.secdict = section_dict
        return self.secdict

    def get_entries(self, encryptedfile, masterpasswd):
        """
        Decrypts a bcrypt file with a given master passphrase, reads in all
        entries and encrypts the password file again with the same master
        passphrase. Fills a dictionary with SHA1 hashes as keys and TroveEntry
        objects as values.
        """
        passwdfile_size = 0
        self.decrypt_file(encryptedfile, masterpasswd)
        passwdfile = encryptedfile.rstrip('.bfe')
        if os.path.isfile(passwdfile):
            passwdfile_size = os.path.getsize(passwdfile)
        if passwdfile_size > 0:
            fh = open(passwdfile, 'r')
            passwdfile_lines = fh.readlines()
            fh.close()
            self.encrypt_file(passwdfile, masterpasswd)
            self.entry_dict = self.extract_entries(passwdfile_lines)
        else:
            # workaround for bcrypt.  If the master passphrase is incorrect,
            # bcrypt creates an *empty* file (0 bytes) (and doesn't warn
            # about this being the case), which would then be encrypted by
            # trove and the old database would be overwritten with this
            # empty file.  Deleting the zero size password file is a
            # workaround so that the database with real data in doesn't get
            # overwritten with empty data.
            os.system("rm -f " + passwdfile)

    def encrypt_file(self, filename, passwd):
        f = open(os.devnull, 'w')
        encrypt = subprocess.Popen(['bcrypt',filename], stdin=subprocess.PIPE, stdout=f, stderr=f)
        encrypt.stdin.write(passwd + "\n" + passwd + "\n")
        encrypt.wait()
        f.close()

    def extract_entries(self, filecontent):
        # TODO: Use config parser to do this!
        mydict = {}
        myentry = TroveEntry()
        for linenumber in range(len(filecontent)):
            line = filecontent[linenumber].strip()
            if (re.search('^\[', line) and re.search('\]$', line)):
                if myentry.name == "":
                    pass
                else:
                    myentry.eid = self.calculate_hash(myentry)
                    mydict[myentry.eid] = myentry
                    del myentry
                    myentry = TroveEntry()
                myentry.name = line.rstrip(']').lstrip('[')
            elif line.split(':')[0] == 'user':
                myentry.user = line.split(':',1)[1].strip()
            elif line.split(':')[0] == 'passwd':
                myentry.passwd = line.split(':',1)[1].strip()
            elif line.split(':')[0] == 'help':
                myentry.helptext = line.split(':',1)[1].strip()
            elif line.split(':')[0] == 'description':
                myentry.description = line.split(':',1)[1].strip()
            if (linenumber == (len(filecontent) - 1)):
                myentry.eid = self.calculate_hash(myentry)
                mydict[myentry.eid] = myentry
            else:
                continue
        return mydict

    def search(self, search_term):
        """
        Searches name fields in self.entry_dict for search_term.
        Both strings are converted to lower case.
        Returns a list of Trove entry objects, where the regular
        expression search has been successful.
        """
        result_list = []
        for key in self.entry_dict:
            if re.search(search_term.lower(), (self.entry_dict[key].name).lower()):
                result_list.append(self.entry_dict[key])
        return result_list

# vim: expandtab shiftwidth=4 softtabstop=4
