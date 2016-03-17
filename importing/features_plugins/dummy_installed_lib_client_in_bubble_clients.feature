Feature: Bubble custom installed client combined with pull and push method in bubble.clients
  please note:
  this will not work in edit mode "pip install -e ."
  make dist
  pip install dist/bubble-0.8.7-py2.py3-none-any.whl --upgrade
  behave features_plugins/


Scenario: load installed source client myclient in bubble.clients.myclient
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
                        CLIENT: bubble.clients.mydummyclient
                        URL: http://localhost:8001
                    TRANSFORM:
                        RULES: config/rules.bubble
                    TARGET:    #push
                        CLIENT: dummy
                        URL: http://localhost:8002
            ...
            """

    And a directory named "./remember/archive"
  When I run "pip show bubble"
    Then the command output should contain "/site-packages"

  When I run "pip uninstall bubble-dummy-client -y"
  When I run "pip install ../demo_client/mydummyclient_bubble.clients.mydummyclient/dist/bubble_dummy_client-0.0.1-py2.py3-none-any.whl"
  When I run "pip list installed |grep bubble-dummy-client"
    Then the command output should contain "bubble-dummy-client (0.0.1)"
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
                        CLIENT: bubble.clients.mydummyclient
                        URL: http://localhost:8001
                    TARGET:    #push
                        CLIENT: bubble.clients.mydummyclient
                        URL: http://localhost:8002
            ...
            """

    And a directory named "./remember/archive"
  When I run "pip show bubble"
    Then the command output should contain "/site-packages"
  When I run "pip uninstall bubble-dummy-client -y"
  When I run "pip install ../demo_client/mydummyclient_bubble.clients.mydummyclient/dist/bubble_dummy_client-0.0.1-py2.py3-none-any.whl"
  When I run "pip list installed |grep bubble-dummy-client"
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
