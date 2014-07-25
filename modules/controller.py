# -*- coding: utf-8 -*-

"""
A module containing the controller-related functionality
"""

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
        self.encrypted_file = ""
        self.config_dir = os.getcwd()
        self.std_encrypted_file_name = 'passwords.txt.bfe'
        return None

    def default(self, arg):
        """
        Print an error message if syntax is unknown.
        """
        if arg == ".":
            self.emptyline()
            return None
        self.view.print_line("")
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
        self.view.print_line("\n")
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
        self.view.print_line("")
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
        self.view.print_line("")
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
        results = sorted(results, key=lambda entry: entry.name.lower())
        self.show_result_listing(results)
        entry = self.choose_from_list(results)
        if (entry != None):
            self.view.print_details(entry)
            choice = raw_input("Show password? (y/N) ")
            yes = self.model.check_choice('boolean', choice)
            if yes:
                self.view.print_password(entry)
        return None

    def do_psearch(self, arg):
        """
        Performs a search for 'arg' in the password field. This search is
        case sensitive. Presents a list of all entries that contain this
        password.
        """
        if not arg:
            self.view.print_usage('psearch')
            return None
        results = self.model.password_search(arg)
        results = sorted(results, key=lambda entry: entry.name.lower())
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
        """
        Display search results
        """
        result_num = len(results)
        if (result_num == 0):
            self.view.print_no_results()
            return None
        else:
            self.view.print_overview(results)

    def read_encrypted_file(self):
        """
        Reads the bcrypted file stored in self.encrypted_file and
        calls the model's method to fill the dictionary of objects with
        decrypted content. SHA1 hashes are keys and TroveEntry objects are
        values of this dictionary.
        """
        self.view.print_info("Encrypted file defined in configuration.")
        if os.path.isfile(self.encrypted_file):
            self.view.print_ok(self.encrypted_file)
            self.masterpwd = getpass.getpass('Please enter master passphrase: ')
            self.model.get_entries(self.encrypted_file, self.masterpwd)
        else:
            self.view.print_fail(self.encrypted_file)
            self.view.print_fail("File not found.")
            self.view.print_line("")
            sys.exit(1)
        return None

    def check_db_for_entries(self):
        """
        Prints an error message if it finds no entries in self.model.entry_dict.
        Otherwise it informs how many entries were found.
        """
        if self.model.start_marker  == False or self.model.end_marker == False:
            self.view.print_line("")
            self.view.print_error("No entries found after decryption.")
            self.view.print_error("Perhaps the passphrase was wrong?")
            self.view.print_line("")
            sys.exit(1)
        elif len(self.model.entry_dict.keys()) == 0:
            self.view.print_info("No entries found.")
        elif len(self.model.entry_dict.keys()) == 1:
            self.view.print_info("One entry found.")
        else:
            self.view.print_info(str(len(self.model.entry_dict.keys())) + " entries found.")
        return None

    def do_del(self, arg):
        """
        Handle deleting an entry
        """
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
                self.view.print_line("Entry [" + entry.name + "] deleted.")
                self.model.write_encrypted_file(self.encrypted_file, self.masterpwd)
                self.view.print_line("Update written to disk: " + self.encrypted_file)
        return None

    def do_add(self, arg):
        """
        Handle adding an entry
        """
        entry = self.model.new_entry()
        self.do_edit("this is the add case", entry)

    def do_edit(self, arg, entry = None):
        """
        Handle editing an entry
        """
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
            self.view.print_info("Writing encrypted file: ")
            self.view.print_ok(self.encrypted_file)
            self.model.write_encrypted_file(self.encrypted_file, self.masterpwd)
        return None

    def ask_for(self, prompt, value):
        """
        Prompt for a given value

        param: str prompt
        param: str value
        """
        new_value = raw_input(prompt + " ["+ value + "]: ")
        if new_value == "":
            return value
        elif new_value == "~~":
            return ""
        else:
            return new_value

    def create_encrypted_file(self):
        """
        Create an encrypted file.

        This is useful in the initialisation step when the input encrypted
        file does not yet exist.
        """
        pass

    def create_store(self):
        """
        Create a store.

        This is useful in the initialisation step when the input encrypted
        store does not yet exist.
        """
        pass

    def print_hello_message(self):
        """
        Print a welcome message at program start
        """
        self.view.print_line("This is " + self.model.program_name + " " + self.model.version)
        self.view.print_line("Use Ctrl+D to exit, type 'help' or '?' for help.")
        self.view.print_line("")

    def run_startup_checks(self):
        """
        Run various checks necessary at program startup.
        """
        if not self.git_is_installed():
            self.view.print_no_git_message()
            sys.exit(1)
        if not self.trove_dir_exists():
            # self.create_trove_dir()
            pass
        if self.config_file_exists():
            self.read_config_file()
        else:
            self.create_config_file()
        if not self.config_file_has_general_section():
            self.add_general_section_to_config()
        #if not self.encrypt_dir_is_git_repo():
        #    self.encrypt_dir_git_init()
        #if self.encrypt_dir_git_has_remote():
        #    self.model.remote = True

    def git_is_installed(self):
        """
        Checks if Git is installed
        """
        return_value, output = self.model.execute('git --version')
        if (return_value != 0):
            return False
        else:
            return True

    def trove_dir_exists(self):
        """
        Checks if directory $HOME/.trove exists.
        """
        trove_dir = os.path.join(os.getenv('HOME'), '.trove')
        return os.path.isdir(trove_dir)

    def create_trove_dir(self):
        """
        Creates directory $HOME/.trove
        """
        trove_dir = os.path.join(os.getenv('HOME'), '.trove')
        self.view.print_info("Creating directory")
        self.view.print_ok(treove_dir)
        os.makedirs(trove_dir)

    def config_file_exists(self):
        """
        Checks if config file $TROVEDIR/trove.conf exists.
        """
        config_file = os.path.join(self.config_dir, 'trove.conf')
        return os.path.isfile(config_file)

    def read_config_file(self):
        """
        Reads config file $TROVEDIR/trove.conf.
        """
        config_file = os.path.join(self.config_dir, 'trove.conf')
        self.view.print_info("Reading config file:")
        self.model.config.read(config_file)
        self.view.print_ok(config_file)

    def create_config_file(self):
        """
        Creates config file $TROVEDIR/trove.conf.
        """
        config_file = os.path.join(self.config_dir, 'trove.conf')
        self.view.print_info("No config file found.")
        self.view.print_info("Writing new config file with default parameters.")
        self.add_general_section_to_config(verbose=False)
        self.view.print_ok(config_file)

    def config_file_has_general_section(self):
        """
        Checks if config file $TROVEDIR/trove.conf has section [General].
        """
        return self.model.config.has_section('General')

    def add_general_section_to_config(self, verbose=True):
        """
        Adds a section [General] to the configuration file.
        """
        if verbose:
            self.view.print_info("No section 'General' found.")
            self.view.print_info("Adding new section with defaults.")
        self.model.config.add_section('General')
        self.model.config.set('General', 'color', 'True')
        self.model.config.set('General', 'warning', 'True')
        self.write_config_file()

    def write_config_file(self):
        """
        Writes the trove configuration file to disk.
        """
        config_file = os.path.join(self.config_dir, 'trove.conf')
        config_file_handle = open(config_file, 'w')
        self.model.config.write(config_file_handle)
        config_file_handle.close()

    def config_file_has_encrypted_file(self):
        """
        Checks if the configuration file defines an encrypted file
        """
        sections_without_general = self.model.config.sections()
        sections_without_general.remove('General')
        for section in sections_without_general:
            if self.model.config.has_option(section, 'path') and self.model.config.has_option(section, 'file'):
                encrypted_dir = self.model.config.get(section, 'path')
                encrypted_file = self.model.config.get(section, 'file')
                self.encrypted_file = os.path.join(encrypted_dir, encrypted_file)
        if self.encrypted_file != "":
            return True
        else:
            return False

    def add_bcrypt_section(self, verbose=True):
        """
        Adds a section [My Trove] to the configuration file.
        """
        if verbose:
            self.view.print_info("No section for encrypted file found.")
            self.view.print_info("Adding new section with defaults.")
        self.model.config.add_section('My Trove')
        self.model.config.set('My Trove', 'path', self.config_dir)
        self.model.config.set('My Trove', 'file', self.std_encrypted_file_name)
        self.model.config.set('My Trove', 'type', 'bcrypt')
        self.write_config_file()

    def init_passwd_file(self):
        self.encrypted_file = os.path.join(self.config_dir, self.std_encrypted_file_name)
        if not os.path.isfile(self.encrypted_file):
            self.view.print_info('Initializing empty password file')
            self.masterpwd = getpass.getpass('Please choose a strong master passphrase: ')
            self.model.write_encrypted_file(self.encrypted_file, self.masterpwd)
            self.view.print_ok(self.encrypted_file)
            self.view.print_info("Use 'add' to create new items.")

    def encrypt_dir_is_a_git_repo(self):
        """
        Check if the directory with encrypted file is a Git repository.
        """
        return_value, output = self.model.execute('cd ' + self.config_dir + '; git branch')
        if (return_value != 0):
            self.view.print_line("No Git repository found in")
            self.view.print_line(self.config_dir)
            self.view.print_line("Initializing new Git repo.")
            self.model.execute('cd ' + self.config_dir +
                'git init; git add .; git commit -m "Initial commit."')

# vim: expandtab shiftwidth=4 softtabstop=4
