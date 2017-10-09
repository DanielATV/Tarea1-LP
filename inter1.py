import re
import operator

ops= {"+": operator.add, "-": operator.sub} # ops["+"](1,1) = 1 + 1 

Variables = dict()  # Key -> nombre variable ; Value -> lista[tipo, valor] 
Funciones = dict()  # Key -> nombre funcion; Value: lista[tipo variable entrada,tipo variable salida,sentencias]
estate = dict()
In_Fun = False
In_While = False
LET = "let mut"
WHILE = "while"
IF = "if"
ELSE = "else"
ELSE_IF = "else if"
RETURN = "return"
FN = "fn"
SENT = ";"
END = "}"
PRINT = "println!"


#Declaracion de variables

var_val = re.compile("let mut\s*(\w*)\s*:\s*(i16|i32|f64)\s*=\s*([0-9]+(.[0-9]+)?);")
var_var = re.compile("let mut\s*(\w*)\s*:\s*(i16|i32|f64)\s*=\s*([A-z]+);")
var_func = re.compile("let mut\s(\w*)\s:\s(i16|i32|f64)\s=\s(\w*)\((\w+)\);")
var_op = re.compile("let mut\s*(\w*)\s*:\s*(i16|i32|f64)\s*=\s*([0-9]+)\s*(\+|\-)\s*([0-9]+);")
var_op_sc = re.compile("let mut\s*(\w*)\s*:\s*(i16|i32|f64)\s*=\s*(\w*)\s*(\+|\-)\s*(\w*)\s*;")
var_op_cast_cast = re.compile("let mut\s*(\w*)\s*:\s*(i16|i32|f64)\s*=\s*\((\w*)\s*as\s*(i16|i32|f64)\)\s*(\+|\-)\s*\((\w*)\s*as\s*(i16|i32|f64)\);")
var_op_valcasti_variable = re.compile("let mut\s*(\w*)\s*:\s*(i16|i32|f64)\s*=\s*\((\w*)\s*as\s*(i16|i32|f64)\)\s*(\+|\-)\s*([A-z]+);")
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
sent_op_doublecast = re.compile("(\w+)\s*=\s*\((\w*)\s*as\s*(i16|i32|f64)\)\s*(\+|\-)+\s*\((\w*)\sas\s*(i16|i32|f64)\);")

#If & While

while_sent = re.compile(r"while\s(\w*)\s(<=|>=|>|<|=)\s(\w*)\s*{")
if_sent = re.compile("if\s(\w*)\s(<=|>=|>|<|=)\s(\w*)\s{")
end_while = end_func = end_if = re.compile("}")
elseif_sent = re.compile("} else if (([A-z]) (<=|>=|>|<|=) ([A-z]+|[0-9]+)) {")
else_sent= re.compile("} else {")

#Retornos

retorno_var_val = re.compile("return\s(\w*);")
retorno_opsc = re.compile("return\s((\w*|\d*)\s*(\+|\-)\s(\w*|\d*));")
retorno_ci = re.compile("return\s(\((\w*)\s*as\s*(i16|i32|f64)\)\s*(\+|\-)\s*(\w*));")
retorno_cd = re.compile("return\s(\w*)\s*(\+|\-)\s\((\w*)\s*as\s*(i16|i32|f64)\);")
retorno_dc = re.compile("return\s\((\w+)\s*as\s*(i16|i32|f64)\)\s*(\+|\-)\s*\((\w*)+\sas\s*(i16|i32|f64)\);")

#Funciones

func = re.compile("fn\s*(\w*)\((\w)\s*:\s*(i16|i32|f64)\)\s*->\s*(i16|i32|f64)\s*{")
func_main = re.compile("fn\s*main\(\)\s*{")

#Print

println = re.compile("println!\((\w+)\);")

# Varible
ind_var = re.compile("[A-z]+")

