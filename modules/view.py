# -*- coding: utf-8 -*-

"""
A module containing the view-related functionality
"""

class View():
    """
    Class providing the view of the application to the user
    """

    def __init__(self):
        """
        Constructor for the View.
        Defines color codes and puts them into a dictionary.
        """
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
        return None

    def print_ok(self, message):
        """
        Display a success message.
        """
        print "[" + self.codes["green"] + " OK " + self.codes["reset"] + "] " + message

    def print_info(self, message):
        """
        Display an info  message.
        """
        print "[" + self.codes["blue"] + "INFO" + self.codes["reset"] + "] " + message

    def print_warning(self, message):
        """
        Display a warning message.
        """
        print "[" + self.codes["yellow"] + "WARN" + self.codes["reset"] + "] " + message

    def print_fail(self, message):
        """
        Display a failure message.
        """
        print "[" + self.codes["red"] + "FAIL" + self.codes["reset"] + "] " + message

    def print_line(self, message):
        """
        Print the given string to the screen
        """
        print message
        return True

    def print_colors(self):
        """
        Prints all defined text colours to the screen.
        This is just a test routine.
        """
        for key in self.codes:
            print self.codes[key] + "Test" + self.codes["reset"] +  "  " + key
        return True

    def print_details(self, entry, header=True, name=True, user=True,
                      passwd=False, help_text=True, desc=True):
        """
        Prints the details of a single entry. The password is not printed by
        default.
        """
        if header == True:
            self.print_line("Details for [" + entry.name + "]:")
        if name == True:
            self.print_line("  Entry name:  %s" % (entry.name))
        if user == True:
            self.print_line("  User:        %s" % (entry.user))
        if passwd == True:
            self.print_line("  Password:    %s" % (entry.passwd))
        if help_text == True:
            if entry.helptext == "":
                self.print_bold("  There is no help text for this entry.")
            else:
                self.print_line("  Help:        %s" % (entry.helptext))
        if desc == True:
            self.print_line("  Description: %s" % (entry.description))
        return True

    def print_bold(self, message):
        """
        Print the given text in bold
        """
        print self.codes["bold"] + message + self.codes["reset"]
        return True

    def print_error(self, message):
        """
        Print an error message to the screen
        """
        self.print_bold(message)
        return True

    def print_help(self):
        """
        Print the help text to the screen
        """
        self.print_line("")
        self.print_bold('Available commands:')
        self.print_line("")
        self.print_bold('search  <search string>')
        self.print_line("    Search all entry names (case insensitive).")
        self.print_bold('add     <search string>')
        self.print_line("    Add a new entry to the password file.")
        self.print_bold('edit    <search string>')
        self.print_line("    Edit an entry.")
        self.print_bold('del     <search string>')
        self.print_line("    Delete an entry.")
        self.print_bold('psearch <search string>')
        self.print_line("    Search all passwords (exact match, case sensitive).")
        self.print_bold('clear')
        self.print_line("    Clear screen.")
        self.print_bold('exit, quit')
        self.print_line("    Exit this interface (you can also use Ctrl+D)")
        self.print_line("")
        return True

    def print_no_results(self):
        """
        Prints standard error message if a search has no results.
        """
        self.print_line("")
        self.print_error("No result(s) found.")
        return True

    def print_no_valid_choice(self):
        """
        Prints standard error if user has typed an invalid choice.
        """
        self.print_line("")
        self.print_error("Not a valid choice.")
        return True

    def print_overview(self, trove_list):
        """
        Prints a nice table of the form:
        No: / Entry name / User name
        to list search results.
        """
        counter = 1
        num_results = len(trove_list)
        self.print_line("")
        if num_results == 1:
            self.print_line("There is one result:")
        else:
            self.print_line("There are " + str(num_results) + " results:")
        self.print_bold("      %-50s%-20s"%('Entry name',  'User name'))
        for entry in trove_list:
            self.print_line("  %2s: %-50s%-20s"%
                            (str(counter), entry.name, entry.user))
            counter += 1
        return True

    def print_password(self, entry):
        """
        Uses print_details() to only print the password entry.
        """
        self.print_details(entry, header=False, name=False, user=False,
                passwd=True, help_text=False, desc=False)
        return True

    def print_usage(self, command):
        """
        Prints standard message if a command is missing its argument.
        """
        self.print_line("")
        self.print_error("Usage: " + command + "  <search string>")
        self.print_error("You need to provide a search string.")
        return True

    def print_no_git_message(self):
        """
        Prints a message informing the user to install Git
        """
        self.print_fail("Git command not found.")
        self.print_fail("Please install Git before using " +
                               self.model.program_name + ".")

# vim: expandtab shiftwidth=4 softtabstop=4
