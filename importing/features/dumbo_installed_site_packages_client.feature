Feature: Bubble custom installed client combined with pull and push method in site packages
Scenario: load installed source client myclient in site packages
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
                        CLIENT: mydumboclient.mydumboclient
                        URL: http://localhost:8001
                    TRANSFORM:
                        RULES: config/rules.bubble
                    TARGET:    #push
                        CLIENT: dummy
                        URL: http://localhost:8002
            ...
            """

    And a directory named "./remember/archive"
  When I run "pip uninstall bubble-dumbo-client -y"
  When I run "pip install ../demo_client/mydumboclient_site_packages.mydumboclient/dist/bubble_dumbo_client-0.0.1-py2.py3-none-any.whl"
  When I run "pip list installed |grep bubble-dumbo-client"
    Then the command output should contain "bubble-dumbo-client (0.0.1)"
  When I run "bubble pull"
    Then the command output should contain "pulled [143] objects"
    Then the command output should contain "remember/pulled_DEV.json"
    And the command returncode is "0"
  When I run "bubble export --stepresult pulled --select 'dummy' -kv -f tab -i 142 -a 1"
    Then the command returncode is "0"
    And the command output should contain:
            """
            dummy
            ---------
            dummy_142
            """
            
Scenario: load installed target client myclient in bubble.clients.myclient
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
                        CLIENT: mydumboclient.mydumboclient
                        URL: http://localhost:8001
                    TARGET:    #push
                        CLIENT: mydumboclient.mydumboclient
                        URL: http://localhost:8002
            ...
            """

    And a directory named "./remember/archive"
    When I run "pip uninstall bubble-dumbo-client -y"
    When I run "pip install ../demo_client/mydumboclient_site_packages.mydumboclient/dist/bubble_dumbo_client-0.0.1-py2.py3-none-any.whl"
    When I run "pip list installed |grep bubble-dumbo-client"

    When I run "bubble pull"
    Then the command output should contain "pulled [143] objects"
    Then the command output should contain "remember/pulled_DEV.json"
    And the command returncode is "0"
   When I run "bubble push"
    Then the command output should contain "pushed [143] objects"
    Then the command output should contain "remember/pushed_DEV.json"
    And the command returncode is "0"
    When I run "bubble export --stepresult pushed --select  res,input.dummy -kv -f tab -i 142 -a 1"
    Then the command returncode is "0"
    And the command output should contain:
            """
            res|input.dummy
            ---|-----------
            OK |dummy_142
            """