# Digito
ind_dig = re.compile("[0-9]+")


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
	elif ELSE_IF in line:
		return ELSE_IF
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
"""
ret_fun(line,tipo,VARS) : 
Inputs:
(string): La linea que se esta leyendo del archivo.
(string): El tipo de dato que se retorna
(diccionario): El diccionario de las variables del enterno en que se trabaja.

Outputs:
(string): El resultado de la operacion en forma de string

"""

	
def ret_fun(line,tipo,VARS):

	obj = retorno_var_val.match(line)
	if obj:
		var = obj.group(1)
		if var.isdigit():
			return var
		else:
			var = VARS[var]
			return var
	obj = retorno_opsc.match(line)
	if obj:
		return operation(line,VARS)
	obj = retorno_cd
	if obj:
		return operation(line,VARS)
	obj = retorno_ci
	if obj:
		return operation(line,VARS)
	obj = retorno_dc
	if obj:
		return operation(line,VARS)

"""
declaration(line,VARS) : 
Inputs:
(string): La linea que se esta leyendo del archivo.
(diccionario): El diccionario de las variables del enterno en que se trabaja.

Outputs:
(None): En el caso que haya error de tipo.
(diccionario): El diccionario actualizado con las declaraciones.

"""
def declaration(line,VARS): # En Desarrollo
	obj = var_val.search(line)
	if(obj):

		if obj.group(2) in ["i32","i16"]:

			up_val(obj.group(1),int(float(obj.group(3))),obj.group(2),VARS)

			return VARS
		else:

			up_val(obj.group(1),float(obj.group(3)),obj.group(2),VARS)

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

		if compar_types(obj.group(3),obj.group(5),VARS):
			if get_val_type(obj.group(3).VARS) in ["i32","i16"]:
				valor = ops[obj.group(4)](float(obj.group(3)),float(obj.group(5)))
				up_val(obj.group(1),int(valor),obj.group(2),VARS)
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

		
			if get_val_type(obj.group(3),VARS) in ["i32","i16"]:

				valor = ops[obj.group(5)](float(get_val_value(obj.group(3),VARS)),float(get_val_value(obj.group(6),VARS)))
				up_val(obj.group(1),int(valor),obj.group(2),VARS)
		
			else:
				valor = ops[obj.group(5)](float(get_val_value(obj.group(3),VARS)),float(get_val_value(obj.group(6),VARS)))
				up_val(obj.group(1),valor,obj.group(2),VARS)
		else:
			print "Error Tipo"
			return None
		
	obj = var_op_valcasti_variable.search(line)
	if obj:


		if obj.group(4) == get_val_type(obj.group(6),VARS):

			if obj.group(2) in ["i32","i16"]:				

				valor = ops[obj.group(5)](float(get_val_value(obj.group(3),VARS)),float(get_val_value(obj.group(6),VARS)))
				up_val(obj.group(1),int(valor),obj.group(2),VARS)
				return  VARS
			else:
				valor = ops[obj.group(5)](float(get_val_value(obj.group(3),VARS)),float(get_val_value(obj.group(6),VARS)))
				up_val(obj.group(1),valor,obj.group(2),VARS)
				return  VARS
		else:
			print "Error tipo"
			return None



	obj = var_op_valcasti_valor.search(line)
	if obj:
	
		if obj.group(2) in ["i32","i16"]:

			valor = ops[obj.group(5)](float(get_val_value(obj.group(3),VARS)),float(obj.group(6)))
			up_val(obj.group(1),int(valor),obj.group(2),VARS)
			return  VARS

		else:
			valor = ops[obj.group(5)](float(get_val_value(obj.group(3),VARS)),float(obj.group(6)))
			up_val(obj.group(1),valor,obj.group(2),VARS)
			return  VARS

	obj = var_op_valcastd_valor.search(line)
	if obj:

		if obj.group(2) in ["i32","i16"]:

			valor = ops[obj.group(5)](float(obj.group(3)),float(get_val_value(obj.group(6),VARS)))
			up_val(obj.group(1),int(valor),obj.group(2),VARS)
			return  VARS

		else:

			valor = ops[obj.group(5)](float(obj.group(3)),float(get_val_value(obj.group(6),VARS)))
			up_val(obj.group(1),valor,obj.group(2),VARS)
			return  VARS

	obj = var_op_valcastd_variable.search(line)

	if obj:

		if obj.group(6) == get_val_type(obj.group(3),VARS):

			if obj.group(2) in ["i32","i16"]:	

				valor = ops[obj.group(4)](float(get_val_value(obj.group(3),VARS)),float(get_val_value(obj.group(5),VARS)))
				up_val(obj.group(1),int(valor),obj.group(2),VARS)
				return  VARS

			else:
				valor = ops[obj.group(4)](float(get_val_value(obj.group(3),VARS)),float(get_val_value(obj.group(5),VARS)))
				up_val(obj.group(1),valor,obj.group(2),VARS)
				return  VARS

		else:
			print "Error de tipo"
			return None

	obj = var_func.search(line)

	if obj:


		variable = obj.group(1)
		tipo =  obj.group(2)
		nombre = obj.group(3)
		argumento = obj.group(4)

		retorno = leedor_fun(nombre,argumento,VARS)
		print retorno
		up_val(variable,retorno,tipo,VARS)
		return VARS

	obj = var_op_sc.search(line)
	if obj:


		if compar_types(obj.group(3),obj.group(5),VARS):
			
			if get_val_type(obj.group(3),VARS) in ["i32","i16"]:

				valor = ops[obj.group(4)](float(get_val_value(obj.group(3),VARS)),float(get_val_value(obj.group(5),VARS)))
				up_val(obj.group(1),int(valor),obj.group(2),VARS)

				return VARS

			else :

				valor = ops[obj.group(4)](float(get_val_value(obj.group(3),VARS)),float(get_val_value(obj.group(5),VARS)))
				up_val(obj.group(1),valor,obj.group(2),VARS)

				return VARS

		else:
			print "Error de tipo"
			return None
		

	else:
		print "Error"
		return None


