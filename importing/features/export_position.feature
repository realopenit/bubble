Feature: Bubble export selection with position flag
Scenario: running export with select with position flag
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
  When I run "bubble export   -r pushed -f tab -c 'input.a:first,input.b:b,input.c:second' -p"
    Then the command output should contain:
    """
    BUBBLE_IDX|first|b|second
    ----------|-----|-|------
    0         |A    |B|C
    1         |AA   |E|one
    2         |Z    |E|Z
    3         |AA   |E|two
    """
    And the command returncode is "0"
