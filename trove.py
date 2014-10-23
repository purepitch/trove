#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
trove -  A program to store and lookup (encrypted) information
"""

import argparse
from modules.model import Model
from modules.view import View
from modules.controller import Controller

parser = argparse.ArgumentParser(
            description="store and lookup encrypted information")
parser.add_argument('--onecmd', nargs=1, help="run a single command")
parser.add_argument('--file', nargs=1, help="name of encrypted input file")

# Initialize Model
model = Model()
model.program_name = "trove"
model.version = "0.1"

# Inititalize View
view = View()

# Parse command line arguments
args = parser.parse_args()

# Initialize Controller
controller = Controller(model, view)

# Say hello
controller.print_hello_message()

# Run startup checks
controller.run_startup_checks()

if args.file is not None:
    controller.encrypted_file = args.file[0]

if not controller.config_file_has_encrypted_file():
    controller.add_bcrypt_section()
    controller.init_passwd_file()
else:
    controller.read_encrypted_file()
    controller.check_db_for_entries()

# Print info line
controller.print_info_message()

if args.onecmd is not None:
    controller.onecmd(args.onecmd[0])
else:
    controller.cmdloop()

# vim: expandtab shiftwidth=4 softtabstop=4
