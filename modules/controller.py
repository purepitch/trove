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
        self.view = view
        self.model = model
        self.view.print_info("This is trove " + self.model.version)
        self.view.print_info("Use Ctrl+D to exit, type 'help' or '?' for help.")
        self.view.print_info("")
        self.prompt = "(" + self.model.program + ") "

    # XXX: method name doesn't match what it does
    # XXX: handle has to be called so that this method can be used and tested
    def default(self, line):
        self.view.print_error("Unknown syntax: %s"%line)

    # XXX: what does this method do??
    def emptyline(self):
        pass

    # XXX: what is 'arg' and why isn't it used in this method?
    def do_testcolors(self, arg):
        self.view.print_colors()

    # XXX: what is 'string' and why isn't it used in this method?
    # XXX: why does this method return true?
    def do_exit(self, string):
        self.view.print_info("")
        return True

    # XXX: what is 'string' and why isn't it used in this method?
    # XXX: this is just a repeat of do_exit().  Why is it here?
    # XXX: why does this method return true?  What is this value used for?
    def do_quit(self, string):
        self.view.print_info("")
        return True

    # XXX: what is 'string' and why isn't it used in this method?
    # XXX: why does this method return true?
    def do_EOF(self, string):
        self.view.print_info("\n")
        return True

    # XXX: what is 'string' and why isn't it used in this method?
    # XXX: this is Linux/Unix specific, and could even be shell-specific
    def do_clear(self, string):
        os.system("clear")

    # XXX: what is 'arg' and why isn't it used in this method?
    def do_help(self, arg):
        self.view.print_help()

# vim: expandtab shiftwidth=4 softtabstop=4
