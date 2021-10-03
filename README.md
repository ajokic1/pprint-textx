# TextX - transform AST into source code

## Description

[TextX](https://github.com/textX/textX) is a tool for creating domain-specific languages in Python. This repository contains modifications which enable the transformation of parsed ASTs (TextX models) into source code, while preserving comments and formatting from the original source code. This functionality was implemented through a set of modifications to the parse-tree generation logic in Arpeggio and the model creation logic in TextX so that additional information about the source code is saved on the model. An extensible printer class was also implemented which handles the transformation of the model into source code using the additional information added to the model. The goal of this functionality is to simplify the creation of language-based tools such as refactoring engines for domain-specific languages created using TextX.

## Setup

Requirements:
- Python 3

Clone the repository:

```
$ git clone https://github.com/ajokic1/pprint-textx.git
```

Create a pyhton virtual environment and activate it:

```
$ cd pprint-textx
$ python -m venv venv
$ source venv/bin/activate
```

Install the modified TextX and Arpeggio packages:

```
$ pip install -e textX
$ pip install -e Arpeggio
```

## Examples

An example which showcases the new functionality is included in the 'drawing' folder. It includes a simple domain-specific language for drawing shapes, and an example implementation of the 'Extract method' refactoring tool using this functionality. In order to run the example, simply run the file 'drawingTest1.py':

```
$ python drawingTest1.py
```
