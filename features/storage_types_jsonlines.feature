Feature: Bubble storage types
Scenario: load mysrclient.py pull and store type jsonlines
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
                def pull(self, amount=100000, index=0):
                    self.say('BC: %d,%d'%(amount,index))
                    for i in range(amount):
                        it={'keyA':'A_'+str(i),
                                    'keyB':'B_'+str(i),
                                    'keyC':['c',66,{'keyDinList':'D_'+str(i)}]}
                        self.say('BC:yielding:%d %d'%(amount,index),stuff=it,verbosity=100)
                        yield it
            """
    When I run "bubble -v 100000 -b 100 pull"
    Then the command output should contain "pulled [100000] objects"
    Then the command output should contain "remember/pulled_DEV.jsonl"
    And the command returncode is "0"
    When I run "bubble export -r pulled -kvp -f tab -c keyA,keyB,keyC.1,keyC.2,keyC.3.keyDinList -a 10"
    Then the command returncode is "0"
    And the command output should contain
      """
      BUBBLE_IDX|keyA|keyB|keyC.1|keyC.2|keyC.3.keyDinList
      ----------|----|----|------|------|-----------------
      0         |A_0 |B_0 |c     |66    |D_0
      1         |A_1 |B_1 |c     |66    |D_1
      2         |A_2 |B_2 |c     |66    |D_2
      3         |A_3 |B_3 |c     |66    |D_3
      4         |A_4 |B_4 |c     |66    |D_4
      5         |A_5 |B_5 |c     |66    |D_5
      6         |A_6 |B_6 |c     |66    |D_6
      7         |A_7 |B_7 |c     |66    |D_7
      8         |A_8 |B_8 |c     |66    |D_8
      9         |A_9 |B_9 |c     |66    |D_9
      """
    When I run "bubble export -r pulled -kvp -f tab -c keyA,keyB,keyC.1,keyC.2,keyC.3.keyDinList -i 99990 -a 10"
    Then the command returncode is "0"
    And the command output should contain
      """
      BUBBLE_IDX|keyA   |keyB   |keyC.1|keyC.2|keyC.3.keyDinList
      ----------|-------|-------|------|------|-----------------
      99990     |A_99990|B_99990|c     |66    |D_99990
      99991     |A_99991|B_99991|c     |66    |D_99991
      99992     |A_99992|B_99992|c     |66    |D_99992
      99993     |A_99993|B_99993|c     |66    |D_99993
      99994     |A_99994|B_99994|c     |66    |D_99994
      99995     |A_99995|B_99995|c     |66    |D_99995
      99996     |A_99996|B_99996|c     |66    |D_99996
      99997     |A_99997|B_99997|c     |66    |D_99997
      99998     |A_99998|B_99998|c     |66    |D_99998
      99999     |A_99999|B_99999|c     |66    |D_99999
      """
