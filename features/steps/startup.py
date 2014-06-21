# -*- coding: utf-8 -*-

from behave import given, then
from nose.tools import assert_true, assert_equal
import pexpect

@given(u'I have started trove')
def i_have_started_trove(context):
    trove = pexpect.spawn("python -u trove.py")
    context.trove = trove
    assert_true(trove.isalive())

@then(u'I should see the welcome text')
@given(u'I have seen the welcome text')
def i_see_welcome_text(context):
    welcome_text = """\
This is trove 0.1
Use Ctrl+D to exit, type 'help' or '?' for help.
"""
    welcome_text = welcome_text.split('\n')

    output = context.trove.readline()
    assert_equal(output.strip(), welcome_text[0].strip())

    output = context.trove.readline()
    assert_equal(output.strip(), welcome_text[1].strip())

@given(u'I have started trove with the empty file')
def trove_started_with_empty_password_file(context):
    trove = pexpect.spawn("python trove.py --file %s" % \
            context.empty_bcrypt_file)
    context.trove = trove
    assert_true(trove.isalive())

# vim: expandtab shiftwidth=4 softtabstop=4