"""
nombre_funcion(parametros) : breve descripcion
Inputs:
(tipo dato) descripcion

Outputs:
(tipo dato) descripcion

"""
def bool(var,cond,var2,VARS):
	if var2.isdigit():
		var = get_val_value(var,VARS)
		var2 = int(var2)
	elif compar_types(var,var2,VARS) == True:
		var = get_val_value(var,VARS)
		var2 = get_val_value(var2,VARS)
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


"""
nombre_funcion(parametros) : breve descripcion
Inputs:
(tipo dato) descripcion

Outputs:
(tipo dato) descripcion

"""

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
					return VARS
				elif op == "-":
					VARS[obj.group(1)][0] = str(int(var) - int(var2))
					return VARS
			elif var.isdigit():
				if not compar_types(obj.group(1),var2):
					print("Error de tipos")
					return None
				var2 = get_val_value(var2,VARS)
				if op == "+":
					VARS[obj.group(1)][0] = str(int(var) + var2)
					return VARS
				else:
					VARS[obj.group(1)][0] = str(int(var) - var2)
					return VARS
			elif var2.isdigit():
				if compar_types(obj.group(1),var,VARS):
					pass
				else:
					print("Error de tipos")
					return None
				var = get_val_value(var,VARS)
				if op == "+":
					VARS[obj.group(1)][0] = str(var + int(var2))
					return VARS
				else:
					VARS[obj.group(1)][0] = str(var - int(var2))
					return VARS
			else:
				if not compar_types(var,var2,VARS):
					print("Error de tipos")
					return None
				if not compar_types(obj.group(1),var,VARS):
					print("Error de tipos")
					return None
				var = get_val_value(var,VARS)
				var2 = get_val_value(var2,VARS)
				if op == "+":
					VARS[obj.group(1)][0] = str(var + var2)
					return VARS
				else:
					VARS[obj.group(1)][0] = str(var - var2)
					return VARS
		else:
			print("Variable "+obj.group(1)+" no declarada")
			return None

	obj = sent_func.match(line)

	if (obj):# Falta La funcion que ejecuta las funciones para llamarla aca
		pass 

	obj = sent_val.match(line)
	if (obj):
		var = obj.group(1)
		val = obj.group(2)
		if var not in VARS.keys():
			print("Variable "+var+" no definida")
			return None
		VARS[var][0] = val
		return VARS

	obj = sent_var.match(line)
	if (obj):
		var = obj.group(1)
		var2 = obj.group(2)
		if var in VARS.keys() and var2 in VARS.keys():
			if compar_types(var,var2):
				VARS[var][0] = get_val_value(var2)
			else:
				print("Error de Tipo")
				return None
		else:
			print("Variable o variables no definidas")
	
	obj = sent_op_cast.match(line)
	if (obj):
		var = obj.group(1)
		var2 = obj.group(2)
		cast = obj.group(3)
		if var not in VARS.keys():
			print("Variable "+var+" no definida")
			return None
		if cast == VARS[var][1]:
			VARS[var][0] = var2
		else:
			print("Error de Tipo")
			return None

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
					return VARS
				else:
					VARS[var][0] = str(int(var2) - int(var3))
					return VARS
		if cast == VARS[var2][1] and cast == VARS[var][1]:
			if op == "+":
				VARS[var][0] = str(int(VARS[var3][0]) + int(VARS[var2][0]))
				return VARS
			else:
				VARS[var][0] = str(int(VARS[var2][0]) - int(var3))
				return VARS
		else:
			print("Error de Tipo")
			return None

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
					return VARS
				else:
					VARS[var][0] = str(int(VARS[var2][0]) - int(var3))
					return VARS
		if cast == VARS[var][1]:
			if op == "+":
				VARS[var][0] = str(int(VARS[var3][0]) + int(VARS[var2][0]))
				return VARS
			else:
				VARS[var][0] = str(int(VARS[var2][0]) - int(VARS[var3][0]))
				return VARS
		else:
			print("Error de Tipo")
			return None
	obj = sent_op_doublecast.match(line)
	if (obj):
		var = obj.group(1)
		var1 = obj.group(2)
		cast1 = obj.group(3)
		op = obj.group(4)
		var2 = obj.group(5)
		cast2 = obj.group(6)
		if(cast1 == cast2):
			if cast1 in ["i16","i32"] and "f64" in VARS[var1]:
				var1 = float_to_int(var1,VARS)
			if cast2 in ["i16","i32"] and VARS[var2][1] == "f64":
				var2 = float_to_int(var2,VARS)
			if cast1 == "f64" and VARS[var1][1] in ["i16","i32"]:
				var1 = int_to_float(var1,VARS)
			if cast2 == "f64" and VARS[var2][1] in ["i16","i32"]:
				var2 = int_to_float(var2,VARS)
			if VARS[var][1] == cast1:
				if cast1 == "f64" and op == "+":
					VARS[var][0] = str(float(var1) + float(var2))
				if cast1 == "f64" and op == "-":
					VARS[var][0] = str(float(var1) - float(var2))
				if cast1 in ["i16","i32"] and op == "+":
					VARS[var][0] = str(int(VARS[var1][0]) + int(VARS[var2][0]))
				if cast1 in ["i16","i32"] and op == "-":
					VARS[var][0] = str(int(VARS[var1][0]) - int(VARS[var2][0]))
			else:
				print("Error de Tipo")
				return None
			return VARS
		else:
			print("Error de Tipo")
			return None


