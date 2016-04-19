Feature: Bubble config
Scenario: Given a source service in configuration, add and modify single keys
    Given a new working directory
    When I run "bubble init"
    When I run "bubble config"
        Then the command output should contain "CFG.BUBBLE.STORAGE_TYPE: json"
    When I run "bubble config -s CFG.BUBBLE.STORAGE_TYPE dataset STRING"
    When I run "bubble config -s CFG.BUBBLE.STORAGE_DATASET_ARGS.DS_TYPE sqlite STRING"
    When I run "bubble config -s CFG.BUBBLE.STORAGE_DATASET_ARGS.DS_BUBBLE_TAG config_command STRING"

    When I run "bubble config"
        Then the command output should contain " CFG.BUBBLE.STORAGE_TYPE: dataset"
        Then the command output should contain " CFG.BUBBLE.STORAGE_DATASET_ARGS.DS_TYPE: sqlite"
        Then the command output should contain " CFG.BUBBLE.STORAGE_DATASET_ARGS.DS_BUBBLE_TAG: config_command"

Scenario: Given a source service in configuration, add and modify single keys, display types
    Given a new working directory
    When I run "bubble init"
    When I run "bubble config -s CFG.TEST_CONFIG_STRING something STRING"
    When I run "bubble config -s CFG.TEST_CONFIG_BOOLEAN_True True BOOLEAN"
    When I run "bubble config -s CFG.TEST_CONFIG_BOOLEAN_False False BOOLEAN"
    When I run "bubble config -s CFG.TEST_CONFIG_BOOLEAN_TruE TruE BOOLEAN"
    When I run "bubble config -s CFG.TEST_CONFIG_BOOLEAN_FaLsE FaLsE BOOLEAN"
    When I run "bubble config -s CFG.TEST_CONFIG_BOOLEAN_T T BOOLEAN"
    When I run "bubble config -s CFG.TEST_CONFIG_BOOLEAN_F F BOOLEAN"
    When I run "bubble config -s CFG.TEST_CONFIG_BOOLEAN_YES YES BOOLEAN"
    When I run "bubble config -s CFG.TEST_CONFIG_BOOLEAN_NO NO BOOLEAN"
    When I run "bubble config -s CFG.TEST_CONFIG_BOOLEAN_Y Y BOOLEAN"
    When I run "bubble config -s CFG.TEST_CONFIG_BOOLEAN_N N BOOLEAN"
    When I run "bubble config -s CFG.TEST_CONFIG_INTEGER_42 42 INTEGER"
    When I run "bubble config -s CFG.TEST_CONFIG_INTEGER_MINUS42 "-42" INTEGER"
    When I run "bubble config -s CFG.TEST_CONFIG_FLOAT_PI 3.14159265359 FLOAT"
    When I run "bubble config -s CFG.TEST_CONFIG_FLOAT_MINUSPI "-3.14159265359" FLOAT"
    When I run "bubble config -s CFG.TEST_CONFIG_FLOAT_HEAD 123. FLOAT"
    When I run "bubble config -s CFG.TEST_CONFIG_FLOAT_TAIL .123 FLOAT"

    When I run "bubble config -t"
        Then the command output should contain " CFG.TEST_CONFIG_BOOLEAN_F: False type: BOOLEAN"
        Then the command output should contain " CFG.TEST_CONFIG_BOOLEAN_FaLsE: False type: BOOLEAN"
        Then the command output should contain " CFG.TEST_CONFIG_BOOLEAN_False: False type: BOOLEAN"
        Then the command output should contain " CFG.TEST_CONFIG_BOOLEAN_N: False type: BOOLEAN"
        Then the command output should contain " CFG.TEST_CONFIG_BOOLEAN_NO: False type: BOOLEAN"
        Then the command output should contain " CFG.TEST_CONFIG_BOOLEAN_T: True type: BOOLEAN"
        Then the command output should contain " CFG.TEST_CONFIG_BOOLEAN_TruE: True type: BOOLEAN"
        Then the command output should contain " CFG.TEST_CONFIG_BOOLEAN_True: True type: BOOLEAN"
        Then the command output should contain " CFG.TEST_CONFIG_BOOLEAN_Y: True type: BOOLEAN"
        Then the command output should contain " CFG.TEST_CONFIG_BOOLEAN_YES: True type: BOOLEAN"
        Then the command output should contain " CFG.TEST_CONFIG_INTEGER_42: 42 type: INTEGER"
        Then the command output should contain " CFG.TEST_CONFIG_INTEGER_MINUS42: -42 type: INTEGER"
        Then the command output should contain " CFG.TEST_CONFIG_STRING: something type: STRING"
        Then the command output should contain " CFG.TEST_CONFIG_FLOAT_PI: 3.14159265359 type: FLOAT"
        Then the command output should contain " CFG.TEST_CONFIG_FLOAT_MINUSPI: -3.14159265359 type: FLOAT"
        Then the command output should contain " CFG.TEST_CONFIG_FLOAT_HEAD: 123.0 type: FLOAT"
        Then the command output should contain " CFG.TEST_CONFIG_FLOAT_TAIL: 0.123 type: FLOAT"


Scenario: Given a configuration, add and modify multiple keys
    Given a new working directory
    And a file named "./config_multiple.sh" with:
            """ set -x
                bubble config -s CFG.BUBBLE.STORAGE_TYPE dataset STRING                              \
                              -s CFG.BUBBLE.STORAGE_DATASET_ARGS.DS_TYPE sqlite STRING               \
                              -s CFG.BUBBLE.STORAGE_DATASET_ARGS.DS_BUBBLE_TAG config_command STRING
            """

    When I run "bubble init"
    When I run "bubble config"
        Then the command output should contain " CFG.BUBBLE.STORAGE_TYPE: json"

    When I run "sh ./config_multiple.sh"
    When I run "bubble config"
        Then the command output should contain " CFG.BUBBLE.STORAGE_TYPE: dataset"
        Then the command output should contain " CFG.BUBBLE.STORAGE_DATASET_ARGS.DS_TYPE: sqlite"
        Then the command output should contain " CFG.BUBBLE.STORAGE_DATASET_ARGS.DS_BUBBLE_TAG: config_command"


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
