import re
import operator

ops= {"+": operator.add, "-": operator.sub} # ops["+"](1,1) = 1 + 1 

Variables = dict()  # Key -> nombre variable ; Value -> lista[tipo, valor] 
Funciones = dict()  # Key -> nombre funcion; Value: lista[tipo variable entrada,tipo variable salida,sentencias]
In_Fun = False
In_While = False
LET = "let mut"
WHILE = "while"
IF = "if"
ELSE = "else"
RETURN = "return"
FN = "fn"
SENT = ";"
END = "}"
PRINT = "println!"

#Declaracion de variables

var_val = re.compile("let mut\s*(\w*)\s*:\s*(i16|i32|f64)\s*=\s*([0-9]+(.[0-9]+)?);")
var_var = re.compile("let mut\s*(\w*)\s*:\s*(i16|i32|f64)\s*=\s*([A-z]+);")
var_func = re.compile("let mut\s(\w*)\s:\s(i16|i32|f64)\s=\s(\w*)\((\d)\);")
var_op = re.compile("let mut\s*(\w*)\s*:\s*(i16|i32|f64)\s*=\s*([0-9]+)\s*(\+|\-)\s*([0-9]+);")
var_op_cast_cast = re.compile("let mut\s*(\w*)\s*:\s*(i16|i32|f64)\s*=\s*\((\w*)\s*as\s*(i16|i32|f64)\)\s*(\+|\-)\s*\((\w*)\s*as\s*(i16|i32|f64)\);")
var_op_valcasti_variable = re.compile("let mut\s*(\w*)\s*:\s*(i16|i32|f64)\s*=\s*\((\w*)\s*as\s*(i16|i32|f64)\)\s*(\+|\-)\s([A-z]+);")
var_op_valcasti_valor = re.compile("let mut\s*(\w*)\s*:\s*(i16|i32|f64)\s*=\s*\((\w*)\s*as\s*(i16|i32|f64)\)\s*(\+|\-)\s([0-9]+(.[0-9]+)?);")
var_op_valcastd_variable = re.compile("let mut\s*(\w*)\s*:\s*(i16|i32|f64)\s*=\s*([A-z]+)\s*(\+|\-)\s\((\w*)\s*as\s*(i16|i32|f64)\);")
var_op_valcastd_valor = re.compile("let mut\s*(\w*)\s*:\s*(i16|i32|f64)\s*=\s*([0-9]+(.[0-9]+)?)\s*(\+|\-)\s\((\w*)\s*as\s*(i16|i32|f64)\);")

#Operaciones y Cast

op_sc = re.compile("(\w+|\d+)\s*(\+|\-)\s(\w+|\d+)")
op_cd = re.compile("\((\w*)\s*as\s*(i16|i32|f64)\)\s*(\+|\-)\s*(\w*)")
op_ci = re.compile("(\w*)\s*(\+|\-)\s\((\w*)\s*as\s*(i16|i32|f64)\)")
cast = re.compile("\((\w*)\s*as\s*(i16|i32|f64)\)")

#Sentencias

sent_val = re.compile("(\w*)\s*=\s*(\w*);")
sent_var = re.compile("(\w*)\s*=\s*(\w*);")
sent_func = re.compile("(\w*)+\s*=\s*(\w*)+\((\w*)+\)\s*;")
sent_op = re.compile("(\w*)\s*=\s*(\w*)\s*(\+|\-)+\s*(\w*);")
sent_op_cast = re.compile("(\w*)\s*=\s*\((\w*)\sas\s(i16|i32|f64)\);")
sent_op_valcasti = re.compile("(\w*)\s*=\s*\((\w*)\s*as\s*(i16|i32|f64)\)\s*(\+|\-)\s*(\w*)\s*;")
sent_op_valcastd = re.compile("(\w*)\s*=\s*(\w*)\s*(\+|\-)\s*\((\w*)\s*as\s*(i16|i32|f64)\)\s*;")

#If & While

while_sent = re.compile(r"while\s(\w*)\s(<=|>=|>|<|=)\s(\w*){")
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
fun_main = re.compile(r"fn\smain\(\)\s{")

#Print

println = re.compile("println!\((\w+)\);")

def bool(line,VARS):
	obj = while_sent.match(line)
	if obj:	
		var = obj.group(1)
		cond = obj.group(2)
		var2 = obj.group(3)
	else:
		obj = if_sent.match(line)
		var = obj.group(1)
		cond = obj.group(2)
		var2 = obj.group(3)
	if var2.isdigit():
		var = get_val_value(var,VARS)
		var2 = int(var2)
	elif compar_types(var,var2,VARS) == True:
		var = get_val_value(var,VARS)
		var2 = get_val_value(var2,VARS)
	else:
		print("Error de tipos")
		return False
		
	if cond == "<":
		return var < var2
	elif cond == ">":
		return var > var2
	elif cond == "=":
		return var == var2
	elif cond == ">=":
		return var >= var2
	elif cond == "<=":
		return var <= var2
	else:
		print("Error de Sintaxis")
		return None

