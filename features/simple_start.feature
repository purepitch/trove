Feature: simple program startup
    As a user of the program
    When I start the program
    I should obtain confirmation that it has started

    Scenario: see welcome screen
        Given I have started trove
        Then I should see the welcome text

# vim: expandtab shiftwidth=4 softtabstop=4
