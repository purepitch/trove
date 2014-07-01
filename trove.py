#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
trove -  A program to store and lookup (encrypted) information
"""

import sys

from modules.model import Model
from modules.view import View
from modules.controller import Controller

# Initialize the Model 
model = Model()
model.program_name = "trove"
model.version = "0.1"

# Say hello
view = View()
controller = Controller(model, view)
controller.print_welcome_text()
controller.read_config()
if not controller.encrypted_file ==  "":
    controller.read_db_file()
    controller.check_db_for_entries()

if len(sys.argv) > 1:
    args = sys.argv[1:len(sys.argv)]
    controller.onecmd(" ".join(args))
else:
    controller.cmdloop()

# vim: expandtab shiftwidth=4 softtabstop=4
