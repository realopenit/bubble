Feature: Bubble usage
Scenario: Starting bubble
    Given a new working directory
    When I run "bubble"
    Then the command output should contain "Usage"
    And  the command returncode is "0"
Scenario: Starting bubble help
    Given a new working directory
    When I run "bubble --help"
    Then the command output should contain "Usage"
    And  the command returncode is "0"
Scenario: Starting bubble pull
    Given a new working directory
    When I run "bubble pull"
    Then the command output should contain "will not pull"
    And  the command returncode is "1"
Scenario: Starting bubble transform
    Given a new working directory
    When I run "bubble transform"
    Then the command output should contain "will not transform"
    And  the command returncode is "1"
Scenario: Starting bubble push
    Given a new working directory
    When I run "bubble push"
    Then the command output should contain "will not push"
    And  the command returncode is "1"
Scenario: Starting bubble pump
    Given a new working directory
    When I run "bubble pump"
    Then the command output should contain "will not pull"
    And  the command returncode is "1"
Scenario: Starting bubble stats
    Given a new working directory
    When I run "bubble stats"
    Then the command output should contain "will not search stats"
    And  the command returncode is "1"
Scenario: Starting bubble stats --monitor nagios
    Given a new working directory
    When I run "bubble stats --monitor nagios"
    Then the command output should contain "will not search stats"
    And  the command returncode is "3"
Scenario: Starting bubble listen
    Given a new working directory
    When I run "bubble listen"
    Then the command output should contain "will not listen"
    And  the command returncode is "1"
Scenario: Starting bubble export
    Given a new working directory
    When I run "bubble export"
    Then the command output should contain "will not export"
    And  the command returncode is "1"
Scenario: Starting bubble rules
    Given a new working directory
    When I run "bubble rules"
    Then the command output should contain "will not show any transformer rules"
    And  the command returncode is "1"
Scenario: Starting bubble functions
    Given a new working directory
    When I run "bubble functions"
    Then the command output should contain "will not show any transformer functions"
    And  the command returncode is "1"
Scenario: Starting bubble web
    Given a new working directory
    When I run "bubble web"
    Then the command output should contain "will not listen"
    And  the command returncode is "1"

