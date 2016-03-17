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
            {"data":     [{"hello":"hi"}]}
            """
    And a file named "./remember/store_DEV.json" with:
            """
            {"data":[{"fruits": {  "pear": {"color":"red"}}}]}
            """
    And a directory named "./remember/archive"
    And a file named "./config/rules.bubble" with:
            """


            read from persistent storage and keep in temp dict
            >>> ;fruits.pear.color         >>>       >>> pre                      >>>
            >>> ;fruits.pear.color,'red'   >>> equal >>> pre_yes_it_is_red        >>>

            write new value
            >>> 'green'                    >>>       >>> ;fruits.pear.color       >>>
            >>> ;fruits.pear.color         >>>       >>> post >>>
            >>> ;fruits.pear.color,'green' >>> equal >>> post_yes_it_is_green_now >>>

            """
    And a file named "./custom_rule_functions.py" with:
            """
            #no define rule functions
            """
  When I run "bubble transform"
    Then the command output should contain "Transforming"
    And the command returncode is "0"
    
    When I run "bubble export -r push -c 'pre,pre_yes_it_is_red,post,post_yes_it_is_green_now' -f tab"
      Then the command returncode is "0"
      And the command output should contain:
          """
          pre|pre_yes_it_is_red|post |post_yes_it_is_green_now
          ---|-----------------|-----|------------------------
          red|True             |green|True
          """
    
    When I run "bubble export -r store -c 'fruits.pear.color' -f tab"
      Then the command returncode is "0"
      And the command output should contain:
          """
          fruits.pear.color
          -----------------
          green
          """