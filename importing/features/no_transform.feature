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
                        CLIENT: ./dummy.py
                        URL: http://localhost:8001
                    TARGET:    #push
                        CLIENT: ./dummy.py
                        URL: http://localhost:8002
            ...
            """

    And a file named "./dummy.py" with:
            """
            from bubble import Bubble

            class BubbleClient(Bubble):
                def __init__(self,cfg=None):
                    pass
                def push(self,*a,**k):
                    pass

                def pull(self,*a,**k):
                    for i in range(143):
                        yield {'dummy':"dummy_"+str(i)}
            """
    And a directory named "./remember/archive"

    When I run "bubble pull"
    When I run "bubble transform"
    Then the command output should contain "There is no transform defined in the configuration"
    And the command returncode is "1"
    When I run "bubble push"
    Then the command output should contain "There is no transform defined in the configuration"
    And the command returncode is "0"
    When I run "bubble export -r pushed -c input.dummy -f tab -i 142 -a 1"
      Then the command returncode is "0"
      And the command output should contain:
        """
        input.dummy
        -----------
        dummy_142
        """
