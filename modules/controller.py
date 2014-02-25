#!/usr/bin/env python 
# -*- coding: utf-8 -*-

from cmd import *
import getpass
import os
import sys

class Controller(Cmd):
    """
    Controller for trove. It is derived from the
    Cmd class for line-oriented command interpreters:
    http://docs.python.org/2/library/cmd.html
    """

    def initialize(self, model, view):
        self.v = view
        self.m = model
        self.v.print_info("This is trove " + self.m.version)
        self.v.print_info("Use Ctrl+D to exit, type 'help' or '?' for help.")
        self.v.print_info("")
        self.prompt = "(" + self.m.program + ") "
        #TODO: Do not hard code passwd file name and make location configurable.
        encryptedfile = sys.path[0] + '/passwd.bfe'
        self.v.print_info("Using encrypted file:")
        self.v.print_info("    " + encryptedfile)
        if os.path.isfile(encryptedfile):
            masterpwd = getpass.getpass('Please enter master passphrase: ')
            self.entry_list = self.m.get_entries(encryptedfile, masterpwd)
        else:
            self.v.print_error("File not found.")
            self.v.print_info("")
            sys.exit(1)
        if len(self.entry_list) == 0:
            self.v.print_info("")
            self.v.print_error("No entries found after decryption.")
            self.v.print_error("Perhaps the passphrase was wrong?")
            self.v.print_info("")
            sys.exit(1)
        else:
            self.v.print_info("Found total number of "
                              + str(len(self.entry_list)) + " entries.")
            self.v.print_info("")

    def default(self, line):
        self.v.print_info("")
        self.v.print_error("Unknown syntax: %s"%line)
        self.v.print_info("")

    def emptyline(self):
        pass

    def do_testcolors(self, arg):
        self.v.print_colors()

    def do_exit(self, s):
        self.v.print_info("")
        return True

    def do_quit(self, s):
        self.v.print_info("")
        return True

    def do_EOF(self, s):
        self.v.print_info("\n")
        return True

    def do_clear(self, s):
        os.system("clear")

    def do_help(self, arg):
        self.v.print_help()

