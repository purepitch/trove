# -*- coding: utf-8 -*-

import unittest

from modules import Model

class TestModel(unittest.TestCase):

    def setUp(self):
        self.model = Model()

    def testGetConfigExpectsConfigFilename(self):
        with self.assertRaises(TypeError):
            self.model.get_config()

# vim: expandtab shiftwidth=4 softtabstop=4
