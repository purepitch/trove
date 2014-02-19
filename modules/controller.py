# -*- coding: utf-8 -*-

from cmd import Cmd
import os

class Controller(Cmd):
    """
    Controller for trove. It is derived from the
    Cmd class for line-oriented command interpreters:
    http://docs.python.org/2/library/cmd.html
    """

    # XXX: maybe more descriptive method name?
    def handle(self, model, view):
        self.v = view
        self.m = model
        self.v.print_info("This is trove " + self.m.version)
        self.v.print_info("Use Ctrl+D to exit, type 'help' or '?' for help.")
        self.v.print_info("")
        self.prompt = "(" + self.m.program + ") "

    # XXX: method name doesn't match what it does
    # XXX: handle has to be called so that this method can be used and tested
    def default(self, line):
        self.v.print_error("Unknown syntax: %s"%line)

    # XXX: what does this method do??
    def emptyline(self):
        pass

    # XXX: what is 'arg' and why isn't it used in this method?
    def do_testcolors(self, arg):
        self.v.print_colors()

    # XXX: what is 's' and why isn't it used in this method?
    # XXX: why does this method return true?
    def do_exit(self, s):
        self.v.print_info("")
        return True

    # XXX: what is 's' and why isn't it used in this method?
    # XXX: this is just a repeat of do_exit().  Why is it here?
    # XXX: why does this method return true?  What is this value used for?
    def do_quit(self, s):
        self.v.print_info("")
        return True

    # XXX: what is 's' and why isn't it used in this method?
    # XXX: why does this method return true?
    def do_EOF(self, s):
        self.v.print_info("\n")
        return True

    # XXX: what is 's' and why isn't it used in this method?
    # XXX: this is Linux/Unix specific, and could even be shell-specific
    def do_clear(self, s):
        os.system("clear")

    # XXX: what is 'arg' and why isn't it used in this method?
    def do_help(self, arg):
        self.v.print_help()

# vim: expandtab shiftwidth=4 softtabstop=4
