Feature: Bubble no transform on empty rules

Scenario Outline: Transform no rule just returns input
    When I apply bubble <rules> on <input> dictionary
    Then I get <output> dictionary
    Examples:
       |input               | rules                                  | output              |
       |{"hello":"world"}   | this is not a rule                     | {"hello":"world"}   |
       |{"hello":"world"}   | >>> this is not a rule                 | {"hello":"world"}   |
       |{"hello":"world"}   | >>>> >>  this is not a rule            | {"hello":"world"}   |
       |{"hello":"world"}   | > > > > > >  this is not a rule        | {"hello":"world"}   |
       |{"hello":"world"}   | >>>>>>>>>                              | {}                  |
       |{"hello":"world"}   | >>> >>> >>>                            | {}                  |
       |{"hello":"world"}   | >>>>>>>>>>>>                           | {}                  |
       |{"hello":"world"}   | >>> >>> >>> >>>                        | {}                  |
       |{"hello":"world"}   | >>> >>> >>> >>> >>> >>>>               | {}                  |
       |{"hello":"world"}   | >>>hello>>> >>> >>> >>> >>>>           | {"hello":"world"}   |
       |{"a":"world"}       | >>>a>>>len>>> >>> >>> >>>>             | {"a":5}             |
       |{"a":"world"}       | >>>a>>>len>>>low>>> >>> >>>>           | {"low":5}           |
       |{"a":"world"}       | >>>a>>>len>>>low>>>dep>>> >>>>         | {"low":5}           |
       |{"a":"world"}       | >>>a>>>len>>>low>>>dep>>>name>>>>      | {"low":5}           |
       |{"hello":"world"}   | >>>>>>>>>>>>>>>>>>                     | {}                  |
       |{"hello":"world"}   | >>> >>> >>> >>> >>> >>>                | {}                  |
       |{"hello":"world"}   | >>> >>>   >>> no_input >>> >>> >>>     | {}                  |
       |{"hello":"world"}   | >>> >>>   >>> no_fun   >>> >>> >>>     | {}                  |
       |{"hello":"world"}   | >>> >>>   >>>    >>> no_out>>> >>>     | {}                  |
       |{"hello":"world"}   | >>> >>>   >>>    >>> no_out>>> >>>     | {}                  |
       |{"hello":"world"}   | >>>>>>>>>>>>>>>>>>>>>                  | {"hello":"world"}   |
       |{"hello":"world"}   | >>>>>>>>>>>>>>>>>>>>>>>>               | {"hello":"world"}   |
       |{"hello":"world"}   | >>>>>>>>>>>>>>>>>>>>>>>>>>>            | {"hello":"world"}   |
       |{"hello":"world"}   | >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>         | {"hello":"world"}   |
       |{"hello":"world"}   | >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>      | {"hello":"world"}   |
       |{"hello":"world"}   | >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>   | {"hello":"world"}   |
