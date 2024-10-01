from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import traceback
import antlr4
import sys
import os
import re

from typing import List, Dict, Tuple, Set, Union, Generic, TypeVar, Any
from enum import Enum

from antlr4.tree.Tree import *
from antlr4 import *

R      = "FAILURE"
G      = "SUCCESS"

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