def float_to_int(var,VARS):
	var = VARS[var][0].split(".")[0]
	return var

def int_to_float(var,VARS):
	var = VARS[var][0]+".0"
	return var

"""
if_exec(line,fp,VARS) : Evalua y ejecuta if, else if y else dentro del codigo fuente. 
Inputs:

(string): Linea que lee del archivo.
(file pointer): Archivo que se esta leyendo.
(dict): Diccionario con las variables del entorno

Outputs:
(dict): Diccionario con las variables de entorno procesadas

"""

def if_exec(line,fp,VARS):
	print("Entrando a if")
	print(line)
	print(VARS)
	llaves_abiertas = 1
	COND = False
	obj = if_sent.match(line)
	if obj:
		var1 = obj.group(1)
		cond = obj.group(2)
		var2 = obj.group(3)
		if bool(var1,cond,var2,VARS) and COND == False:
			COND = True
			for line in fp:
				line = line.strip("\n")
				line = line.strip("\t")
				a = identifier(line)
				if a == SENT:
					VARS = sentence(line,VARS)
				elif a == IF:
					VARS = if_exec(line,fp,VARS)
				elif a == WHILE:
					lista = while_list(line,fp) # Ejecucion de los while
		else:
			llaves_abiertas = 1
			for line in fp:
				line = line.strip("\n")
				line = line.strip("\t")
				if llaves_abiertas == 0:
						break
				if "}" in line:
					llaves_abiertas = llaves_abiertas - 1
					if llaves_abiertas == 0:
						break
				if "{" in line:
					llaves_abiertas = llaves_abiertas + 1			
	obj = elseif_sent.match(line)
	if obj:
		var1 = obj.group(1)
		cond = obj.group(2)
		var2 = obj.group(3)
		print(var1,cond,var2)
		if bool(var1,cond,var2,VARS) and COND == False:
			COND = True
			for line in fp:
				line = line.strip("\n")
				line = line.strip("\t")
				a = identifier(line)
				if a == SENT:
					VARS = sentence(line,VARS)
				elif a == IF:
					VARS = if_exec(line,fp,VARS)
				elif a == WHILE:
					lista = while_list(line,fp)
					## Ejecucion de los while
		else:
			llaves_abiertas = 1
			for line in fp:
				line = line.strip("\n")
				line = line.strip("\t")
				if llaves_abiertas == 0:
						break
				if "}" in line:
					llaves_abiertas = llaves_abiertas - 1
					if llaves_abiertas == 0:
						break
				if "{" in line:
					llaves_abiertas = llaves_abiertas + 1			
	obj = else_sent.match(line)
	if obj:
		if COND == False:
			COND = True
			for line in fp:
				line = line.strip("\n")
				line = line.strip("\t")
				a = identifier(line)
				if a == SENT:
					VARS = sentence(line,VARS)
				elif a == IF:
					VARS = if_exec(line,fp,VARS)
				elif a == WHILE:
					lista = while_list(line,fp) ## Ejecucion de los while
				elif "}" in line:
					break
		else:
			llaves_abiertas = 1
			for line in fp:
				line = line.strip("\n")
				line = line.strip("\t")
				if llaves_abiertas == 0:
						break
				if "}" in line:
					llaves_abiertas = llaves_abiertas - 1
					if llaves_abiertas == 0:
						break
				if "{" in line:
					llaves_abiertas = llaves_abiertas + 1
	return VARS	

