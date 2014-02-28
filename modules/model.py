#!/usr/bin/env python 
# -*- coding: utf-8 -*-

import ConfigParser
import subprocess
import re
import os
import sys
import time
from datetime import datetime
import csspw

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
        file again with the same master passphrase. Returns a list of ListEntry
        objects.
        """
        entry_list = []
        passwdfile_size = 0
        csspw.decrypt_file(encryptedfile, masterpasswd)
        passwdfile = encryptedfile.rstrip('.bfe')
        if os.path.isfile(passwdfile):
            passwdfile_size = os.path.getsize(passwdfile)
        if passwdfile_size > 0:
            fh = open(passwdfile, 'r')
            passwdfile_lines = fh.readlines()
            fh.close()
            csspw.encrypt_file(passwdfile, masterpasswd)
            entry_list = csspw.extract_entries(passwdfile_lines)
            entry_list = sorted(entry_list, key=lambda entry: entry.name.lower())
        else:
            os.system("rm -f " + passwdfile)
        return entry_list

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

    def search(self, entry_list, search_key):
        """
        Searches a given list (entry_list) for a key (search_key).
        Both strings are converted to lower case. Returns the number
        of results found and the list of results (ListEntry objects).
        """
        result_list = []
        for entry in entry_list:
            if re.search(search_key.lower(), (entry.name).lower()):
                result_list.append(entry)
        result_num = len(result_list)
        return result_num, result_list

