import re

Variables = dict()  # Key -> Variable ; Value -> [valor, tipo] 
Funciones = dict()  #
In_Fun = False
In_While = False
LET = "let mut"
WHILE = "while"
IF = "if"
ELSE = "else"
RETURN = "return"
FN = "fn"
END = "}"
PRINT = "println!"

#Declaracion de variables

var_val = re.compile("let mut\s*(\w*)\s*:\s*(i16|i32|f64)\s*=\s*(\d*)")
var_var = re.compile("let mut\s*(\w*)\s*:\s*(i16|i32|f64)\s*=\s*(\w*)")
var_func = re.compile("let mut\s(\w*)\s:\s(i16|i32|f64)\s=\s(\w*)\((\d)\);")
var_op = re.compile("let mut\s*(\w*)\s*:\s*(i16|i32|f64)\s*=\s*(\w*)\s*(\+|\-)\s*(\w);")
var_op_cast_cast = re.compile("let mut\s*(\w*)\s*:\s*(i16|i32|f64)\s*=\s*\((\w*)\s*as\s*(i16|i32|f64)\)\s*(\+|\-)\s*\((\w*)\s*as\s*(i16|i32|f64)\)")
var_op_valcasti = re.compile("let mut\s*(\w*)\s*:\s*(i16|i32|f64)\s*=\s*\((\w*)\s*as\s*(i16|i32|f64)\)\s*(\+|\-)\s(\w*)")
var_op_valcastd = re.compile("let mut\s*(\w*)\s*:\s*(i16|i32|f64)\s*=\s*(\w*)\s*(\+|\-)\s\((\w*)\s*as\s*(i16|i32|f64)\)")

#Operaciones y Cast

op_sc = re.compile("(\w*|\d*)\s*(\+|\-)\s(\w*|\d*)")
op_cd = re.compile("\((\w*)\s*as\s*(i16|i32|f64)\)\s*(\+|\-)\s*(\w*)")
op_ci = re.compile("(\w*)\s*(\+|\-)\s\((\w*)\s*as\s*(i16|i32|f64)\)")
cast = re.compile("\((\w*)\s*as\s*(i16|i32|f64)\)")

#If & While

while_sent = re.compile("while\s(\w*)\s(<=|>=|>|<|=)\s(\w*)\s{")
if_sent = re.compile("if\s(\w*)\s(<=|>=|>|<|=)\s(\w*)\s{")
end_while = end_func = end_if = re.compile("}")
elseif_sent = re.compile("} else if (([A-z]) (<=|>=|>|<|=) ([A-z]+|[0-9]+)) {")
else_sent= re.compile("} else {")

#Retornos

retorno_var_val = re.compile("return\s(\w*);")
retorno_opsc = re.compile("return\s((\w*|\d*)\s*(\+|\-)\s(\w*|\d*));")
retorno_ci = re.compile("return\s(\((\w*)\s*as\s*(i16|i32|f64)\)\s*(\+|\-)\s*(\w*));")
retorno_cd = re.compile("return\s(\w*)\s*(\+|\-)\s\((\w*)\s*as\s*(i16|i32|f64)\);")

#Funciones

func = re.compile("fn\s(\w*)\((\w):\s(i16|i32|f64)\)\s->\s(i16|i32|f64){")

#Print

println = re.compile("println!\((\w+)\);")

def up_val(var,valor,tipo):
	Variables[var] = [valor,tipo]

def get_val_type(var):
	if var not in Variables.keys():
		return None
	else:
		return Variables[var][1]

def get_val_value(var):
	if var not in Variables.keys():
		return None
	else:
		return Variables[var][0]

def compar_types(var1,var2): ###
	if var1 not in Variables.keys() or var2 not in Variables.keys():
		return False
	if get_val_type(var1) == get_val_type(var2):
		return True
	else:
		return False

def cast(var,tipo): ###
	if var not in Variables.keys():
		return False
	Variables[var][1] = tipo

"""
identifier(line) : Busca que es lo que se intenta hacer, por ejemplo, definir una funcion.
Inputs:
(string) La linea que se esta leyendo del archivo.

Outputs:
(string) El match que tuvo.
"""
def identifier(line):
	if LET in line:
		return LET
	elif WHILE in line:
		return WHILE
	elif IF in line:
		return IF
	elif ELSE in line:
		return ELSE
	elif RETURN in line:
		return RETURN
	elif FN in line:
		return FN
	elif END in line:
		return END
	elif PRINT in line:
		return PRINT
	else:
		return "Statment"


file = open("codigo_rust.txt", "r")

for line in file:
	line = line.strip("\n")
	if len(line)==1 and line != "}":
		continue
	a = identifier(line)
	print a