"""
Store_fun(line,fp) : Guarda la funcion en un diccionario. 
Inputs:

(string): Linea que lee del archivo.
(file object): Archivo que se esta leyendo.

Outputs:
(tipo dato) descripcion

"""

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
		if llaves_abiertas <= 0:
			break
		if "}" in line:
			llaves_abiertas = llaves_abiertas - 1
		if "{" in line:
			llaves_abiertas = llaves_abiertas + 1
		Funciones[name_func].append(line)
	return True

"""
while_list(line,fp) : Guarda todo el ciclo while en una lista.
Inputs:
(string): Linea que lee dl archivo
(file object): Archivo que se esta leyendo.

Outputs:
(lista) Lista con todas las senticas del while, siendo el primer elemento una tupla con el boleano a evaluar.

"""
def while_list(line,fp):
	obj = while_sent.search(line)
	var1 = obj.group(1)
	cond = obj.group(2)
	var2 = obj.group(3)
	lista = list()
	lista.append((var1,cond,var2))
	llaves_abiertas = 1
	for line in fp:
		
		line = line.strip("\n")
		line = line.strip("\t")
		a = identifier(line)
		
		if llaves_abiertas <= 0:
			break
		if "}" in line:
			llaves_abiertas = llaves_abiertas - 1
		if "{" in line:
			llaves_abiertas = llaves_abiertas + 1
		lista.append(line)
	return lista

"""
nombre_funcion(parametros) : breve descripcion
Inputs:
(tipo dato) descripcion

Outputs:
(tipo dato) descripcion

"""
def up_val(var,valor,tipo,VARS):
	VARS[var] = [valor,tipo]
	return VARS

