#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
trove -  A program to store and lookup (encrypted) information
"""

import sys
import argparse

from modules.model import Model
from modules.view import View
from modules.controller import Controller

parser = argparse.ArgumentParser(
            description="store and lookup encrypted information")
parser.add_argument('--onecmd', nargs=1, help="run a single command")

model = Model()

model.program    = "trove"
model.author     = "Andreas Dorian Gerdes"
model.copyright  = "Copyright 2013--2014"
model.email      = "dorian.gerdes@gmail.com"
model.maintainer = "Andreas Dorian Gerdes"
model.status     = "Development"
model.version    = "0.1"

view = View()

args = parser.parse_args()

controller = Controller(model, view)
controller.print_welcome_text()
controller.read_db_file()
controller.check_db_for_entries()

if len(sys.argv) > 1:
    args = sys.argv[1:len(sys.argv)]
    controller.onecmd(" ".join(args))
else:
    controller.cmdloop()

# vim: expandtab shiftwidth=4 softtabstop=4
