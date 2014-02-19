#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
trove -  A program to store and lookup (encrypted) information
"""

import sys

from modules.model import Model
from modules.view import View
from modules.controller import Controller

m = Model()
v = View()
c = Controller()

m.program    = "trove"
m.author     = "Andreas Dorian Gerdes"
m.email      = "dorian.gerdes@gmail.com"
m.status     = "Development"
m.version    = "0.1"

c.initialize(m, v)

if len(sys.argv) > 1:
    args = sys.argv[1:len(sys.argv)]
    c.onecmd(" ".join(args))
else:
    c.cmdloop()

# vim: expandtab shiftwidth=4 softtabstop=4
