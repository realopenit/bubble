Feature: Bubble export
Scenario: Export pushed data in yaml format
  Given a file named ".bubble" with:
            """
            bubble=0.1.1
            """
    And a directory named "./export"
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
                         {"res":200,"input":{"a":"D","b":"E","c":"F"}}
                        ]
            }
            """
    When I run "bubble export   --stepresult pushed --formattype yaml --select 'input.a,input.b,input.c'"
    Then the command output should contain "export/export_pushed_DEV.yaml"
    And the command returncode is "0"
    And the file "export/export_pushed_DEV.yaml" should contain:
            """
            - {input.a: A, input.b: B, input.c: C}
            - {input.a: D, input.b: E, input.c: F}
            """


Scenario: Export pushed data in csv format
  Given a file named ".bubble" with:
            """
            bubble=0.1.1
            """
    And a directory named "./export"
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
                         {"res":200,"input":{"a":"D","b":"E","c":"F"}}
                        ]
            }
            """
    When I run "bubble export   --stepresult pushed --formattype csv --select 'input.a,input.b,input.c'"
    Then the command output should contain "export/export_pushed_DEV.csv"
    And the command returncode is "0"
    And the file "export/export_pushed_DEV.csv" should contain:
            """
            input.a,input.b,input.c
            A,B,C
            D,E,F
            """

Scenario: Export pushed data in json format
  Given a file named ".bubble" with:
            """
            bubble=0.1.1
            """
    And a directory named "./export"
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
                         {"res":200,"input":{"a":"D","b":"E","c":"F"}}
                        ]
            }
            """
    When I run "bubble export   --stepresult pushed --formattype json --select 'input.a,input.c'"
    Then the command output should contain "export/export_pushed_DEV.json"
    And the command returncode is "0"
    #there is no guranteed order in file for ujson..
    #And the file "export/export_pushed_DEV.json" should contain:
    #        """
    #        [{"input.c":"C","input.a":"A"},{"input.c":"F","input.a":"D"}]
    #        and
    #        [{"input.a":"A","input.c":"C"},{"input.a":"D","input.c":"F"}]
    #        are the logically the same
    #        """
Scenario: Export pushed data in tablib default format to stdout
  Given a file named ".bubble" with:
            """
            bubble=0.1.1
            """
    And a directory named "./export"
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
                         {"res":200,"input":{"a":"D","b":"E","c":"F"}}
                        ]
            }
                        """
    When I run "bubble export   --stepresult pushed --formattype tab --select 'input.b,input.c,input.b'"
    Then the command output should contain:
    """
    input.b|input.c|input.b
    -------|-------|-------
    B      |C      |B      
    E      |F      |E      
    """
    
    And the command returncode is "0"


Scenario: Export pushed data in csv format, weird stuff
  Given a file named ".bubble" with:
            """
            bubble=0.1.1
            """
    And a directory named "./export"
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
            {"data":   [{"res":200,"input":{"a":"A","b":"B","c":"C"}},
                        {"res":200,"input":{"a":"#","b":"\"","c":";"}},
                        {"res":200,"input":{"a":"$","b":"A","c":"\""}},
                        {"res":200,"input":{"a":"<","b":">","c":"="}},
                        {"res":200,"input":{"a":1,"b":"with space and comma,like this;","c":"\\"}}
                        ]
            }
            """
    When I run "bubble export   --stepresult pushed --formattype csv --select 'input.a:a,input.X:X,input.b:b,input.c:c'"
    Then the command output should contain "export/export_pushed_DEV.csv"
    And the command returncode is "0"
    And the file "export/export_pushed_DEV.csv" should contain:
            """
            a,X,b,c
            A,None,B,C
            #,None,"""",;
            $,None,A,""""
            <,None,>,=
            1,None,"with space and comma,like this;",\
            """
