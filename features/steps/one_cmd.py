# -*- coding: utf-8 -*-

from behave import given, then
from nose.tools import assert_true, assert_regexp_matches
import re
import pexpect

@given(u'I run trove with the --onecmd option and no argument')
def run_trove_onecmd(context):
    process = pexpect.spawn("python trove.py --onecmd")
    context.process = process
    assert_true(process.isalive())

@then(u'I should see an error message')
def see_error_message(context):
    output = "".join(context.process.readlines())
    error_message = "error: argument --onecmd: expected 1 argument"
    regexp = re.compile(error_message, re.MULTILINE)
    assert_regexp_matches(output, regexp)

# vim: expandtab shiftwidth=4 softtabstop=4
