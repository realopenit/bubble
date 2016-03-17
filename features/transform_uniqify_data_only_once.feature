Feature: Bubble pre transform uniqify data only once
Scenario: Preprocess make uniq pull
  Given a file named ".bubble" with:
            """
            bubble=0.4.1
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
                    return  [{"id":"1","name":"me:first"},
                             {"id":"2","name":"my:first"}
                            ]
    
            """
    And a file named "./remember/uniq_pull_DEV.json" with:
            """
            {"data":[]}
            """
    And a file named "./remember/store_DEV.json" with:
            """
            {"data":[]}
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
    When I run "bubble export -r uniq_pull -c uid,history_amount -kv -f tab --order uid"
    Then the command returncode is "0"
    And the command output should contain:
            """
            uid|history_amount
            ---|--------------
            [1]|1
            [2]|1
            """
    But note that "doing it again will not add history because of storetimestamp"
    When I run "bubble -v 10000 transform"
    Then the command output should contain "Transforming"
    When I run "bubble export -r uniq_pull -c uid,history_amount -kv -f tab --order uid"
    Then the command returncode is "0"
    And the command output should contain:
            """
            uid|history_amount
            ---|--------------
            [1]|1
            [2]|1
            """
