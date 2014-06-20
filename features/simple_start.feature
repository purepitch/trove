Feature: simple program startup
    As a user of the program
    When I start the program
    I should obtain confirmation that it has started

    Scenario: see welcome screen
        Given I have started trove
        Then I should see the welcome text

    Scenario: no password file
        Given I have started trove
        And I have seen the welcome text
        And there is no initial password file
        Then I should see the "no password file" error message
        And trove should exit uncleanly

# vim: expandtab shiftwidth=4 softtabstop=4
