Feature: Bubble pull
Scenario: Given a source service in configuration
    Given a new working directory
    When I run "bubble init"
    When I run "bubble pull"
    Then the command output should contain "saved result in ["
    And the command returncode is "0"
