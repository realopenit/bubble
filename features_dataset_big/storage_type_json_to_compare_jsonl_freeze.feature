Feature: Bubble storage type:jsonl  to compare with DS freeze_json
Scenario: load mysrclient.py pull and store to jsonl
  Given a file named ".bubble" with:
            """
            bubble=2016.04.21
            """
    And a file named "./config/config.yaml" with:
            """
            ---
            CFG:
                BUBBLE:
                    STORAGE_TYPE: jsonl
                DEV:
                    SOURCE:    #pull
                        CLIENT: ./mysrcclient.py
            ...
            """
    And a directory named "./remember/archive"
    And a file named "./mysrcclient.py" with:
            """
            from bubble import Bubble
            class BubbleClient(Bubble):
                def __init__(self,cfg={}):
                    self.CFG=cfg
                def pull(self, amount=100, index=0):
                    self.say('BC: %d,%d'%(amount,index))
                    for i in range(amount):
                        it={'keyA':'A_'+str(i),
                                    'keyB':'B_'+str(i),
                                    'keyC':['c',66,{'keyDinList':'D_'+str(i)}]}
                        self.say('BC:inloop:%d %d'%(amount,index),stuff=it,verbosity=100)
                        yield it
                    #return ret
            """
    When I run "bubble pull --amount 10000"
    Then the command output should contain "pulled [10000] objects"
    Then the command output should contain "remember/pulled_DEV.jsonl"
    And the command returncode is "0"
    When I run "bubble -v0 export -r pulled -p  -i 9999 -a 1 -f tab -c keyC.3.keyDinList"
    Then the command output should contain
          """
          BUBBLE_IDX|keyC.3.keyDinList
          ----------|-----------------
          9999      |D_9999
          """
    And the command returncode is "0"

