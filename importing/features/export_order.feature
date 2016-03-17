Feature: Bubble export  with single column ordering
Scenario: running export with order  key:+ (asc) or key:- (desc), or key (default:asc)
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
            {"data": [{"res":200,"input":{"a":"A","b":"B","c":"C"}},
                      {"res":200,"input":{"a":"AA","b":"E","c":"one"}},
                      {"res":200,"input":{"a":"Z","b":"E","c":"Z"}},
                      {"res":200,"input":{"a":"AA","b":"E","c":"two"}}
                     ]
            }
            """
    When I run "bubble export   --stepresult pushed --formattype tab -p -O BUBBLE_IDX"
    Then the command output should contain:
    """
    BUBBLE_IDX
    ----------
    0
    1
    2
    3
    """
    And the command returncode is "0"
    When I run "bubble export   --stepresult pushed --formattype tab -p -O BUBBLE_IDX:+"
    Then the command output should contain:
    """
    BUBBLE_IDX
    ----------
    0
    1
    2
    3
    """
    And the command returncode is "0"
    When I run "bubble export   --stepresult pushed --formattype tab -p -O BUBBLE_IDX:-"
    Then the command output should contain:
    """
    BUBBLE_IDX
    ----------
    3
    2
    1
    0
    """
    And the command returncode is "0"
