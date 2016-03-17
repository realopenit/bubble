Feature: Bubble export selection with where option
Scenario: running export with where string key:val
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
    When I run "bubble export   --stepresult pushed --formattype tab --select 'input.a:a,input.c:c' --where 'input.a:AA'"
    Then the command output should contain:
    """
    a |c
    --|---
    AA|one
    AA|two
    """
    And the command returncode is "0"

Scenario: running export with where string key:val,key:val
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
            {"data":    [{"res":200,"input":{"a":"A","b":"B","c":"C"}},
                         {"res":200,"input":{"a":"AA","b":"E","c":"one"}},
                         {"res":200,"input":{"a":"Z","b":"E","c":"Z"}},
                         {"res":200,"input":{"a":"Z","b":"A Big","c":"A Circle"}},
                         {"res":200,"input":{"a":"AA","b":"E","c":"two"}}
                        ]
            }
            """
    When I run "bubble export   --stepresult pushed --formattype tab --select 'input.b:b,input.c:c' --where 'input.b:B,input.c:C'"
    Then the command output should contain:
    """
    b    |c       
    -----|--------
    B    |C
    A Big|A Circle
    """
    And the command returncode is "0"
        
