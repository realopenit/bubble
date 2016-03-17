Feature: Bubble functions
Scenario: Show the functions that are available for the transformer rules
    Given a new working directory
    When I run "bubble init"
    Then the command output should contain "Created an example rule_functions"
    Then the command output should contain "/custom_rule_functions.py"
    And the command returncode is "0"
    When I run "bubble functions"
    Then the command output should contain "fun: replace_hello_with_goodbye"
    And the command returncode is "0"