def sentence(line,VARS):
	obj = sent_op.match(line)
	if (obj):
		if obj.group(1) in VARS.keys():
			var = obj.group(2)
			op = obj.group(3)
			var2 = obj.group(4)
			if var.isdigit() and var2.isdigit():
				if op == "+":
					VARS[obj.group(1)][0] = str(int(var) + int(var2))
					return True
				elif op == "-":
					VARS[obj.group(1)][0] = str(int(var) - int(var2))
					return True
			elif var.isdigit():
				if not compar_types(obj.group(1),var2):
					print("Error de tipos")
					return False
				var2 = get_val_value(var2)
				if op == "+":
					VARS[obj.group(1)][0] = str(int(var) + var2)
					return True
				else:
					VARS[obj.group(1)][0] = str(int(var) - var2)
					return True
			elif var2.isdigit():
				if compar_types(obj.group(1),var):
					pass
				else:
					print("Error de tipos")
					return False
				var = get_val_value(var)
				if op == "+":
					VARS[obj.group(1)][0] = str(var + int(var2))
					return True
				else:
					VARS[obj.group(1)][0] = str(var - int(var2))
					return True
			else:
				if not compar_types(var,var2):
					print("Error de tipos")
					return False
				if not compar_types(obj.group(1),var):
					print("Error de tipos")
					return False
				var = get_val_value(var)
				var2 = get_val_value(var2)
				if op == "+":
					VARS[obj.group(1)][0] = str(var + var2)
					return True
				else:
					VARS[obj.group(1)][0] = str(var - var2)
					return True
		else:
			print("Variable "+obj.group(1)+" no declarada")
			return False

	obj = sent_func.match(line)

	if (obj):# Falta La funcion que ejecuta las funciones para llamarla aca
		pass 

	obj = sent_var.match(line)
	if (obj):
		var = obj.group(1)
		var2 = obj.group(2)
		if var in VARS.keys() and var2 in VARS.keys():
			if compar_types(var,var2):
				VARS[var][0] = get_val_value(var2)
			else:
				print("Error de Tipo")
				return False
		else:
			print("Variable o variables no definidas")
	
	obj = sent_val.match(line)
	if (obj):
		var = obj.group(1)
		val = obj.group(2)
		if var not in VARS.keys():
			print("Variable "+var+" no definida")
			return False
		VARS[var] = int(val)
		return True
	
	obj = sent_op_cast.match(line)
	if (obj):
		var = obj.group(1)
		var2 = obj.group(2)
		cast = obj.group(3)
		if var not in VARS.keys():
			print("Variable "+var+" no definida")
			return False
		if cast == VARS[var][1]:
			VARS[var][0] = var2
		else:
			print("Error de Tipo")
			return False

	obj = sent_op_valcastd.match(line)
	if (obj):
		var = obj.group(1)
		var2 = obj.group(2)
		op = obj.group(3)
		var3 = obj.group(4)
		cast = obj.group(5)
		if var2.isdigit():
			if cast == VARS[var][1]:
				if op == "+":
					VARS[var][0] = str(int(VARS[var3][0]) + int(var2))
					return True
				else:
					VARS[var][0] = str(int(var2) - int(var3))
					return True
		if cast == VARS[var2][1] and cast == VARS[var][1]:
			if op == "+":
				VARS[var][0] = str(int(VARS[var3][0]) + int(VARS[var2][0]))
				return True
			else:
				VARS[var][0] = str(int(VARS[var2][0]) - int(var3))
				return True
		else:
			print("Error de Tipo")
			return False

	obj = sent_op_valcasti.match(line)
	if (obj):
		var = obj.group(1)
		var2 = obj.group(2)
		cast = obj.group(3)
		op = obj.group(4)
		var3 = obj.group(5)
		if var3.isdigit():
			if cast == VARS[var][1]:
				if op == "+":
					VARS[var][0] = str(int(VARS[var2][0]) + int(var3))
					return True
				else:
					VARS[var][0] = str(int(VARS[var2][0]) - int(var3))
					return True
		if cast == VARS[var][1]:
			if op == "+":
				VARS[var][0] = str(int(VARS[var3][0]) + int(VARS[var2][0]))
				return True
			else:
				VARS[var][0] = str(int(VARS[var2][0]) - int(VARS[var3][0]))
				return True
		else:
			print("Error de Tipo")
			return False

def store_fun(line,fp):
	obj = func_main.match(line)
	if obj:
		return None
	obj = func.match(line)
	name_func = obj.group(1)
	var_func = obj.group(2)
	type_in = obj.group(3)
	type_out = obj.group(4)
	llaves_abiertas = 1
	Funciones[name_func] = [(var_func,type_in,type_out)]
	for line in fp:
		line = line.strip("\n")
		line = line.strip("\t")
		a = identifier(line)
		print(llaves_abiertas)
		if llaves_abiertas <= 0:
			break
		if "}" in line:
			llaves_abiertas = llaves_abiertas - 1
		if "{" in line:
			llaves_abiertas = llaves_abiertas + 1
		Funciones[name_func].append(line)
	return True

