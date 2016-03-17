Feature: Bubble custom local client
Scenario: load mysrclient.py in the Bubble directory
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
                        CLIENT: ./mysrcclient.py
                        URL: http://localhost:8001
                    TRANSFORM:
                        RULES: config/rules.bubble
                    TARGET:    #push
                        CLIENT: dummy
                        URL: http://localhost:8002
            ...
            """

    And a directory named "./remember/archive"
    And a file named "./mysrcclient.py" with:
            """
            from bubble import Bubble
            class BubbleClient(Bubble):
                def __init__(self,cfg={}):
                    self.CFG=cfg
                def pull(self, *args, **kwargs):
                    self.say('pull:args:',stuff=args)
                    self.say('pull:kwargs:',stuff=args)
                    return [{'LATIN SMALL LETTER U WITH DIAERESIS':u"\xfc"}]
            """

  When I run "bubble pull"
    Then the command output should contain "pulled [1] objects"
    Then the command output should contain "remember/pulled_DEV.json"
    And the command returncode is "0"
  When I run "bubble export --stepresult pulled --select 'LATIN SMALL LETTER U WITH DIAERESIS:char' --showkeys -f tab"
    Then the command returncode is "0"
    And the command output should contain:
            """
            char
            ----
            ü
            """