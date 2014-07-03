Feature: entry search in interactive mode

    Scenario: search for a known entry
        Given there exists a valid password file
        And I start trove with the --file option
        And I enter the master passphrase
        And the trove prompt has been shown
        When I search for a known entry
        Then I should see an overview of the entry
        And I should be asked if I want the password shown

# vim: expandtab shiftwidth=4 softtabstop=4
