# -*- coding: utf-8 -*-

from behave import given, then
from nose.tools import assert_false, assert_regexp_matches, assert_not_equal
import os.path
import re

@given(u'there is no initial password file')
def no_initial_password_file(context):
    assert_false(os.path.exists('passwd.bfe'))

@then(u'I should see the "no password file" error message')
def see_no_password_file_error(context):
    output = "".join(context.process.readlines())
    regexp = re.compile("passwd.bfe", re.MULTILINE)
    assert_regexp_matches(output, regexp)

    regexp = re.compile("File not found", re.MULTILINE)
    assert_regexp_matches(output, regexp)

@then(u'the program should exit uncleanly')
def program_exits_uncleanly(context):
    context.process.close()
    assert_not_equal(context.process.exitstatus, 0)

# vim: expandtab shiftwidth=4 softtabstop=4
