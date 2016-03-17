Feature: Bubble transform config dict
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
            {"data":     [{"hello":"hi"}]}
            """
    And a directory named "./remember/archive"
    And a file named "./config/rules.bubble" with:
            """
            read from configuration and args
            >>> ~ARGS.stage            >>>       >>> current_stage     >>>
            >>> ~ARGS.stage            >>>       >>> path              >>>
            >>> ~CFG.DEV.SOURCE.CLIENT >>>       >>> src_client        >>>
            >>> ~CFG.DEV.SOURCE.**     >>> as_is >>> src               >>>
            
            """
    And a file named "./custom_rule_functions.py" with:
            """
            from bubble.functions import register
            @register
            def as_is(inp):
                return inp
            """
  When I run "bubble transform"
    Then the command output should contain "Transforming"
    And the command returncode is "0"
    
    When I run "bubble export -r push -c 'current_stage,src_client,src.CLIENT' -f tab"
      Then the command returncode is "0"
      And the command output should contain:
        """
        current_stage|src_client|src.CLIENT
        -------------|----------|----------
        DEV          |dummy     |dummy
        """