"""
nombre_funcion(parametros) : breve descripcion
Inputs:
(tipo dato) descripcion

Outputs:
(tipo dato) descripcion

"""
def get_val_type(var,VARS):
	if var not in VARS.keys():
		return None
	else:
		return VARS[var][1]

"""
nombre_funcion(parametros) : breve descripcion
Inputs:
(tipo dato) descripcion

Outputs:
(tipo dato) descripcion

"""
def get_val_value(var,VARS):
		return int(VARS[var][0])
"""
nombre_funcion(parametros) : breve descripcion
Inputs:
(tipo dato) descripcion

Outputs:
(tipo dato) descripcion

"""
def compar_types(var1,var2,VARS): ###
	if VARS[var1][1] == VARS[var2][1]:
		return True
	else:
		return None


"""
nombre_funcion(parametros) : breve descripcion
Inputs:
(tipo dato) descripcion

Outputs:
(tipo dato) descripcion

"""
def cast(var,tipo): ###
	if var not in Variables.keys():
		return False
	Variables[var][1] = tipo



def leedor_fun(nombre,argumento,VARS):
	varibles_fun=dict()

	if argumento in VARS.keys():

		up_val(Funciones[nombre][0][0],VARS[argumento][0],Funciones[nombre][0][1],varibles_fun)

		for sent in Funciones[nombre][1:]:
			return sent_retorno(sent,varibles_fun)
		
	else:
		
		up_val(Funciones[nombre][0][0],argumento,Funciones[nombre][0][1],varibles_fun)

		for sent in Funciones[nombre][1:]:
			return  sent_retorno(sent,varibles_fun)


"""
leedor_while(listawhile,VARS) : Construye el while que se le entrega como lista.
Inputs:
(lista): Lista de todas las sentencias del while.
(diccionario): Diccionario de las variables del entorno.

Outputs:
(None): No retorna parametro.

"""
def exe_while(lista_while,fp,VARS):

	Flag = bool(lista_while[0][0],lista_while[0][1],lista_while[0][2],VARS)
	while Flag:
		for line in lista_while[1:]:
			a = identifier(line)
			if a == SENT:
				VARS = sentence(line,VARS)
				
			elif a == IF:
				VARS = if_exec(line,fp,VARS)

		Flag = bool(lista_while[0][0],lista_while[0][1],lista_while[0][2],VARS)

def println(line,VARS):
	obj = print_ln.match(line)
	var = obj.group(1)
	type_var = VARS[var][1]
	print("El valor es: "+var+". Su tipo es: "+type_var)

