Feature: Bubble export escapes
Scenario: running export key string contains ": or , or . "
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
            {"data": [{"res":200,"input":{"A.B":"a","B.C":"b"}},
                      {"res":200,"input":{"A:B":"a","B:C":"b"}},
                      {"res":200,"input":{"A,B":"a","B,C":"b"}}
                     ]
            }
            """
  When I run "bubble export   -r pushed -f tab -c input.A___bts_escsep_B,input.B___bts_escsep_C -kvp"
    Then the command output should contain:
    """
    BUBBLE_IDX|input.A___bts_escsep_B|input.B___bts_escsep_C
    ----------|----------------------|----------------------
    0         |a                     |b
    1         |None                  |None
    2         |None                  |None
    """
    And the command returncode is "0"
  When I run "bubble export   -r pushed -f tab -c input.A___bts_esccolon_B,input.B___bts_esccolon_C -kvp"
    Then the command output should contain:
    """
    BUBBLE_IDX|input.A___bts_esccolon_B|input.B___bts_esccolon_C
    ----------|------------------------|------------------------
    0         |None                    |None
    1         |a                       |b
    2         |None                    |None
    """
    And the command returncode is "0"
  When I run "bubble export   -r pushed -f tab -c input.A___bts_esccomma_B,input.B___bts_esccomma_C -kvp"
    Then the command output should contain:
    """
    BUBBLE_IDX|input.A___bts_esccomma_B|input.B___bts_esccomma_C
    ----------|------------------------|------------------------
    0         |None                    |None
    1         |None                    |None
    2         |a                       |b
    """
    And the command returncode is "0"

Scenario: running export key string contains ": or , or . , all escapes in one key"
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
            {"data": [{"res":200,"input":{"A.B:C,D":"all escapes in one key"}}
                     ]
            }
            """
  When I run "bubble export   -r pushed -f tab -c input.A___bts_escsep_B___bts_esccolon_C___bts_esccomma_D -kvp"
    Then the command output should contain:
    """
    BUBBLE_IDX|input.A___bts_escsep_B___bts_esccolon_C___bts_esccomma_D
    ----------|--------------------------------------------------------
    0         |all escapes in one key
    """
    And the command returncode is "0"
 Scenario: running export key string contains ": or , or . , complex"
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
            {"data": [{"res":200, "input": {"A.B:C,D": {"nest":["li1",
                                                                "li2",
                                                                "li3",
                                                                {"li4.list_item":"all escapes in one key in list item"},
                                                                "li5"]
                                                                }
                                           }
                      }
                     ]
            }
            """
   When I run "bubble export   -r pushed -f tab -c input.A___bts_escsep_B___bts_esccolon_C___bts_esccomma_D.nest.4.li4___bts_escsep_list_item -kvp"
    Then the command output should contain:
    """
    BUBBLE_IDX|input.A___bts_escsep_B___bts_esccolon_C___bts_esccomma_D.nest.4.li4___bts_escsep_list_item
    ----------|------------------------------------------------------------------------------------------
    0         |all escapes in one key in list item
    """
    And the command returncode is "0"