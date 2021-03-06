# -*- coding: utf-8 -*-

import unittest
import StringIO
import sys
import re

from modules.view import View

class TestView(unittest.TestCase):

    def setUp(self):
        self.view = View()

    def testPrintInfoExpectsArgument(self):
        with self.assertRaises(TypeError):
            self.view.print_line()

    def testPrintInfoPrintsInput(self):
        message = "test message"
        old_stdout = sys.stdout
        sys.stdout = StringIO.StringIO()
        self.view.print_line(message)
        received_stdout = sys.stdout.getvalue().strip()
        sys.stdout = old_stdout
        self.assertEqual(received_stdout, message)

    def testPrintBoldExpectsArgument(self):
        with self.assertRaises(TypeError):
            self.view.print_bold()

    def testPrintBoldPrintsMessageInAnsiBold(self):
        message = "bold message"
        old_stdout = sys.stdout
        sys.stdout = StringIO.StringIO()
        self.view.print_bold(message)
        received_stdout = sys.stdout.getvalue().strip()
        sys.stdout = old_stdout
        bold_message = "\x1b[01m" + message + "\x1b[0m"
        self.assertEqual(received_stdout, bold_message)

    def testPrintErrorExpectsArgument(self):
        with self.assertRaises(TypeError):
            self.view.print_error()

    def testPrintErrorPrintsMessageInAnsiBold(self):
        message = "error message"
        old_stdout = sys.stdout
        sys.stdout = StringIO.StringIO()
        self.view.print_error(message)
        received_stdout = sys.stdout.getvalue()
        sys.stdout = old_stdout
        formatted_message = "\x1b[01m" + message + "\x1b[0m\n"
        self.assertEqual(received_stdout, formatted_message)

    def testPrintHelpPrintsAvailableCommandsToStdout(self):
        old_stdout = sys.stdout
        sys.stdout = StringIO.StringIO()
        self.view.print_help()
        received_stdout = sys.stdout.getvalue()
        sys.stdout = old_stdout
        regexp = re.compile('Available commands:')
        self.assertRegexpMatches(received_stdout, regexp)

# vim: expandtab shiftwidth=4 softtabstop=4
