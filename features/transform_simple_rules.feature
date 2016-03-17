Feature: Bubble transformation

Scenario Outline: Transform a dictionary to another one using single bubble rule defs
    When I apply bubble <rules> on <input> dictionary
    Then I get <output> dictionary

    Examples:
       |input               | rules                                  | output              |
       |{"hello":"world"}   | >>>hello>>>                            | {"hello":"world"}   |
       |{"hello":"world"}   | >>>hello>>>size>>>                     | {"hello":5}         |
       |{"hello":"world"}   | >>>hello>>>size>>>wlen>>>              | {"wlen":5}          |
       |{"i":"bubble"}      | >>>i>>>len>>>u>>>                      | {"u":6}             |
       |{"hi":"1"}          | >>>hi>>>adder>>>o>>>                   | {"o":2}             |
       |{"i":"h2g2"}        | >>>i>>>the_answer>>>the_answer>>>      | {"the_answer":42}   |
       |{}                  | >>>'insiders'>>> >>>.add_temp_var>>>   | {}                  |
       |{"this":"renaming"} | >>>this>>>>>>that>>>                   | {"that":"renaming"} |
