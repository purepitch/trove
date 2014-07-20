# -*- coding: utf-8 -*-

"""
A module containing the model-related functionality
"""

import ConfigParser
import hashlib
import subprocess
import re
import os
import datetime

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
        self.config = ConfigParser.ConfigParser()
        self.entries = ConfigParser.ConfigParser()
        self.start_marker = False
        self.end_marker = False
        self.entry_dict = {}
        return None

    def new_entry(self):
        """
        Initialise and return a new ``TroveEntry``.
        """
        return TroveEntry()

    def calculate_hash(self, entry):
        """
        Calculate and return the entry's SHA1 hash.
        """
        return hashlib.sha1(entry.name + entry.user + entry.passwd +
                            entry.helptext + entry.description).hexdigest()

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
        """
        Decrypt the encrypted secrets file.
        """
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
            self.extract_entries(passwdfile)
            self.encrypt_file(passwdfile, masterpasswd)
        else:
            # workaround for bcrypt.  If the master passphrase is incorrect,
            # bcrypt creates an *empty* file (0 bytes) (and doesn't warn
            # about this being the case), which would then be encrypted by
            # trove and the old database would be overwritten with this
            # empty file.  Deleting the zero size password file is a
            # workaround so that the database with real data in doesn't get
            # overwritten with empty data.
            os.system("rm -f " + passwdfile)

    def write_encrypted_file(self, encryptedfile, masterpasswd):
        """
        Write the encrypted data to file using the given master password.
        """
        passwdfile = encryptedfile.rstrip('.bfe')
        ef = open(passwdfile, 'w')
        ef.write("# Auto generated by " + self.program_name + " " +
                 self.version + "\n")
        now = datetime.datetime.now()
        ef.write("# Date: " + datetime.date.strftime(now, "%Y-%m-%d %H:%M:%S") + "\n\n")
        ef.write("# ### TROVE START MARKER ###\n\n")
        for key in self.entry_dict:
            entry = self.entry_dict[key]
            ef.write("[" + entry.name + "]\n")
            ef.write("user: " + entry.user + "\n")
            ef.write("password: " + entry.passwd + "\n")
            ef.write("help: " + entry.helptext + "\n")
            ef.write("description: " + entry.description + "\n\n")
        ef.write("# ### TROVE END MARKER ###\n")
        ef.close()
        os.system("rm -f " + encryptedfile)
        self.encrypt_file(passwdfile, masterpasswd)

    def encrypt_file(self, filename, passwd):
        """
        Encrypt the secrets file.
        """
        f = open(os.devnull, 'w')
        encrypt = subprocess.Popen(['bcrypt',filename], stdin=subprocess.PIPE, stdout=f, stderr=f)
        encrypt.stdin.write(passwd + "\n" + passwd + "\n")
        encrypt.wait()
        f.close()

    def extract_entries(self, filename):
        """
        Extract password entries from the decrypted secrets information.
        """
        fh = open(filename, 'r')
        list_of_lines = fh.readlines()
        fh.close()
        myentry = TroveEntry()
        for line in list_of_lines:
            line = line.strip()
            if (re.search('TROVE START MARKER', line)):
                self.start_marker = True
            if (re.search('TROVE END MARKER', line)):
                self.end_marker = True
        if self.start_marker and self.end_marker:
            self.entries.read(filename)
            for entry in self.entries.sections():
                print entry
                myentry.name = entry
                if 'user' in self.entries.options(entry):
                    myentry.user = self.entries.get(str(entry), 'user')
                if 'password' in self.entries.options(entry):
                    myentry.passwd = self.entries.get(entry, 'password')
                if 'help' in self.entries.options(entry):
                    myentry.helptext = self.entries.get(entry, 'help')
                if 'description' in self.entries.options(entry):
                    myentry.description = self.entries.get(entry, 'description')
                myentry.eid = self.calculate_hash(myentry)
                self.entry_dict[myentry.eid] = myentry
        return

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

    def password_search(self, search_term):
        """
        Searches password fields in self.entry_dict for search_term.
        Returns a list of Trove entry objects, where the regular
        expression search has been successful.
        """
        result_list = []
        for key in self.entry_dict:
            if re.search(search_term, (self.entry_dict[key].passwd)):
                result_list.append(self.entry_dict[key])
        return result_list

    def execute(self, command):
        """
        Run the given command in a subprocess.
        """
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        proc.wait()
        return_value = proc.poll()
        output = proc.communicate()[0]
        return return_value, output

# vim: expandtab shiftwidth=4 softtabstop=4
