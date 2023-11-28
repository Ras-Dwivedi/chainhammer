# Instruction to installation
These are extra instruction for installation with few updates
## install pyenv to maintain python version
use the following link to install pyenv (https://ggkbase-help.berkeley.edu/how-to/install-pyenv/)

## Install python 3.9
pyenv install 3.9

## install pyenv virtual env and activate the environment
### download the git repo
```
git clone https://github.com/pyenv/pyenv-virtualenv.git $(pyenv root)/plugins/pyenv-virtualenv
```
### Enable the virtual env
```
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
```
## Create a pyenv virtual environment

### Source bashrc
```
source ~/.bashrc 
```
## Create virtual env
```
pyenv virtualenv 3.9.7 hammer-env
```
### activate the virtual env
``` pyenv activate hammer-env```
### upgrade pip
```python -m pip install --upgrade pip```
### before installing all the dependencies install setup tool
```
pip install --upgrade setuptools
```
Install matplotlib
```
pip install matplotlib```
```
pip install py-solc
```
pip install eth-testrpc
pip install eth-tester
```
```
pip install requests
```
```
pip install web3
```
```sudo snap install solc```
### install all the dependencies
```pip install -r requirements.txt```


## How to install pyenv
### Checkout the git repository
 ```$ git clone https://github.com/pyenv/pyenv.git ~/.pyenv``````
### Add to bash profile:
```echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bash_profile```
```$ echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bash_profile ```

Add ```pyenv init``` to your shell to enable shims and autocompletion. Please make sure eval ```$(pyenv init -)```is placed toward the end of the shell configuration file since it manipulates PATH during the initialization.
```$ echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n eval "$(pyenv init -)"\nfi' >> ~/.bash_profile```
Note: There are some systems where the BASH_ENV variable is configured to point to .bashrc. On such systems you should almost certainly put the above mentioned line eval "$(pyenv init -)" into .bash_profile, and not into .bashrc. Otherwise you may observe strange behaviour, such as pyenv getting into an infinite loop. Make sure to check this because of the new ubuntu installation (Jan 2018.)

Restart your shell so the path changes take effect. You can now begin using pyenv.
```$ exec "$SHELL```

## On using the default venv
**Note** that this repository contains a default venev with it.
To use the same python venv, just use the 
```
source venv/bin/activate
```
This virtual env contains the version python `3.7.9`
you might have to install the dependencies afterwards.
for which you can again use 
```
pip install -r requirements.txt
```