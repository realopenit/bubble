Feature: Bubble export escapes
Scenario: running export key string contains arrows ">>>"
  Given a file named ".bubble" with:
            """
            bubble=0.1.1
            """
    And a file named "./config/config.yaml" with:
            """
            ---
            CFG:
                BUBBLE:
                    DEBUG: True
                    VERBOSE: True
                    STORAGE_TYPE: json
                DEV:
                    SOURCE:    #pull
                        CLIENT: dummy
                        URL: http://localhost:8001
                    TRANSFORM:
                        RULES: config/rules.bubble
                    TARGET:    #push
                        CLIENT: dummy
                        URL: http://localhost:8002
            ...
            """

    And a file named "./remember/pushed_DEV.json" with:
            """
            {"data": [{"res":200,"input":{"A>>>B":"a","B>>>C":"b"}}
                     ]
            }
            """
  When I run "bubble export   -r pushed -f tab -c input.A___bts_escarrows_B,input.B___bts_escarrows_C -kvp"
    Then the command output should contain:
    """
    BUBBLE_IDX|input.A___bts_escarrows_B|input.B___bts_escarrows_C
    ----------|-------------------------|-------------------------
    0         |a                        |b
    """
    And the command returncode is "0"
  Scenario: running export key string contains arrows ">>>" select alias
  Given a file named ".bubble" with:
            """
            bubble=0.1.1
            """
    And a file named "./config/config.yaml" with:
            """
            ---
            CFG:
                BUBBLE:
                    DEBUG: True
                    VERBOSE: True
                    STORAGE_TYPE: json
                DEV:
                    SOURCE:    #pull
                        CLIENT: dummy
                        URL: http://localhost:8001
                    TRANSFORM:
                        RULES: config/rules.bubble
                    TARGET:    #push
                        CLIENT: dummy
                        URL: http://localhost:8002
            ...
            """

    And a file named "./remember/pushed_DEV.json" with:
            """
            {"data": [{"res":200,"input":{"A>>>B":"a","B>>>C":"b"}}
                     ]
            }
            """
  When I run "bubble export   -r pushed -f tab -c input.A___bts_escarrows_B:iAB,input.B___bts_escarrows_C:iBC -kvp"
    Then the command output should contain:
    """
    BUBBLE_IDX|iAB|iBC
    ----------|---|---
    0         |a  |b
    """
    And the command returncode is "0"

