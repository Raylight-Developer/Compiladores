from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import traceback
import antlr4
import sys
import os
import re

from PySide6.QtWidgets import QWidget
from graphviz import Digraph
from antlr4 import *
from typing import *

RESET  = "</span>"
R      = "<span style = 'color:rgb(250,50,50);' >"
G      = "<span style = 'color:rgb(50,250,50);' >"
B      = "<span style = 'color:rgb(50,50,250);' >"
Y      = "<span style = 'color:rgb(250,250,50);' >"
TEST   = "<span style = 'color:rgb(100,100,100);' >"
TAB  = "&nbsp;&nbsp;&nbsp;&nbsp;"
HTAB = "&nbsp;&nbsp;"

def parse_args(args: str):
	options = {"render" : False}
	for arg in args:
		if arg.startswith("--"):
			key, value = arg[2:].split("=", 1) if "=" in arg[2:] else (arg[2:], None)
			options[key] = value
	return options

def is_float(value: str):
	try:
		float(value)
		return True
	except:
		return False

def is_bool(value: str):
	try:
		bool(value)
		return True
	except:
		return False