def operation(line,VARS):

	obj = retorno_opsc.match(line)
	if (obj):

		if obj.group(2) in VARS.keys():
			var = obj.group(2)
			op = obj.group(3)
			var2 = obj.group(4)
			if var.isdigit() and var2.isdigit():
				if op == "+":
					return str(int(var) + int(var2))
				elif op == "-":
					return str(int(var) - int(var2))
			elif var.isdigit():
				if not compar_types(obj.group(1),var2):
					print("Error de tipos")
					return None
				var2 = get_val_value(var2,VARS)
				if op == "+":
					return str(int(var) + var2)
				else:
					return str(int(var) - var2)
			elif var2.isdigit():
				if compar_types(obj.group(1),var,VARS) == False:
					print("Error de tipos")
					return None
				var = get_val_value(var,VARS)
				if op == "+":
					return str(var + int(var2))
				else:
					return str(var - int(var2))
			else:
				if compar_types(var,var2,VARS) == False:
					print("Error de tipos")
					return None
				if compar_types(obj.group(1),var,VARS) == False:
					print("Error de tipos")
					return None
				var = get_val_value(var,VARS)
				var2 = get_val_value(var2,VARS)
				if op == "+":
					return str(var + var2)
				else:
					return str(var - var2)
		else:
			print("Variable "+obj.group(1)+" no declarada")
			return None

	obj = sent_func.match(line)

	if (obj):# Falta La funcion que ejecuta las funciones para llamarla aca
		pass 

	obj = sent_var.match(line)
	if (obj):

		var = obj.group(1)
		var2 = obj.group(2)
		if var in VARS.keys() and var2 in VARS.keys():
			if compar_types(var,var2):
				return var2
			else:
				print("Error de Tipo")
				return None
		else:
			print("Variable o variables no definidas")
	
	obj = sent_val.match(line)
	if (obj):

		var = obj.group(1)
		val = obj.group(2)
		if var not in VARS.keys():
			print("Variable "+var+" no definida")
			return None
		return val
	
	obj = sent_op_cast.match(line)
	if (obj):

		var = obj.group(1)
		var2 = obj.group(2)
		cast = obj.group(3)
		if var not in VARS.keys():
			print("Variable "+var+" no definida")
			return None
		if cast == VARS[var][1]:
			return var2
		else:
			print("Error de Tipo")
			return None

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
					return str(int(VARS[var3][0]) + int(var2))
				else:
					return str(int(var2) - int(var3))
		if cast == VARS[var2][1] and cast == VARS[var][1]:
			if op == "+":
				return str(int(VARS[var3][0]) + int(VARS[var2][0]))
			else:
				return str(int(VARS[var2][0]) - int(var3))
		else:
			print("Error de Tipo")
			return None

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
					return str(int(VARS[var2][0]) + int(var3))
				else:
					return str(int(VARS[var2][0]) - int(var3))
		if cast == VARS[var][1]:
			if op == "+":
				return str(int(VARS[var3][0]) + int(VARS[var2][0]))
			else:
				return str(int(VARS[var2][0]) - int(VARS[var3][0]))
		else:
			print("Error de Tipo")
			return None
	obj = retorno_dc.match(line)

	if (obj):

		var1 = obj.group(1)
		cast1 = obj.group(2)
		op = obj.group(3)
		var2 = obj.group(4)
		cast2 = obj.group(5)
		if(cast1 == cast2):
			if cast1 in ["i16","i32"] and VARS[var1][1] == "f64":
				var1 = float_to_int(var1,VARS)
			if cast2 in ["i16","i32"] and VARS[var2][1] == "f64":
				var2 = float_to_int(var2,VARS)
			if cast1 == "f64" and VARS[var1][1] in ["i16","i32"]:
				var1 = int_to_float(var1,VARS)
			if cast2 == "f64" and VARS[var2][1] in ["i16","i32"]:
				var2 = int_to_float(var2,VARS)
			if VARS[var][1] == cast1:
				if cast1 == "f64" and op == "+":
					return str(float(var1) + float(var2))
				if cast1 == "f64" and op == "-":
					return str(float(var1) - float(var2))
				if cast1 ["i16","i32"] and op == "+":
					return str(int(var1) + int(var2))
				if cast1 ["i16","i32"] and op == "-":
					return  str(int(var1) - int(var2))
			else:
				print("Error de Tipo")
				return None
		else:
			print("Error de Tipo")
			return None
			
def isfloat(a):
	if "." in a:
		return True
	else:
		return False

def sent_retorno(linea,VARS):

	obj = retorno_opsc.search(linea)

	if obj:

		valor = ops[obj.group(3)](float(obj.group(4)),get_val_value(obj.group(2),VARS))
		return int(valor)




file = open("codigo_rust1.txt", "r")



for line in file: # Considerar hacer un strip "\t" las tabulaciones pueden generar error en los compile
	line = line.strip("\n").strip("\t")



	identificador = identifier(line)
	if identificador == FN:

		if func_main.search(line):
			
			for line in file:
				line = line.strip("\n").strip("\t")

				identificador = identifier(line)
				if identificador == LET:

					estate = declaration(line,Variables)

					if estate == None:
						break
					else:

						Variables = estate

				elif identificador == IF:
					print "if"

				elif identificador == WHILE:

					if while_sent.search(line):
						ciclowhile = while_list(line,file)

						exe_while(ciclowhile,file,Variables)
						#leedor_while(ciclowhile,Variables)





		elif func.search(line):
			store_fun(line,file)

		else:
			print "Error"
			break
			
print Variables
