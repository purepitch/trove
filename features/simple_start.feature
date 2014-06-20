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

    Scenario: password file specified on command line
        Given there exists a valid password file
        And I start trove with the --file option
        And I have seen the welcome text
        When the master passphrase is entered
        Then I should see how many entries were found
        And the trove prompt should be shown

    @wip
    Scenario: empty password file
        Given there exists an empty password file
        And I have started trove
        And I have seen the welcome text
        When the master passphrase is entered
        Then I should see an error message

# vim: expandtab shiftwidth=4 softtabstop=4
