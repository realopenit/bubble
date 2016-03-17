Feature: Bubble pump no transform
Scenario: Given a target and no transform in configuration
    Given a new working directory
    When I run "bubble init"
    Then the command output should contain "Bubble initialized"
    Given a file named "./config/config.yaml" with:
            """
            ---
            CFG:
                BUBBLE:
                    DEBUG: True
                    VERBOSE: True
                    STORAGE_TYPE: json
                DEV:
                    SOURCE:    #pull
                        CLIENT: ./mysrcclient.py
                    TARGET:    #push
                        CLIENT: ./mytgtclient.py
            ...
            """
    When I run "bubble pump"
    Then the command output should contain "Pushing"
    Then the command output should contain "saved result in ["
    And the command returncode is "0"
    
