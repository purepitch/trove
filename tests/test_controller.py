# -*- coding: utf-8 -*-

import unittest
import re
import StringIO
import sys

from modules import Controller, Model, View

class TestController(unittest.TestCase):

    def setUp(self):
        self.model = Model()
        self.view = View()
        self.controller = Controller(self.model, self.view)

    def testDefaultExpectsArgument(self):
        with self.assertRaises(TypeError):
            self.controller.default()

    def testDoTestColorsExpectsArgument(self):
        with self.assertRaises(TypeError):
            self.controller.do_testcolors()

    def testDoExitExpectsArgument(self):
        with self.assertRaises(TypeError):
            self.controller.do_exit()

    def testDoExitReturnsTrue(self):
        return_value = self.controller.do_exit("")
        self.assertTrue(return_value)

    def testDoQuitExpectsArgument(self):
        with self.assertRaises(TypeError):
            self.controller.do_quit()

    def testDoQuitReturnsTrue(self):
        return_value = self.controller.do_quit("")
        self.assertTrue(return_value)

    def testDoEofExpectsArgument(self):
        with self.assertRaises(TypeError):
            self.controller.do_EOF()

    def testDoEofReturnsTrue(self):
        return_value = self.controller.do_EOF("")
        self.assertTrue(return_value)

    def testDoClearExpectsArgument(self):
        with self.assertRaises(TypeError):
            self.controller.do_clear()

    def testDoHelpExpectsArgument(self):
        with self.assertRaises(TypeError):
            self.controller.do_help()

class TestControllerPrintedOutput(unittest.TestCase):

    def setUp(self):
        self.model = Model()
        self.view = View()
        self.controller = Controller(self.model, self.view)
        self.old_stdout = sys.stdout
        sys.stdout = StringIO.StringIO()

    def testDefaultPrintsExpectedErrorMessage(self):
        error_message = "error message"
        self.controller.default(error_message)
        received_stdout = sys.stdout.getvalue().strip()
        expected_message = 'Unknown syntax: ' + error_message
        regexp = re.compile(expected_message)
        self.assertRegexpMatches(received_stdout, regexp)

    def testDoTestColorsPrintsTestText(self):
        self.controller.do_testcolors("")
        received_stdout = sys.stdout.getvalue().strip()
        regexp = re.compile('Test.*reset')
        self.assertRegexpMatches(received_stdout, regexp)

    def testDoExitPrintsEmptyLine(self):
        self.controller.do_exit("")
        received_stdout = sys.stdout.getvalue()
        self.assertEqual(received_stdout, "\n")

    def testDoQuitPrintsEmptyLine(self):
        self.controller.do_quit("")
        received_stdout = sys.stdout.getvalue()
        self.assertEqual(received_stdout, "\n")

    def testDoEofPrintsEndOfFile(self):
        self.controller.do_EOF("")
        received_stdout = sys.stdout.getvalue()
        self.assertEqual(received_stdout, "\n\n")

    def testDoHelpPrintsHelpTextToStdout(self):
        self.controller.do_help("")
        received_stdout = sys.stdout.getvalue()
        regexp = re.compile('Available commands:')
        self.assertRegexpMatches(received_stdout, regexp)

    def tearDown(self):
        sys.stdout = self.old_stdout

# vim: expandtab shiftwidth=4 softtabstop=4
