# -*- coding: utf-8 -*-

from behave import given, then
from nose.tools import assert_true, assert_false, \
        assert_equal, assert_regexp_matches
import pexpect
import os
import re

@given(u'there exists a valid password file')
def valid_password_file_exists(context):
    password_bfe = "passwords.bfe"
    context.password_bfe = password_bfe
    create_valid_password_file(password_bfe)
    assert_true(os.path.exists(password_bfe))

@given(u'I start trove with the --file option')
def trove_starts_with_file_option(context):
    process = pexpect.spawn("python trove.py --file %s" % \
            context.password_bfe)
    context.process = process
    assert_true(process.isalive())

@then(u'I should see how many entries were found')
def see_number_of_entries_found(context):
    expected_text = 'Found total number of \d+ entries.'
    context.process.expect(expected_text)
    output = context.process.match.string.strip()
    regexp = re.compile(expected_text)
    assert_regexp_matches(output, regexp)

@then(u'the trove prompt should be shown')
def see_trove_prompt(context):
    expected_text = '\(trove\)'
    context.process.expect(expected_text)
    output = context.process.match.string.strip()
    regexp = re.compile(expected_text)
    assert_regexp_matches(output, regexp)

@given(u'trove is started with an empty --file option')
def trove_starts_with_empty_file_option(context):
    process = pexpect.spawn("python trove.py --file")
    context.process = process
    assert_true(process.isalive())

@then(u'I should see the "--file missing argument" error message')
def see_file_missing_argument_error_message(context):
    expected_text = 'error: argument --file: expected 1 argument'
    context.process.expect(expected_text)
    output = context.process.match.string.strip()
    regexp = re.compile(expected_text)
    assert_regexp_matches(output, regexp)

def create_valid_password_file(password_bfe):
    if os.path.exists(password_bfe):
        os.remove(password_bfe)

    password_file = "passwords"
    password_data = """\
[ Papa Smurf (Root) ]
connection_name: papa.smurf.smurf
user: root
password: Mh4_l,ifw2as
help: Mary had a little lamb, its fleece was white as snow
description: Root access to main smurf computer
"""
    password_fh = open(password_file, "w")
    password_fh.write(password_data)
    password_fh.close()

    bcrypt = pexpect.spawn("bcrypt %s" % password_file)

    assert_true(bcrypt.isalive())

    assert_equal(bcrypt.expect('Encryption key:'), 0)
    assert_equal(bcrypt.match.string, 'Encryption key:')
    assert_equal(bcrypt.sendline("testtest"), 9)
    assert_equal(bcrypt.expect('Again:'), 0)
    assert_equal(bcrypt.match.string.strip(), 'Again:')
    assert_equal(bcrypt.sendline("testtest"), 9)
    bcrypt.wait()
    bcrypt.close()

    assert_false(bcrypt.isalive())
    assert_equal(bcrypt.exitstatus, 0)

# vim: expandtab shiftwidth=4 softtabstop=4
