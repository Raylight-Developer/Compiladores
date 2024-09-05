package com.compiler.Types;

import java.util.*;

public class Class {
	public String ID;
	public String parent;
	public Function constructor;
	public List<Function> function_members;
	public List<Variable> variable_members;
}