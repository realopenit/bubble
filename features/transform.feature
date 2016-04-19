Feature: Bubble transform
Scenario: Transform pulled data using custom rules and functions
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
            "data": [{"hello":"hi"},
                       {"hello":"bubble"}
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
            use constant E7dal as input for the hello rule function and store
            result in hello_e7dal
            >>>"E7dal">>> hello >>>hello_e7dal>>>
            """
    And a file named "./custom_rule_functions.py" with:
            """
            from bubble.functions import register
            def hi(name='world'):
                return "hello %s:)"%name
            register(hi,'hello')
            """
    When I run "bubble transform"
    Then the command output should contain "Transforming"
    And the command returncode is "0"
    When I run "bubble export -r push -c 'hello_e7dal' -f tab"
      Then the command returncode is "0"
      And the command output should contain:
        """
        hello_e7dal
        -------------
        hello E7dal:)
        hello E7dal:)
        """
Scenario: Transform pulled data using custom rules and functions,internal value
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
            "data": [{"hello":"hi"},
                       {"hello":"bubble"}
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
            a simple rule that will just copy 'hello' from input to output
            >>>hello>>> >>>hi>>>

            store the value of hi internally as internal_hi

            >>>hello>>> >>>.internal_hi>>>

            is the value of the internal hi equal to 'hi',
            store boolean result value as internal_hello_is_hi
            >>>.internal_hi,'hi'>>>equal>>>.internal_hello_is_hi>>>

            if the internally stored boolean value is true,
            then put "okidoki" in to hello_is_hi output variable
            >>>.internal_hello_is_hi:'okidoki'>>> >>> hello_is_hi>>>

            """
    And a file named "./custom_rule_functions.py" with:
            """
            from bubble.functions import register
            def hi(name='world'):
                return "hello %s:)"%name
            register(hi,'hello')
            """
    When I run "bubble transform"
    Then the command output should contain "Transforming"
    And the command returncode is "0"
    When I run "bubble export -r push -c 'hi,hello_is_hi' -f tab"
      Then the command returncode is "0"
      And the command output should contain:
        """
        hi    |hello_is_hi
        ------|-----------
        hi    |okidoki
        bubble|None
        """
Scenario: Given a source service in configuration with only DEV
    Given a new working directory
    When I run "bubble init"
    When I run "bubble pull"
    When I run "bubble transform -s PROD"
    Then the command output should contain "There is no STAGE in CFG:PROD"
    And the command returncode is "1"
