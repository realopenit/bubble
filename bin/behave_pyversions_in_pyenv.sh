set -x
pip install wheel
make dist

#make backup for current pyenv version
mv  .python-version .python-version.BEAST

for env in 2.6.9 2.7.9 2.7.10 pypy-portable-4.0.1 2.7.11 3.5.0 3.5.1
do
   #pyenv install env   # this is only needed on creation
   pname="beast_bu_${env}_test_behave"
   pyenv uninstall -f $pname
   pyenv virtualenv $env $pname
   pyenv local $pname
   echo running in env: $env
   echo running in env:name: $pname
   pyenv local $pname
   pip list
   pip install ./dist/bubble-*-py2.py3-none-any.whl
   pip install -r dev_requirements.txt
   python --version && behave --version && bubble --version
   time behave --format=progress
done

#restore backup for current pyenv version
mv  .python-version.BEAST .python-version
