Feature: Bubble examples
Scenario: Show the examples that are available
    Given a new working directory
    When I run "bubble examples"
        Then the command output should contain
            """
            available example: configuration
            """
        Then the command output should contain
            """
            available example: client_push
            """
        But note that "we are only checking for first and last example"
        And the command returncode is "0"

Scenario: Show an example by name
    Given a new working directory
    When I run "bubble examples -n configuration"
        Then the command output should contain
            """
            ################################################################################
            ### start of bubble example: configuration
            ################################################################################
            """
        Then the command output should contain
            """
            ################################################################################
            ### end of bubble example: configuration
            ################################################################################
            """
        And the command returncode is "0"


Scenario: Show all examples
    Given a new working directory
    When I run "bubble examples -a"
        Then the command output should contain
            """
            ### end of bubble example: configuration
            """
        Then the command output should contain
            """
            ### end of bubble example: client_push
            """
        But note that "we are only checking for first and last example"
        And the command returncode is "0"

