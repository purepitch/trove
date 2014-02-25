#!/usr/bin/env python 
# -*- coding: utf-8 -*-

import ConfigParser
import subprocess
import re
import os
import sys
import time
from datetime import datetime
from csspw import *

class Model():
    """
    Model for the common license management interface.
    This class handles all business logic.
    """
    def __init__(self):
        self.program    = ""
        self.author     = ""
        self.email      = ""
        self.status     = ""
        self.version    = ""
        self.config = None

    def get_config(self, file):
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
        now = time.time()
        time_stamp = datetime.fromtimestamp(now).strftime('%Y-%m-%d %H:%M:%S')
        return time_stamp

    def get_entries(self, encryptedfile, masterpasswd):
        entry_list = []
        passwdfile_size = 0
        decrypt_file(encryptedfile, masterpasswd)
        passwdfile = encryptedfile.rstrip('.bfe')
        if os.path.isfile(passwdfile):
            passwdfile_size = os.path.getsize(passwdfile)
        if passwdfile_size > 0:
            fh = open(passwdfile, 'r')
            passwdfile_lines = fh.readlines()
            fh.close()
            encrypt_file(passwdfile, masterpasswd)
            entry_list = extract_entries(passwdfile_lines)
            entry_list = sorted(entry_list, key=lambda entry: entry.name.lower())
        else:
            os.system("rm -f " + passwdfile)
        return entry_list

    def execute(self, command):
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        proc.wait()
        output = proc.communicate()[0]
        return output

