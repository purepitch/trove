# -*- coding: utf-8 -*-

from behave import given, when, then
from nose.tools import assert_true, assert_false,\
        assert_equal, assert_regexp_matches
import re
import pexpect
import os

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

@given(u'a default password file exists')
def default_password_file_exists(context):
    default_bfe = "passwd.bfe"
    create_valid_password_file(default_bfe)
    assert_true(os.path.exists(default_bfe))

@when(u'I run trove with "{command}"')
def run_trove_onecmd_exit(context, command):
    trove = pexpect.spawn("python trove.py %s" % command)
    context.trove = trove
    assert_true(trove.isalive())

@then(u'trove should exit cleanly')
def trove_exits_cleanly(context):
    assert_equal(context.trove.expect(pexpect.EOF), 0)
    assert_false(context.trove.isalive())
    context.trove.close()
    assert_equal(context.trove.exitstatus, 0)

def create_valid_password_file(password_bfe):
    if os.path.exists(password_bfe):
        os.remove(password_bfe)

    password_file = password_bfe.split('.')[0]
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
