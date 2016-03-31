Feature: Bubble storage type:dataset sqlite big chunksize
Scenario: load mysrclient.py pull and store default type sqlite
  Given a file named ".bubble" with:
            """
            bubble=0.7.2
            """
    And a file named "./config/config.yaml" with:
            """
            ---
            CFG:
                BUBBLE:
                    STORAGE_TYPE: dataset
                    STORAGE_DATASET_ARGS:
                        DS_TYPE: sqlite
                        DS_BUBBLE_TAG: testbig
                        DS_CHUNKSIZE: 1000
                DEV:
                    SOURCE:    #pull
                        CLIENT: ./myclient.py
                    TARGET:    #push
                        CLIENT: ./myclient.py
            ...
            """
    And a directory named "./remember/archive"
    And a file named "./myclient.py" with:
            """
            from bubble import Bubble
            class BubbleClient(Bubble):
                def __init__(self,cfg={}):
                    self.CFG=cfg
                def pull(self, amount=100, index=0):
                    self.say('BC:pull: %d,%d'%(amount,index))
                    for i in range(amount):
                        it={'keyA':'A_'+str(i),
                                    'keyB':'B_'+str(i),
                                    'keyC':['c',66,{'keyDinList':'D_'+str(i)}]}
                        self.say('BC:inloop:%d %d'%(amount,index),stuff=it,verbosity=100)
                        yield it
                def push(self, data={}):
                    self.say('BC:push:',stuff=data)
                    return "pushed"
            """
    When I run "mkdir logs"
    When I run "bubble -p pump --amount 10000"
    Then the command output should contain "Pumping finsished"
    And the command returncode is "0"
    When I run "bubble -v0 export -r pushed -p  -i 9999 -a 1 -f tab -c input.keyA"
    Then the command output should contain
          """
          BUBBLE_IDX|input.keyA
          ----------|----------
          9999      |A_9999
          """
    And the command returncode is "0"

