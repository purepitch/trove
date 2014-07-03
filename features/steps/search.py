# -*- coding: utf-8 -*-

from behave import when, then
from nose.tools import assert_true, assert_false, assert_equal

@when(u'I search for a known entry')
def known_entry_search(context):
    context.trove.sendline("search smurf")
    assert_true(context.trove.isalive())
    assert_false(context.trove.eof())

@then(u'I should see an overview of the entry')
def show_entry_overview(context):
    expected_text = "Entry name:   Papa Smurf (Root)"
    context.trove.expect_exact(expected_text)
    assert_equal(context.trove.match.strip(), expected_text)

    expected_text = "User:        root"
    context.trove.expect_exact(expected_text)
    assert_equal(context.trove.match.strip(), expected_text)

    expected_text = \
            "Help:        Mary had a little lamb, its fleece was white as snow"
    context.trove.expect_exact(expected_text)
    assert_equal(context.trove.match.strip(), expected_text)

    expected_text = "Description: Root access to main smurf computer"
    context.trove.expect_exact(expected_text)
    assert_equal(context.trove.match.strip(), expected_text)

@then(u'I should be asked if I want the password shown')
def ask_to_show_password(context):
    expected_text = "Show password? (y/N)"
    context.trove.expect_exact(expected_text)
    assert_equal(context.trove.match.strip(), expected_text)

# vim: expandtab shiftwidth=4 softtabstop=4
