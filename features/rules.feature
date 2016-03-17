Feature: Bubble rules
Scenario: Show the rules that are available for the transformer rules
    Given a new working directory
    When I run "bubble init"
    Then the command output should contain "Created an example rules"
    Then the command output should contain "/config/rules.bubble"
    And the command returncode is "0"
    When I run "bubble rules"
    Then the command output should contain "rule: <Rule 19 >>> in >>> <RuleFunction"
    Then the command output should contain " replace_hello_with_goodbye <function replace_hello_with_goodbye at"
    Then the command output should contain " > custom> >>> out >>> None >>> None >>>"
    But note that "checks are for a single line of output,  nature of functions and their hex id's"
    And the command returncode is "0"
