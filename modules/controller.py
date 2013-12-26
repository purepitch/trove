#!/usr/bin/env python 
# -*- coding: utf-8 -*-

from cmd import *
import os

class Controller(Cmd):
    """
    Controller for trove. It is derived from the
    Cmd class for line-oriented command interpreters:
    http://docs.python.org/2/library/cmd.html
    """

    def handle(self, model, view):
        self.v = view
        self.m = model
        self.v.print_info("This is trove " + self.m.version)
        self.v.print_info("Use Ctrl+D to exit, type 'help' or '?' for help.")
        self.v.print_info("")
        self.prompt = "(" + self.m.program + ") "

    def default(self, line):
        self.v.print_error("Unknown syntax: %s"%line)

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

