from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import sys
import os

from graphviz import Digraph
from antlr4 import *
from typing import *

RESET  = "</span>"
R      = "<span style = 'color:rgb(250,50,50);' >"
G      = "<span style = 'color:rgb(50,250,50);' >"
B      = "<span style = 'color:rgb(50,50,250);' >"
TEST   = "<span style = 'color:rgb(100,100,100);' >"