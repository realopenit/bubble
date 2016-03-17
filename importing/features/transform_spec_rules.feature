Feature: Bubble allowed specs rules

Scenario Outline: Transform allowed specs
    When I apply bubble <rules> on <input> dictionary
    Then I get <output> dictionary
    Examples:
       |input               | rules                                  | output              |
       |{"hello":"world"}   | >>>>>>>>>>>>>>>                        | {}                  |
       |{"hello":"world"}   |    i                                   | {"hello":"world"}   |
       |{"hello":"world"}   | >>> >>>                                | {}                  |
       |{"hello":"world"}   |    i   f                               | {"hello":"world"}   |
       |{"hello":"world"}   | >>> >>> >>>                            | {}                  |
       |{"hello":"world"}   |    i   f   o                           | {"hello":"world"}   |
       |{"hello":"world"}   | >>> >>> >>> >>>                        | {}                  |
       |{"hello":"world"}   |    i   f   o   d                       | {"hello":"world"}   |
       |{"hello":"world"}   | >>> >>> >>> >>> >>>                    | {}                  |
       |{"hello":"world"}   |    i   f   o   d   n                   | {"hello":"world"}   |
       |{"hello":"world"}   | >>> >>> >>> >>> >>> >>>>               | {}                  |
       |{"hello":"world"}   | >>>hello>>> >>> >>> >>> >>>>           | {"hello":"world"}   |
       |{"a":"world"}       | >>>a>>>len>>> >>> >>> >>>>             | {"a":5}             |
       |{"a":"world"}       | >>>a>>> >>>goodbye>>>                  | {"goodbye":"world"} |
       |{"a":"world"}       | >>>a>>>len>>>low>>> >>> >>>>           | {"low":5}           |
       |{"a":"world"}       | >>>a>>>len>>>low>>>dep>>> >>>>         | {"low":5}           |
       |{"a":"world"}       | >>>a>>>len>>>low>>>dep>>>name>>>>      | {"low":5}           |
