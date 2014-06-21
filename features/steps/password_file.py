# -*- coding: utf-8 -*-

from behave import given, when, then
from nose.tools import assert_true, assert_false, \
        assert_regexp_matches, assert_equal, assert_not_equal
import os.path
import re
import pexpect

@given(u'there is no initial password file')
def no_initial_password_file(context):
    password_file = 'passwd.bfe'
    if os.path.exists(password_file):
        os.remove(password_file)
    assert_false(os.path.exists(password_file))

@then(u'I should see the "no password file" error message')
def see_no_password_file_error(context):
    password_file = "passwd.bfe"
    return_value = context.trove.expect(password_file)
    assert_equal(return_value, 0)

    output = context.trove.match.string.strip()
    regexp = re.compile(password_file)
    assert_regexp_matches(output, regexp)

    expected_text = 'File not found'
    return_value = context.trove.expect(expected_text)
    assert_equal(return_value, 0)

    output = context.trove.match.string.strip()
    regexp = re.compile(expected_text)
    assert_regexp_matches(output, regexp)

@given(u'there exists an empty password file')
def an_empty_password_file_exists(context):
    empty_bcrypt_file = "empty.bfe"
    context.empty_bcrypt_file = empty_bcrypt_file
    create_empty_bcrypt_file(empty_bcrypt_file)
    assert_true(os.path.exists(empty_bcrypt_file))

@given(u'I have started trove with the empty file')
def trove_started_with_empty_password_file(context):
    trove = pexpect.spawn("python trove.py --file %s" % \
            context.empty_bcrypt_file)
    context.trove = trove
    assert_true(trove.isalive())

@given(u'a default password file exists')
def default_password_file_exists(context):
    default_bfe = "passwd.bfe"
    create_valid_password_file(default_bfe)
    assert_true(os.path.exists(default_bfe))

@when(u'the master passphrase is entered')
def enter_master_passphrase(context):
    context.trove.expect('Please enter master passphrase:')
    context.trove.sendline("testtest")

    assert_true(context.trove.isalive())

@then(u'I should see an error message')
def see_error_message(context):
    return_value = context.trove.expect('No entries found after decryption.')
    assert_equal(return_value, 0)

    return_value = context.trove.expect('Perhaps the passphrase was wrong?')
    assert_equal(return_value, 0)

@then(u'trove should exit uncleanly')
def trove_exits_uncleanly(context):
    context.trove.close()
    assert_not_equal(context.trove.exitstatus, 0)

def create_empty_bcrypt_file(empty_bcrypt_file):
    if (os.path.exists(empty_bcrypt_file)):
        os.remove(empty_bcrypt_file)

    empty_file = "empty"
    assert_equal(os.system("touch %s" % empty_file), 0)
    bcrypt = pexpect.spawn("bcrypt %s" % empty_file)

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
