# -*- coding: utf-8 -*-

import unittest
import re

from modules import Model

class TestModel(unittest.TestCase):

    def setUp(self):
        self.model = Model()

    def testGetConfigExpectsConfigFilename(self):
        with self.assertRaises(TypeError):
            self.model.get_config()

    @unittest.skip("should an error be raised with missing config file?")
    def testGetConfigRaisesErrorOnMissingConfigFile(self):
        with self.assertRaises(IOError):
            self.model.get_config(file="missing.conf")

# vim: expandtab shiftwidth=4 softtabstop=4
