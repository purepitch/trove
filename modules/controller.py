# -*- coding: utf-8 -*-

"""
A module containing the controller-related functionality
"""

import ConfigParser
import getpass
from cmd import Cmd
import os
import sys

class Controller(Cmd):
    """
    Controller for trove. It is derived from the
    Cmd class for line-oriented command interpreters:
    http://docs.python.org/2/library/cmd.html
    """

    def __init__(self, model, view):
        """
        The constructor from Cmd is extended:
        Model and View objects are added as entities to the controller.
        A welcome message is printed and the prompt gets set.
        """
        Cmd.__init__(self)
        self.view = view
        self.model = model
        self.masterpwd = ""
        self.prompt = "\n(" + self.model.program_name + ") "
        self.encrypted_file = os.path.join(os.getcwd(), 'passwd.bfe')
        self.config_file = os.path.join(os.getcwd(), 'trove.conf')
        return None

    def default(self, arg):
        """
        Print an error message if syntax is unknown.
        """
        if arg == ".":
            self.emptyline()
            return None
        self.view.print_info("")
        self.view.print_error("Unknown syntax: %s" % arg)
        return None

    def do_clear(self, arg):
        """
        Calls the Linux 'clear' command to clear the screen.
        """
        os.system("clear")
        return None

    def do_EOF(self, arg):
        """
        Ctrl+D is one way to exit the application.
        """
        self.view.print_info("\n")
        return True

    def emptyline(self):
        """
        Handle the case that no command is given.
        """
        return None

    def do_testcolors(self, arg):
        """
        Prints the colour test output to the screen.
        """
        self.view.print_colors()

    def do_exit(self, arg):
        """
        Exits the application.
        """
        self.view.print_info("")
        return True

    def do_help(self, arg):
        """
        Prints a help text to help the user remember the commands available.
        This method is also called then typing '?'.
        """
        self.view.print_help()
        return None

    def do_quit(self, arg):
        """
        Another way to exit the application.
        """
        self.view.print_info("")
        return True

    def do_search(self, arg):
        """
        Performs a search for 'arg' in all entry names. If more than one result
        is found, the selection is presented and the user can choose the entry
        to be displayed. By default the password itself is not shown, only the help
        text. However, the user can choose to see the password in a second step.
        """
        if not arg:
            self.view.print_usage('search')
            return None
        results = self.model.search(arg)
        self.show_result_listing(results)
        entry = self.choose_from_list(results)
        if (entry == None):
            return None
        if (entry.helptext != ""):
            self.view.print_details(entry)
            choice = raw_input("Show password? (y/N) ")
            yes = self.model.check_choice('boolean', choice)
            if yes:
                self.view.print_password(entry)
        else:
            self.view.print_bold("There is no help text for this entry.")
            self.view.print_details(entry, passwd = True)
        return None

    def do_psearch(self, arg):
        """
        Performs a search for 'arg' in the password field. This search is
        case sensitive. Presents a list of all entries that contain this
        password.
        """
        if not arg:
            self.view.print_usage('search')
            return None
        results = self.model.password_search(arg)
        self.show_result_listing(results)
        return None

    def choose_from_list(self, results):
        """
        Displays the list 'results' in a nice way and asks user to
        pick one result. Returns entry object to calling method.
        """
        result_num = len(results)
        if result_num == 1:
            entry = results[0]
        else:
            choice = raw_input("Select item: (1-" + str(result_num) + ") ")
            if choice == ".":
                return None
            success = self.model.check_choice('integer', choice, result_num)
            if success:
                entry = results[int(choice) - 1]
            else:
                self.view.print_no_valid_choice()
                return None
        return entry

    def show_result_listing(self, results):
        result_num = len(results)
        if (result_num == 0):
            self.view.print_no_results()
            return None
        else:
            results = sorted(results, key=lambda entry: entry.name.lower())
            self.view.print_overview(results)

    def read_encrypted_file(self):
        """
        Reads the bcrypted file 'passwd.bfe' in the current directory and
        calls the model's method to fill the dictionary of objects with
        decrypted content. SHA1 hashes are keys and TroveEntry objects are
        values of this dictionary.
        """
        #TODO: Do not hard code passwd file name and make location configurable.
        self.view.print_info("Using encrypted file:")
        self.view.print_info("    " + self.encrypted_file)
        if os.path.isfile(self.encrypted_file):
            self.masterpwd = getpass.getpass('Please enter master passphrase: ')
            self.model.get_entries(self.encrypted_file, self.masterpwd)
        else:
            self.view.print_error("File not found.")
            self.view.print_info("")
            sys.exit(1)
        return None

    def check_db_for_entries(self):
        """
        Prints an error message if it finds no entries in self.model.entry_dict.
        Otherwise it informs how many entries were found.
        """
        # TODO: This should be done differently. The success of the decryption
        # process should be directly available. It should not be necessary to
        # count the number of entries to guess this. Unfortunately the bcrypt
        # program gives the same return value in both cases, so it cannot be used
        # right now. Perhaps the switch to GPG will help.
        if len(self.model.entry_dict.keys()) == 0:
            self.view.print_info("")
            self.view.print_error("No entries found after decryption.")
            self.view.print_error("Perhaps the passphrase was wrong?")
            self.view.print_info("")
            sys.exit(1)
        else:
            self.view.print_info("Found total number of "
                              + str(len(self.model.entry_dict.keys())) + " entries.")
        return None

    def do_del(self, arg):
        if not arg:
            self.view.print_usage('del')
            return None
        results = self.model.search(arg)
        entry = self.choose_from_list(results)
        if entry != None:
            decision = raw_input("Really delete this entry? (Type 'yes') ")
            if decision != "yes":
                return None
            else:
                del self.model.entry_dict[entry.eid]
                self.view.print_info("Entry [" + entry.name + "] deleted.")
                self.model.write_encrypted_file(self.encrypted_file, self.masterpwd)
                self.view.print_info("Update written to disk: " + self.encrypted_file)
        return None

    def do_add(self, arg):
        entry = self.model.new_entry()
        self.do_edit("this is the add case", entry)

    def do_edit(self, arg, entry = None):
        if not arg:
            self.view.print_usage('edit')
            return None
        if entry == None:
            results = self.model.search(arg)
            entry = self.choose_from_list(results)
        if entry != None:
            original_entry_id = entry.eid
            name = self.ask_for("Name", entry.name)
            if name == ".":
                return None
            else:
                entry.name = name
            user = self.ask_for("User", entry.user)
            if user == ".":
                return None
            else:
                entry.user = user
            passwd = self.ask_for("Password", entry.passwd)
            if passwd == ".":
                return None
            else:
                entry.passwd = passwd
            helptext = self.ask_for("Help", entry.helptext)
            if helptext == ".":
                return None
            else:
                entry.helptext = helptext
            description = self.ask_for("Description", entry.description)
            if description == ".":
                return None
            else:
                entry.description = description
            entry.eid = self.model.calculate_hash(entry)
            if original_entry_id != "":
                del self.model.entry_dict[original_entry_id]
            self.model.entry_dict[entry.eid] = entry
            self.view.print_info("Writing encrypted file: " + self.encrypted_file)
            self.model.write_encrypted_file(self.encrypted_file, self.masterpwd)
        return None

    def ask_for(self, prompt, value):
        new_value = raw_input(prompt + " ["+ value + "]: ")
        if new_value == "":
            return value
        elif new_value == "~~":
            return ""
        else:
            return new_value

    def create_encrypted_file(self):
        if len(self.config.sections()) == 1:
            self.view.print_info("")
            self.view.print_error("You seem to have no encrypted stores defined.")
            self.create_store()
        if len(self.config.sections()) > 1:
            sections_without_general = self.config.sections()
            sections_without_general.remove('General')
            for section in sections_without_general:
                if self.config.has_option(section, 'file'):
                    self.encrypted_file = self.config.get(section, 'file')
                    break
                else:
                    self.view.print_info("")
                    self.view.print_error("No key 'file' found in section " + section)
        if len(self.config.sections()) > 2:
            self.view.print_info("")
            self.view.print_bold("Your trove config file contains more than")
            self.view.print_bold("two sections. up to now only one file for")
            self.view.print_bold("encrypted storage is supported.")
            self.view.print_info("")
            self.view.print_bold("Using first section which has a 'file' key.")

    def create_store(self):
        pass

    def print_hello_message(self):
        self.view.print_info("This is " + self.model.program_name + " " + self.model.version)
        self.view.print_info("Use Ctrl+D to exit, type 'help' or '?' for help.")
        self.view.print_info("")

    def run_startup_checks(self):
        #self.check_if_git_is_installed() #!! Not yet implemented!
        #self.check_if_trove_dir_exists() # Not yet necessary, we are working in PWD
        self.check_if_config_file_exists()
        #self.check_if_encrypt_dir_is_a_git_repo()
        #if self.is_git == True:
        #    self.check_if_git_has_remote()

    def check_if_git_is_installed(self):
        """
        Checks if Git is installed
        (not yet implemented)
        """
        pass
    
    def check_if_trove_dir_exists(self):
        """
        Checks if directory $HOME/.trove exists.
        If not it will be created.
        (not active yet)
        """
        trove_dir = os.path.join(os.getenv('HOME'), '.trove')
        if not os.path.isdir(trove_dir):
            pass
            #print "mkdir trove_dir"
            #os.makedirs(trove_dir)
            #os.system("mkdir " + trove_dir)
    
    def check_if_config_file_exists(self):
        """
        Checks if config file in model.config_file exists.
        If not it will be created with a default [General] section.
        """
        self.model.config = ConfigParser.ConfigParser()
        if os.path.isfile(self.config_file):
            print "Reading config file: " + self.config_file
            self.model.config.read(self.config_file)
        else:
            print "No config file found."
            print "Writing new config file: " + self.config_file
            print "with default parameters."
            self.add_general_section_to_config()
        if not self.model.config.has_section('General'):
            print "No section 'General' found."
            print "Adding new section with defaults."
            self.add_general_section_to_config()
    
    def add_general_section_to_config(self):
        """
        Adds a [General] section to the trove configuration file
        if it is not present.
        """
        self.model.config.add_section('General')
        self.model.config.set('General', 'color', 'True')
        self.model.config.set('General', 'warning', 'True')
        self.write_config_file()
    
    def write_config_file(self):
        """
        Writes the trove configuration file to disk.
        """
        config_file_handle = open(self.config_file, 'w')
        self.model.config.write(config_file_handle)
        config_file_handle.close()

# vim: expandtab shiftwidth=4 softtabstop=4