def up_val(var,valor,tipo,VARS):
	VARS[var] = [valor,tipo]
	return VARS

def get_val_type(var,VARS):
	if var not in VARS.keys():
		return None
	else:
		return VARS[var][1]

def get_val_value(var,VARS):
	if var not in VARS.keys():
		return None
	else:
		return int(VARS[var][0])

def compar_types(var1,var2,VARS): ###
	if VARS[var1][1] == VARS[var2][1]:
		return True
	else:
		return False

def declaration(line,VARS): # En Desarrollo
	obj = var_val.search(line)
	if(obj):
		up_val(obj.group(1),obj.group(3),obj.group(2),VARS)
		return VARS
	obj = var_var.search(line)
	if(obj):
		lista = Variables[obj.group(3)]
		if obj.group(2) == lista[1]:
			up_val(obj.group(1),lista[0],obj.group(2),VARS)
			return VARS
		else:
			print "Error de tipo"#falta hacer que termine el programa
			return None

	obj = var_op.search(line)
	if obj:
		print "operacion"
		if compar_types(obj.group(3),obj.group(5),VARS):
			if get_val_type(obj.group(3).VARS) == ("i32" or "i16"):
				valor = ops[obj.group(4)](int(obj.group(3)),int(obj.group(5)))
				up_val(obj.group(1),valor,obj.group(2),VARS)
				return VARS
			else:
				valor = ops[obj.group(4)](float(obj.group(3)),float(obj.group(5)))
				up_val(obj.group(1),valor,obj.group(2),VARS)
				return  VARS


		else:
			print "Error de tipo"
			return None

	obj = var_op_cast_cast.search(line)
	if obj:

		if compar_types(obj.group(3),obj.group(6),VARS):

		
			if get_val_type(obj.group(3),VARS) == ("i32" or "i16"):

				valor = ops[obj.group(5)](int(float(get_val_value(obj.group(3),VARS))),int(float(get_val_value(obj.group(6),VARS))))
				up_val(obj.group(1),valor,obj.group(2),VARS)
		
			else:
				valor = ops[obj.group(5)](float(get_val_value(obj.group(3),VARS)),float(get_val_value(obj.group(6),VARS)))
				up_val(obj.group(1),valor,obj.group(2),VARS)
		else:
			print "Error Tipo"
		
	#Faltan ver los checkeos de tipo
	obj = var_op_valcasti_variable.search(line)
	if obj:

		valor = ops[obj.group(5)](int(float(get_val_value(obj.group(3)))),int(float(get_val_value(obj.group(6)))))
		up_val(obj.group(1),valor,obj.group(2),VARS)



	obj = var_op_valcasti_valor.search(line)
	if obj:

		valor = ops[obj.group(5)](int(float(get_val_value(obj.group(3)))),int(float(obj.group(6))))
		up_val(obj.group(1),valor,obj.group(2),VARS)

	obj = var_op_valcastd_valor.search(line)
	if obj:

		valor = ops[obj.group(5)](int(float(obj.group(3))),int(float(get_val_value(obj.group(6),VARS))))
		up_val(obj.group(1),valor,obj.group(2),VARS)

	obj = var_op_valcastd_variable.search(line)

	if obj:

		valor = ops[obj.group(4)](int(float(get_val_value(obj.group(3),VARS))),int(float(get_val_value(obj.group(5),VARS))))
		up_val(obj.group(1),valor,obj.group(2),VARS)



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
		return SENT

def leedor_if():
	i = 0
	while True:
		line = file.readline().strip("\n")
		if end_if.search(line) and len(line) == 2:
			break
		elif elseif_sent.search(line):#falta probarlo
			print "else if"
		elif else_sent.search(line):
			print "else"
		'''
		elif declarar
		elif asginar
		elif operaciones
		elif pr1nt
		elif funcion
		elif retorn
		elif while
		elif if
		'''


		i += 1
	print i

def leedor_while():
	i = 0
	while True:
		line = file.readline().strip("\n")
		if end_while.search(line) and len(line) == 2:
			break

		'''
		elif declarar
		elif asginar
		elif operaciones
		elif pr1nt
		elif funcion
		elif retorn
		elif while
		elif if
		''' 
		i += 1
	print i

file = open("codigo_rust1.txt", "r")

while True: # Considerar hacer un strip "\t" las tabulaciones pueden generar error en los compile
	line = file.readline().strip("\n")
	if line == "":
		break
	if len(line)==1 and line != "}":
		continue
	identificador = identifier(line)
	if identificador == FN:
		if fun_main.search(line):
			continue
		else:
			print "funcion"
	elif identificador == LET:

		declaration(line,Variables)

	elif identificador == IF:
		print "if"
		if if_sent.search(line):
			leedor_if()
	elif identificador == WHILE:
		print "while"
		if while_sent.search(line):
			leedor_while()

print Variables
