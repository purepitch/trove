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

    def testDateReturnsCorrectFormat(self):
        timestamp = self.model.get_date()
        regexp = re.compile(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}')
        self.assertRegexpMatches(timestamp, regexp)

    def testExecuteExpectsCommandArgument(self):
        with self.assertRaises(TypeError):
            self.model.execute()

    def testExecuteReturnsString(self):
        output = self.model.execute('ls')
        self.assertTrue(isinstance(output, str))

# vim: expandtab shiftwidth=4 softtabstop=4
