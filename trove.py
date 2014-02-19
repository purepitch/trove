#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
trove -  A program to store and lookup (encrypted) information
"""

import sys

from modules.model import Model
from modules.view import View
from modules.controller import Controller

model = Model()
view = View()
controller = Controller()

model.program    = "trove"
model.author     = "Andreas Dorian Gerdes"
model.copyright  = "Copyright 2013"
model.email      = "dorian.gerdes@gmail.com"
model.maintainer = "Andreas Dorian Gerdes"
model.status     = "Development"
model.version    = "0.1"

controller.initialize(model, view)

if len(sys.argv) > 1:
    args = sys.argv[1:len(sys.argv)]
    controller.onecmd(" ".join(args))
else:
    controller.cmdloop()

# vim: expandtab shiftwidth=4 softtabstop=4
