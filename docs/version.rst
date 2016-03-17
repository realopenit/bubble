.. _id.versioning:

Versioning
----------

Bubble has a simple date versioning, YYYY.MM.DD  (long: preferred, with leading zeroes)
    for example: 2016.02.23
this is the date on which the package has been built.


This still has the appearance of ag "regular" versioning scheme, with the added advantage of
 a user instantly knowing how "old" or "mature" or "buggy" the software is.
furthermore it is easily comparable:
suppose you have two versions: "2016.02.23" and "2016.01.01"
#drop the dots, and make integer values
20160223 > 20160101 so "2016.02.23" is the newer and most likely the better version.


In case the YYYY is too big  we could also adopt a shorter, YY.M.D(short,
       years after 2000, without leading zeroes, but the dots stay!)
    for example: 16.2.23

when building the package the message " Normalizing '2016.03.10' to '2016.3.10'" will appear.


What happens after the building and fixating the "version" is testing and releasing, something like this.

And remaining in the downloads/DEV          --> local: http://doc.devpi.net/latest/quickstart-pypimirror.html
promote DEV->TEST
https://wiki.python.org/moin/TestPyPI
And remaining in the downloads/TEST         --> devpypi: https://testpypi.python.org/pypi
promote TEST->PRODUCTION
And remaining in the downloads/PRODUCTION   --> pypi: https://pypi.python.org/pypi

# TODO define all the stages needed
# TODO setup downloads and promotion like above


So the source of your package defines the status and NOT the version, which is only a date disguised as version.


# http://python-packaging-user-guide.readthedocs.org/en/latest/distributing/#choosing-a-versioning-scheme
# https://www.python.org/dev/peps/pep-0440/