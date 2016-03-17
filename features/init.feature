Feature: Bubble init
Scenario: Initializing bubble
    Given a new working directory
    When I run "bubble init"
    Then a file named ".bubble" exists
    And the command output should contain "Initialised"
    And the command output should contain "please adjust your configuration file"
    And the file ".bubble" should contain:
            """
            bubble=
            """
    And the file ".bubble" should contain:
            """
            home=
            """
    And the file ".bubble" should contain:
            """
            local_init_timestamp=
            """
    And the file ".bubble" should contain:
            """
            local_creator_user=
            """
    And the file ".bubble" should contain:
            """
            local_created_in_env=
            """
    And the command returncode is "0"

Scenario: Initializing bubble with a given name
    Given a new working directory
    When I run "bubble init e7dal"
    Then a file named ".bubble" exists
    And the command output should contain "Initialised"
    And the command output should contain "please adjust your configuration file"
    And the file ".bubble" should contain:
            """
            name=(((e7dal)))
            """
    And the command returncode is "0"


Scenario: Initializing bubble, bubble already present
  Given a file named ".bubble" with:
            """
            bubble:0.1.1
            """
    When I run "bubble init"
    Then the command output should contain "already"
    And a file named ".bubble" exists
    And the command returncode is "0"
