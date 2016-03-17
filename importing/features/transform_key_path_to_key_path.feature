Feature: Bubble transform key paths
Scenario: key path a.b.c should be copied to key path d.e.f
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

    And a file named "./remember/pulled_DEV.json" with:
            """
            {"timestamp": "2014-12-15T16:15:39.530314+00:00",
            "client": {  "URL": "http://localhost:8001",
                            "CLIENT": "service_hello_dummy"
                        },
            "data":     [{"a":{"b":{"c":"hello"}}}]
            }
            """
    And a file named "./remember/store_DEV.json" with:
            """
            {"data":[]}
            """
    And a directory named "./remember/archive"
    And a file named "./config/rules.bubble" with:
            """

            create the full path for destination path
            copy a.b.c to d.e.f
            >>> a.b.c >>> >>> d.e.f >>>

                        """
    And a file named "./custom_rule_functions.py" with:
            """
            #no define rule functions
            rule_functions={}
            """
    When I run "bubble transform"
    Then the command output should contain "Transforming"
    And the command returncode is "0"
    When I run "bubble export -r push -c 'd.e.f' -f tab"
      Then the command returncode is "0"
      And the command output should contain:
        """
        d.e.f
        -----
        hello
        """

Scenario: Transform: key path a.2.c should be copied to key path d.3.f
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

    And a file named "./remember/pulled_DEV.json" with:
            """
            {"timestamp": "2014-12-15T16:15:39.530314+00:00",
            "client": {  "URL": "http://localhost:8001",
                            "CLIENT": "service_hello_dummy"
                        },
            "data":     [
                           {"a": ["",
                                  "",
                                 {"c":"hello"}
                                 ]
                            }
                          ]
            }
            """
    And a file named "./remember/store_DEV.json" with:
            """
            {"data":[]}
            """
    And a directory named "./remember/archive"
    And a file named "./config/rules.bubble" with:
            """

            create the full path for destination path
            a list in d

            >>>'world'               >>>       >>> d.1.2.3.hello           >>>
            >>>'some cheese for the mouse' >>> >>>  where.do.you.want.this? >>>

            key path a.3.c should be copied to key path d.4.f
            >>> a.3.c >>> >>> d.4.f >>>

                        """
    And a file named "./custom_rule_functions.py" with:
            """
            """
    When I run "bubble transform"
    Then the command output should contain "Transforming"
    And the command returncode is "0"
    When I run "bubble export -r push -c 'where.do.you.want.this?' -f tab"
      Then the command returncode is "0"
      And the command output should contain:
        """
        where.do.you.want.this?
        -------------------------
        some cheese for the mouse
        """
