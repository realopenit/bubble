Feature: Bubble export selection with select option as aliases
Scenario: running export with select string key:alias
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
    When I run "bubble export   --stepresult pushed --formattype tab --select 'input.a:first,input.b:b,input.c:second'"
    Then the command output should contain:
    """
    first|b|second
    -----|-|------
    A    |B|C
    AA   |E|one
    Z    |E|Z
    AA   |E|two
    """
    And the command returncode is "0"
