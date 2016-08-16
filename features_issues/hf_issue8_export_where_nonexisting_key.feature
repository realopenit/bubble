Feature: hf: export selection with where nonexisting key option
	please have a look at https://github.com/realopenit/bubble/issues/8
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
            {"data": [{"res":200,"input":{"a":"s1","b":"B","c":"C"}},
                      {"res":200,"input":{"a":"s2","b":"E","c":"one","X":"wontSELECT"}},
                      {"res":200,"input":{"a":"s3","b":"E","c":"Z","X":"A"}},
                      {"res":200,"input":{"a":"s4","b":"E","c":"Z","X":"AA"}},
                      {"res":200,"input":{"a":"s5","b":"E","c":"two","X":"AAAA"}},
                      {"res":200,"input":{"a":"s6","b":"E","c":"two","X":"there is AA in here too"}}
                     ]
            }
            """
    When I run "bubble export   --stepresult pushed --formattype tab --select 'input.a:a,input.X:X' --where 'input.X:AA'"
    Then the command output should contain:
    """
    a |X
    --|-----------------------
    s4|AA
    s5|AAAA
    s6|there is AA in here too
    """
    And the command returncode is "0"
