# -*- coding: utf-8 -*-

import unittest
import glob
import fileinput
import re

class TestCodingStandards(unittest.TestCase):
    """
    Tests of the DNPS project-wide coding standards
    """

    def testEncodingStringExistsInSourceCode(self):
        """
        The string "# -*- coding: utf-8 -*-" should exist in all source files
        """
        python_files = find_all_source_files()
        files_missing_encoding = []
        for filename in python_files:
            if encoding_missing_in_file(filename):
                files_missing_encoding.append(filename)

        self.assertEquals(len(files_missing_encoding), 0,
                "Files missing encoding string: " +
                str(files_missing_encoding))

    def testVimCodaExistsInSourceCode(self):
        """
        The string "# vim: expandtab shiftwidth=4 softtabstop=4" should exist
        at the bottom of all source files.
        """
        python_files = find_all_source_files()
        files_missing_coda = []
        for filename in python_files:
            if coda_missing_in_file(filename):
                files_missing_coda.append(filename)

        self.assertEquals(len(files_missing_coda), 0,
                "Files missing vim coda: " +
                str(files_missing_coda))

    def testNoTrailingWhitespace(self):
        """
        Check for trailing whitespace in source code
        """
        python_files = find_all_source_files()
        trailing_whitespace_files = []
        for filename in python_files:
            if has_trailing_whitespace(filename):
                trailing_whitespace_files.append(filename)

        self.assertEquals(len(trailing_whitespace_files), 0,
                "Files with trailing whitespace: " +
                str(trailing_whitespace_files))

def find_all_source_files():
    """
    Find and return a list of all source files
    """
    python_files = glob.glob('*.py')
    python_files += glob.glob('*/*.py')
    python_files += glob.glob('*/*/*.py')

    return python_files

def encoding_missing_in_file(filename):
    """
    Returns true if the encoding string is missing from the given file
    """
    encoding_regexp = re.compile(r'# -\*- coding: utf-8 -\*-')
    encoding_missing = True
    for line in fileinput.input(filename):
        encoding_missing = not encoding_regexp.match(line)
        if fileinput.lineno() > 2 or not encoding_missing:
            break
    fileinput.close()

    return encoding_missing

def coda_missing_in_file(filename):
    """
    Returns true if the vim coda is missing from the end of the given file
    """
    encoding_regexp = re.compile(r'# vim: expandtab shiftwidth=4 softtabstop=4')

    # slurp in the file
    fh = open(filename, 'r')
    lines = fh.readlines()
    fh.close()

    # select the last 3 lines
    lines = lines[-3:]

    coda_missing = True
    for line in lines:
        coda_missing = not encoding_regexp.match(line)

    return coda_missing

def has_trailing_whitespace(filename):
    """
    Returns true if the source code contains trailing whitespace
    """
    # slurp in the file
    fh = open(filename, 'r')
    lines = fh.readlines()
    fh.close()

    lines = [ line.rstrip('\n') for line in lines ]

    regexp = re.compile(r'\s+$')
    trailing_whitespace = [ regexp.search(line) for line in lines ]

    return any(trailing_whitespace)

if __name__ == "__main__":
    unittest.main()

# vim: expandtab shiftwidth=4 softtabstop=4
