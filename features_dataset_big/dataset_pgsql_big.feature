Feature: Bubble storage type:dataset postgresql big
Scenario: load mysrclient.py pull and store postgresql
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
                        DS_BUBBLE_TAG: testbig
                        DS_TYPE: postgresql
                        DS_HOST: localhost
                        DS_DB: bubble
                        DS_PORT: 3000
                        DS_USER: bubble
                        DS_PASSWORD: bubble
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
    Then the command output should contain "saved result in dataset[step:pulled][stage:DEV]"
    And the command returncode is "0"
    When I run "bubble -v0 export -r pulled -p  -i 9999 -a 1 -f tab -c keyC.3.keyDinList"
    Then the command output should contain
          """
          BUBBLE_IDX|keyC.3.keyDinList
          ----------|-----------------
          9999      |D_9999
          """
    And the command returncode is "0"
