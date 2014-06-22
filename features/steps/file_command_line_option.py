# -*- coding: utf-8 -*-

from behave import given, then
from nose.tools import assert_true, assert_regexp_matches
import pexpect
import re

@given(u'I start trove with the --file option')
def trove_starts_with_file_option(context):
    trove = pexpect.spawn("python trove.py --file %s" % \
            context.password_bfe)
    context.trove = trove
    assert_true(trove.isalive())

@then(u'I should see how many entries were found')
def see_number_of_entries_found(context):
    expected_text = 'Found total number of \d+ entries.'
    context.trove.expect(expected_text)
    output = context.trove.match.string.strip()
    regexp = re.compile(expected_text)
    assert_regexp_matches(output, regexp)

@then(u'the trove prompt should be shown')
def see_trove_prompt(context):
    expected_text = '(trove)'
    context.trove.expect(expected_text)
    output = context.trove.match.string.strip()
    regexp = re.compile(expected_text)
    assert_regexp_matches(output, regexp)

@given(u'trove is started with an empty --file option')
def trove_starts_with_empty_file_option(context):
    trove = pexpect.spawn("python trove.py --file")
    context.trove = trove
    assert_true(trove.isalive())

@then(u'I should see the "--file missing argument" error message')
def see_file_missing_argument_error_message(context):
    expected_text = 'error: argument --file: expected 1 argument'
    context.trove.expect(expected_text)
    output = context.trove.match.string.strip()
    regexp = re.compile(expected_text)
    assert_regexp_matches(output, regexp)

# vim: expandtab shiftwidth=4 softtabstop=4
