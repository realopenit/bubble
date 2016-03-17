Feature: Bubble stats
Scenario: No errors should print OK
    Given a new working directory
    And a file named "./remember/stats_DEV.json" with:
            """
            {"data":[{
              "pulled_stat_total_count": 1000,
              "pulled_stat_error_count": 0,
              "transformed_stat_total_count": 1000,
              "transformed_stat_error_count": 0,
              "pushed_stat_total_count": 1000,
              "pushed_stat_error_count": 0
              }]}
            """
    When I run "bubble init"
  When I run "bubble stats --monitor nagios --full"
    Then the command output should contain "Ok - pull: 1000 0 transform: 1000  0 push: 1000 0"
    And the command returncode is "0"

Scenario: No Errors and different totals should print Warning
    Given a new working directory
    And a file named "./remember/stats_DEV.json" with:
            """
            {"data":[{
            "pulled_stat_total_count": 1000,
            "pulled_stat_error_count": 0,
            "transformed_stat_total_count": 800,
            "transformed_stat_error_count": 0,
            "pushed_stat_total_count": 1200,
            "pushed_stat_error_count": 0
            }]}
            """
    When I run "bubble init"
    When I run "bubble stats --monitor nagios"
    Then the command output should contain "Warning - pull: 1000 0 transform: 800  0 push: 1200 0"
    And the command returncode is "1"

Scenario: Errors should print Critical
    Given a new working directory
    And a file named "./remember/stats_DEV.json" with:
            """
            {"data":[{
            "pulled_stat_total_count": 1000,
            "pulled_stat_error_count": 10,
            "transformed_stat_total_count": 1000,
            "transformed_stat_error_count": 10,
            "pushed_stat_total_count": 1000,
            "pushed_stat_error_count": 10
            }]}
            """
    When I run "bubble init"
    When I run "bubble stats --monitor nagios"
    Then the command output should contain "Critical - pull: 1000 10 transform: 1000  10 push: 1000 10"
    And the command returncode is "2"

Scenario: No stats should return Unknown
    Given a new working directory
    And a file named "./remember/stats_DEV.json" with:
            """
            {"data":[]}
            """
    When I run "bubble init"
    When I run "bubble stats --monitor nagios"
    Then the command output should contain "Unknown"
    And the command returncode is "3"
