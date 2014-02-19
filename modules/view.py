# -*- coding: utf-8 -*-

class View():

    def __init__(self):
        colordict = {}
        colordict["reset"] = "\x1b[0m"
        colordict["bold"] = "\x1b[01m"
        colordict["teal"] = "\x1b[36;06m"
        colordict["turquoise"] = "\x1b[36;01m"
        colordict["fuscia"] = "\x1b[35;01m"
        colordict["purple"] = "\x1b[35;06m"
        colordict["blue"] = "\x1b[34;01m"
        colordict["darkblue"] = "\x1b[34;06m"
        colordict["green"] = "\x1b[32;01m"
        colordict["darkgreen"] = "\x1b[32;06m"
        colordict["yellow"] = "\x1b[33;01m"
        colordict["brown"] = "\x1b[33;06m"
        colordict["red"] = "\x1b[31;01m"
        colordict["darkred"] = "\x1b[31;06m"
        self.codes = colordict

    def print_info(self, message):
        print message

    # XXX: is this just a test routine?
    def print_colors(self):
        for key in self.codes:
            print self.codes[key] + "Test" + self.codes["reset"] +  "  " + key

    def print_bold(self, message):
        print self.codes["bold"] + message + self.codes["reset"]

    def print_error(self, message):
        self.print_info("")
        self.print_bold(message)
        self.print_info("")

    def print_help(self): 
        self.print_info("")
        self.print_bold('Available commands:')
        self.print_info("")
        self.print_bold('add  [entry]')
        self.print_info("    Add a new entry to your trove.")
        self.print_bold('edit [SHA1]')
        self.print_info("    Edit one of your entries. You will need to provide")
        self.print_info("    a hash key to identify the entry you want to edit.")
        self.print_bold('del  [SHA1]')
        self.print_info("    Delete one of your entries.")
        self.print_bold('search  <search string>')
        self.print_info("    Search all entry names (case insensitive).")
        self.print_bold('psearch <search string>')
        self.print_info("    Search all passwords (exact match).")
        self.print_bold('clear')
        self.print_info("    Clear screen.")
        self.print_bold('exit, quit')
        self.print_info("    Exit this interface (you can also use Ctrl+D)")
        self.print_info("")

# vim: expandtab shiftwidth=4 softtabstop=4
