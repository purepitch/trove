Feature: run one command from command line
    As a trove user
    When I run trove with single commands
    I should see the output I expect

    Scenario: "--onecmd" without arguments
        Given I run trove with the --onecmd option and no argument
        Then I should see the missing argument in onecmd error message


# vim: expandtab shiftwidth=4 softtabstop=4
