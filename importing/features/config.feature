Feature: Bubble config
Scenario: Given a source service in configuration, add and modify single keys
    Given a new working directory
    When I run "bubble init"
    When I run "bubble config"
        Then the command output should contain "CFG.BUBBLE.STORAGE_TYPE: json"
    When I run "bubble config -s CFG.BUBBLE.STORAGE_TYPE dataset"
    When I run "bubble config -s CFG.BUBBLE.STORAGE_DATASET_ARGS.DS_TYPE sqlite"
    When I run "bubble config -s CFG.BUBBLE.STORAGE_DATASET_ARGS.DS_BUBBLE_TAG config_command"

    When I run "bubble config"
        Then the command output should contain " CFG.BUBBLE.STORAGE_TYPE: dataset"
        Then the command output should contain " CFG.BUBBLE.STORAGE_DATASET_ARGS.DS_TYPE: sqlite"
        Then the command output should contain " CFG.BUBBLE.STORAGE_DATASET_ARGS.DS_BUBBLE_TAG: config_command"

    When I run "bubble pull"
        Then the command output should contain "saved result in dataset[step:stats][stage:DEV]"
        But note that "the command output should contain \"saved result in [\" for the previous storage type json"
        And the command returncode is "0"

Scenario: Given a configuration, add and modify multiple keys
    Given a new working directory
    And a file named "./config_multiple.sh" with:
            """ set -x
                bubble config -s CFG.BUBBLE.STORAGE_TYPE dataset                              \
                              -s CFG.BUBBLE.STORAGE_DATASET_ARGS.DS_TYPE sqlite               \
                              -s CFG.BUBBLE.STORAGE_DATASET_ARGS.DS_BUBBLE_TAG config_command
            """

    When I run "bubble init"
    When I run "bubble config"
        Then the command output should contain " CFG.BUBBLE.STORAGE_TYPE: json"

    When I run "sh ./config_multiple.sh"
    When I run "bubble config"
        Then the command output should contain " CFG.BUBBLE.STORAGE_TYPE: dataset"
        Then the command output should contain " CFG.BUBBLE.STORAGE_DATASET_ARGS.DS_TYPE: sqlite"
        Then the command output should contain " CFG.BUBBLE.STORAGE_DATASET_ARGS.DS_BUBBLE_TAG: config_command"

    When I run "bubble pull"
        Then the command output should contain "saved result in dataset[step:stats][stage:DEV]"
        But note that "the command output should contain \"saved result in [\" for the previous storage type json"
        And the command returncode is "0"

Scenario: Given a configuration,copy a single src key to a single dest key
    Given a new working directory
    When I run "bubble init"
    When I run "bubble  -v 0 config -c CFG.DEV.TRANSFORM.RULES CFG.ACC.TRANSFORM.RULES"
    When I run "bubble config"
        Then the command output should contain " CFG.ACC.TRANSFORM.RULES: config/rules.bubble"

Scenario: Given a configuration,copy a star single src.* key to a dest key
    Given a new working directory
    When I run "bubble init"
    When I run "bubble  -v 0 config -c CFG.DEV.* CFG.ACC"
    When I run "bubble config"
        Then the command output should contain " CFG.ACC.TRANSFORM.RULES: config/rules.bubble"
        Then the command output should contain " CFG.ACC.TARGET.CLIENT: ./mytgtclient.py"


Scenario: Given a configuration,delete a single key
    Given a new working directory
    When I run "bubble init"
    When I run "bubble  -v 0 config -d CFG.DEV.TRANSFORM.RULES"
    When I run "bubble config"
        Then the command output should not contain " CFG.DEV.TRANSFORM.RULES: config/rules.bubble"

Scenario: Given a source service in configuration,delete branch of key.*
    Given a new working directory
    When I run "bubble init"
    When I run "bubble -v 0 config -d CFG.DEV.TRANSFORM.*"
    When I run "bubble config"
        Then the command output should not contain " CFG.DEV.TRANSFORM.RULES: config/rules.bubble"
