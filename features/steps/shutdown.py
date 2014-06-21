# -*- coding: utf-8 -*-

from behave import then
from nose.tools import assert_false, assert_equal, assert_not_equal
import pexpect

@then(u'trove should exit cleanly')
def trove_exits_cleanly(context):
    assert_equal(context.trove.expect(pexpect.EOF), 0)
    assert_false(context.trove.isalive())
    context.trove.close()
    assert_equal(context.trove.exitstatus, 0)

@then(u'trove should exit uncleanly')
def trove_exits_uncleanly(context):
    context.trove.close()
    assert_not_equal(context.trove.exitstatus, 0)

# vim: expandtab shiftwidth=4 softtabstop=4
