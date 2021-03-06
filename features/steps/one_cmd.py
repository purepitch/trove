# -*- coding: utf-8 -*-

from behave import given, when, then
from nose.tools import assert_true, assert_regexp_matches
import re
import pexpect

@given(u'I run trove with the --onecmd option and no argument')
def run_trove_onecmd(context):
    trove = pexpect.spawn("python trove.py --onecmd")
    context.trove = trove
    assert_true(trove.isalive())

@then(u'I should see the missing argument in onecmd error message')
def see_error_message(context):
    output = "".join(context.trove.readlines())
    error_message = "error: argument --onecmd: expected 1 argument"
    regexp = re.compile(error_message, re.MULTILINE)
    assert_regexp_matches(output, regexp)

@when(u'I run trove with "{command}"')
def run_trove_onecmd_exit(context, command):
    trove = pexpect.spawn("python trove.py %s" % command)
    context.trove = trove
    assert_true(trove.isalive())

# vim: expandtab shiftwidth=4 softtabstop=4
