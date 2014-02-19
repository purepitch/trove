#!/usr/bin/env python 
# -*- coding: utf-8 -*-

import ConfigParser
import hashlib
import subprocess
import re
import os
import sys
import time
from datetime import datetime

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
        self.program    = ""
        self.author     = ""
        self.email      = ""
        self.status     = ""
        self.version    = ""
        self.config = None
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

    def get_config(self, file):
        """
        Reads in the trove configuration file.
        Not used just yet.
        """
        config = ConfigParser.ConfigParser()
        config.read(file)
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

    def get_date(self):
        """
        Returns the current date and time in ISO format.
        """
        now = time.time()
        time_stamp = datetime.fromtimestamp(now).strftime('%Y-%m-%d %H:%M:%S')
        return time_stamp

    def get_entries(self, encryptedfile, masterpasswd):
        """
        Uses functions from csspw to decrypt a bcrypt file with a given
        master passphrase, reads in all entries and encrypts the password
        file again with the same master passphrase. Returns a dictionary with
        SHA1 hashes as keys and TroveEntry objects as values.
        """
        entry_dict = {}
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
            entry_dict = self.extract_entries(passwdfile_lines)
        else:
            os.system("rm -f " + passwdfile)
        return entry_dict

    def encrypt_file(self, filename, passwd):
        f = open(os.devnull, 'w')
        encrypt = subprocess.Popen(['bcrypt',filename], stdin=subprocess.PIPE, stdout=f, stderr=f)
        encrypt.stdin.write(passwd + "\n" + passwd + "\n")
        encrypt.wait()
        f.close()


    def execute(self, command):
        """
        Uses the subprocess module to execute child processes and
        returns the output of these processes to be handled/parsed
        by the calling instance.
        """
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        proc.wait()
        output = proc.communicate()[0]
        return output

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

    def search(self, entry_dict, search_term):
        """
        Searches name fields in a given dictionary (entry_dict) for a
        search term (search_term). Both strings are converted to lower
        case. Returns a list of Trove entry objects, where the regular
        expression search has been successful.
        """
        result_list = []
        for key in entry_dict:
            if re.search(search_term.lower(), (entry_dict[key].name).lower()):
                result_list.append(entry_dict[key])
        return result_list

# vim: expandtab shiftwidth=4 softtabstop=4
