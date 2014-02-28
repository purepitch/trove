#!/usr/bin/env python 
# -*- coding: utf-8 -*-

import os

class View():

    def __init__(self):
        colordict ={}
        colordict["reset"]="\x1b[0m"
        colordict["bold"]="\x1b[01m"
        colordict["teal"]="\x1b[36;06m"
        colordict["turquoise"]="\x1b[36;01m"
        colordict["fuscia"]="\x1b[35;01m"
        colordict["purple"]="\x1b[35;06m"
        colordict["blue"]="\x1b[34;01m"
        colordict["darkblue"]="\x1b[34;06m"
        colordict["green"]="\x1b[32;01m"
        colordict["darkgreen"]="\x1b[32;06m"
        colordict["yellow"]="\x1b[33;01m"
        colordict["brown"]="\x1b[33;06m"
        colordict["red"]="\x1b[31;01m"
        colordict["darkred"]="\x1b[31;06m"
        self.codes = colordict
        return None

    def print_info(self, message):
        print message
        return True

    def print_colors(self):
        for key in self.codes:
            print self.codes[key] + "Test" + self.codes["reset"] +  "  " + key
        return True

    def print_bold(self, message):
        print self.codes["bold"] + message + self.codes["reset"]
        return True

    def print_error(self, message):
        self.print_bold(message)
        return True

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
        return True

    def print_no_results(self):
        self.print_info("")
        self.print_error("No results found.")
        self.print_info("")
        return True

    def print_no_valid_choice(self):
        self.print_info("")
        self.print_error("Not a valid choice.")
        self.print_info("")
        return True

    def print_overview(self, trove_list):
        counter = 1
        num_results = len(trove_list)
        self.print_info("")
        self.print_info("There are " + str(num_results) + " results:")
        self.print_bold("      %-50s%-20s"%('Entry name',  'User name'))
        for entry in trove_list:
            self.print_info("  %2s: %-50s%-20s"%
                            (str(counter), entry.name, entry.user))
            counter += 1
        return True

    def print_usage(self, command):
        self.print_info("")
        self.print_error("Usage: " + command + "  <search string>")
        self.print_error("You need to provide a search string.")
        self.print_info("")
        return True

    def print_details(self, entry, name = True, user = True, passwd = False, help = True, desc = True):
        if name == True:
            self.print_info("  Entry name:  %s"%(entry.name))
        if user == True:
            self.print_info("  User:        %s"%(entry.user))
        if passwd == True:
            self.print_info("  Password:    %s"%(entry.passwd))
        if help == True:
            self.print_info("  Help:        %s"%(entry.helptext))
        if desc == True:
            self.print_info("  Description: %s"%(entry.description))
        return True

    def print_password(self, entry):
        self.print_details(entry, name = False, user = False, passwd = True, help = False, desc = False)
        return True
