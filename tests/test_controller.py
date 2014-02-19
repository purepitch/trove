# -*- coding: utf-8 -*-

import unittest
import re
import StringIO
import sys

from modules import Controller, Model, View

class TestController(unittest.TestCase):

    def setUp(self):
        self.controller = Controller()
        self.model = Model()
        self.view = View()

    def testHandleExpectsArgument(self):
        with self.assertRaises(TypeError):
            self.controller.handle()

    def testHandlePrintsWelcomeMessage(self):
        old_stdout = sys.stdout
        sys.stdout = StringIO.StringIO()
        self.controller.handle(self.model, self.view)
        received_stdout = sys.stdout.getvalue().strip()
        sys.stdout = old_stdout
        welcome_message = "This is trove"
        regexp = re.compile(welcome_message)
        self.assertRegexpMatches(received_stdout, regexp)

    def testDefaultExpectsArgument(self):
        with self.assertRaises(TypeError):
            self.controller.default()

    def testDefaultPrintsExpectedErrorMessage(self):
        self.controller.handle(self.model, self.view)
        error_message = "error message"
        old_stdout = sys.stdout
        sys.stdout = StringIO.StringIO()
        self.controller.default(error_message)
        received_stdout = sys.stdout.getvalue().strip()
        sys.stdout = old_stdout
        expected_message = 'Unknown syntax: ' + error_message
        regexp = re.compile(expected_message)
        self.assertRegexpMatches(received_stdout, regexp)

    def testDoTestColorsExpectsArgument(self):
        self.controller.handle(self.model, self.view)
        with self.assertRaises(TypeError):
            self.controller.do_testcolors()

    def testDoTestColorsPrintsTestText(self):
        self.controller.handle(self.model, self.view)
        old_stdout = sys.stdout
        sys.stdout = StringIO.StringIO()
        self.controller.do_testcolors("")
        received_stdout = sys.stdout.getvalue().strip()
        sys.stdout = old_stdout
        regexp = re.compile('Test.*reset')
        self.assertRegexpMatches(received_stdout, regexp)

    def testDoExitExpectsArgument(self):
        self.controller.handle(self.model, self.view)
        with self.assertRaises(TypeError):
            self.controller.do_exit()

    def testDoExitPrintsEmptyLine(self):
        self.controller.handle(self.model, self.view)
        old_stdout = sys.stdout
        sys.stdout = StringIO.StringIO()
        self.controller.do_exit("")
        received_stdout = sys.stdout.getvalue()
        sys.stdout = old_stdout
        self.assertEqual(received_stdout, "\n")

    def testDoExitReturnsTrue(self):
        self.controller.handle(self.model, self.view)
        return_value = self.controller.do_exit("")
        self.assertTrue(return_value)
    
    def testDoQuitExpectsArgument(self):
        self.controller.handle(self.model, self.view)
        with self.assertRaises(TypeError):
            self.controller.do_quit()

    def testDoQuitPrintsEmptyLine(self):
        self.controller.handle(self.model, self.view)
        old_stdout = sys.stdout
        sys.stdout = StringIO.StringIO()
        self.controller.do_quit("")
        received_stdout = sys.stdout.getvalue()
        sys.stdout = old_stdout
        self.assertEqual(received_stdout, "\n")

    def testDoQuitReturnsTrue(self):
        self.controller.handle(self.model, self.view)
        return_value = self.controller.do_quit("")
        self.assertTrue(return_value)

    def testDoEofExpectsArgument(self):
        self.controller.handle(self.model, self.view)
        with self.assertRaises(TypeError):
            self.controller.do_EOF()

    def testDoEofPrintsEndOfFile(self):
        self.controller.handle(self.model, self.view)
        old_stdout = sys.stdout
        sys.stdout = StringIO.StringIO()
        self.controller.do_EOF("")
        received_stdout = sys.stdout.getvalue()
        sys.stdout = old_stdout
        self.assertEqual(received_stdout, "\n\n")

    def testDoEofReturnsTrue(self):
        self.controller.handle(self.model, self.view)
        return_value = self.controller.do_EOF("")
        self.assertTrue(return_value)

    def testDoClearExpectsArgument(self):
        self.controller.handle(self.model, self.view)
        with self.assertRaises(TypeError):
            self.controller.do_clear()

    def testDoHelpExpectsArgument(self):
        self.controller.handle(self.model, self.view)
        with self.assertRaises(TypeError):
            self.controller.do_help()

    def testDoHelpPrintsHelpTextToStdout(self):
        self.controller.handle(self.model, self.view)
        old_stdout = sys.stdout
        sys.stdout = StringIO.StringIO()
        self.controller.do_help("")
        received_stdout = sys.stdout.getvalue()
        sys.stdout = old_stdout
        regexp = re.compile('Available commands:')
        self.assertRegexpMatches(received_stdout, regexp)

 # vim: expandtab shiftwidth=4 softtabstop=4
