Feature: Bubble pre transform uniqify
Scenario: Preprocess make uniq pull
  Given a file named ".bubble" with:
            """
            bubble=0.3.3
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
                        CLIENT: ./mysrcclient.py
                    TRANSFORM:
                        UNIQ_KEYS_PULL: id
                        DELTAS_ONLY: False
                        RULES: config/rules.bubble
                    TARGET:    #push
                        CLIENT: dummy
            ...
            """

    And a file named "./mysrcclient.py" with:
            """
            from bubble import Bubble
            class BubbleClient(Bubble):
                def __init__(self,cfg={}):
                    self.CFG=cfg
                def pull(self, *args, **kwargs):
                    self.say('pull:args:',stuff=args)
                    self.say('pull:kwargs:',stuff=args)
                    return  [{"id":"1","name":"me:first"},
                             {"id":"1","name":"me:last"}
                            ]
    
            """


    And a directory named "./remember/archive"
    And a file named "./config/rules.bubble" with:
            """
            >>>name>>>
            """
    And a file named "./custom_rule_functions.py" with:
            """
            """
  When I run "bubble pull"
    Then the command output should contain "pulled [2] objects"
    Then the command output should contain "remember/pulled_DEV.json"
    And the command returncode is "0"
  When I run "bubble -v 10000 transform"
    Then the command output should contain "Transforming"
  When I run "bubble export -r uniq_pull -c delta.equal,uid,delta.modified.1.from,delta.modified.1.key,delta.modified.1.to -kp -f tab"
    Then the command returncode is "0"
    And the command output should contain:
            """
            BUBBLE_IDX|delta.equal|uid|delta.modified.1.from|delta.modified.1.key|delta.modified.1.to
            ----------|-----------|---|---------------------|--------------------|-------------------
            0         |False      |[1]|me:first             |name                |me:last

            """
    When I run "bubble export -r push -c name -kvp -f tab"
    Then the command returncode is "0"
    And the command output should contain:
            """
            BUBBLE_IDX|name
            ----------|-------
            0         |me:last

            """
Scenario: Preprocess make unig multiple keys
  Given a file named ".bubble" with:
            """
            bubble=0.3.3
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
                        CLIENT: ./mysrcclient.py
                        URL: http://localhost:8001
                    TRANSFORM:
                        UNIQ_KEYS_PULL: id,name
                        DELTAS_ONLY: False
                        RULES: config/rules.bubble
                    TARGET:    #push
                        CLIENT: dummy
                        URL: http://localhost:8002
            ...
            """
    And a file named "./mysrcclient.py" with:
            """
            from bubble import Bubble
            class BubbleClient(Bubble):
                def __init__(self,cfg={}):
                    self.CFG=cfg
                def pull(self, *args, **kwargs):
                    self.say('pull:args:',stuff=args)
                    self.say('pull:kwargs:',stuff=args)
                    return  [{"id":"1","name":"me:first","letter":"A"},
                             {"id":"2","name":"myself:first","letter":"B"},
                             {"id":"1","name":"me:first","letter":"C"}
                            ]
            """
    And a directory named "./remember/archive"
    And a file named "./config/rules.bubble" with:
            """
            >>>name>>>
            """
    And a file named "./custom_rule_functions.py" with:
            """
            """
  When I run "bubble pull"
    Then the command output should contain "pulled [3] objects"
    Then the command output should contain "remember/pulled_DEV.json"
    And the command returncode is "0"
    
    When I run "bubble transform"
    Then the command output should contain "Transforming"
    And the command returncode is "0"

    When I run "bubble export -r uniq_pull -c delta.equal,uid,delta.modified.1.from,delta.modified.1.key,delta.modified.1.to -kv -f tab --order uid:+"
    Then the command returncode is "0"
    And the command output should contain:
            """
            delta.equal|uid               |delta.modified.1.from|delta.modified.1.key|delta.modified.1.to
            -----------|------------------|---------------------|--------------------|-------------------
            False      |[1]_[me:first]    |A                    |letter              |C
            None       |[2]_[myself:first]|None                 |None                |None
            """
