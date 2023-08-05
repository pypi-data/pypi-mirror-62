# A simple Calculator Project

In this project, i used a *Fire* to solve expressions such as BODMAS,which solves multiple operations i.e addition,subtraction,multiplication and division. Where *fire* is a Python library that will turn any Python component into a command line interface with just a single call to Fire.
The easiest way to use *Fire* is to take any Python program, and then simply call fire.Fire() at the end of the program. This will expose the full contents of the program to the command line.

**Getting Started**

How to run project?

1. Create a virtual environment on your local machine
```
python3 -m venv env
```
2. Activate virtual environment
```
source env/bin/activate
```
3. Make a local directory

4. Clone project in your directory
```
git clone https://github.com/mugdhadalal/pycalci.git
```
5. Install setup.py
```
python3 setup.py install
```
6. Use command pycalci,it will show you commands
```
$ pycalci

NAME
    pycalci
SYNOPSIS
    pycalci COMMAND
COMMANDS
    COMMAND is one of the following:

     solve
```
7. use pycalci solve EXPRESSION
```
$ pycalci solve 2+4*5/2
12.0
```

**Example**
```
import fire

def hello(name):
  return 'Hello {name}!'.format(name=name)

if __name__ == '__main__':
  fire.Fire()
```
Here's how we can run our program from the command line:
```
$ python example.py hello World
Hello World!
```

**Dependancies**

Scripting Language =	Python 3.0+

Command-Line Option  =	fire
