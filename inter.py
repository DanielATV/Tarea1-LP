import re

Variables = dict()  # Key -> Variable ; Value -> [valor, tipo] 
Funciones = dict()  #
In_Fun = None
In_While = None
Cond_Done = False
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


var_val = re.compile("let mut\s*(\w+)\s*:\s*(i16|i32|f64)\s*=\s*(\d*|\d*\.\d*);")
var_var = re.compile("let mut\s*(\w+)\s*:\s*(i16|i32|f64)\s*=\s*(\w+);")
var_func = re.compile("let mut\s*(\w*)\s*:\s*(i16|i32|f64)\s*=\s*(\w*)\((\w*)\);")
var_op = re.compile("let mut\s*(\w+)\s*:\s*(i16|i32|f64)\s*=\s*(\w+)\s*(\+|\-)\s*(\w+);")
var_op_cast = re.compile("let mut\s*(\w+)\s*:\s*(i16|i32|f64)\s*=\s*(\w*)\s*(\+|\-)\s*\((\w*)\s*as\s*(i16|i32|f64)\);")
var_op_valcasti = re.compile("let mut\s*(\w*)\s*:\s*(i16|i32|f64)\s*=\s*\((\w*)\s*as\s*(i16|i32|f64)\)\s*(\+|\-)\s(\w*);")
var_op_valcastd = re.compile("let mut\s*(\w*)\s*:\s*(i16|i32|f64)\s*=\s*(\w*)\s*(\+|\-)\s\((\w*)\s*as\s*(i16|i32|f64)\);")
var_op_cast_cast = re.compile("let mut\s*(\w*)\s*:\s*(i16|i32|f64)\s*=\s*\((\w*)\s*as\s*(i16|i32|f64)\)\s*(\+|\-)\s*\((\w*)\s*as\s*(i16|i32|f64)\)\s*;")
sent_val = re.compile("(\w*)\s*=\s*(\w*);")
obj_bool = re.compile("(\w*)\s*(<|>|=|>=|<=)\s*(\w*)")
sent_var = re.compile("(\w*)\s*=\s*(\w*);")
sent_func = re.compile("(\w*)\s*=\s*(\w*)\((\w*)\)\s*;")
sent_op = re.compile("(\w*)\s*=\s*(\w*)\s*(\+|\-)+\s*(\w*);")
sent_op_cast = re.compile("(\w*)\s*=\s*\((\w*)\sas\s(i16|i32|f64)\);")
sent_op_valcasti = re.compile("(\w*)\s*=\s*\((\w*)\s*as\s*(i16|i32|f64)\)\s*(\+|\-)\s*(\w*)\s*;")
sent_op_valcastd = re.compile("(\w*)\s*=\s*(\w*)\s*(\+|\-)\s*\((\w*)\s*as\s*(i16|i32|f64)\)\s*;")
sent_op_doublecast = re.compile("(\w+)\s*=\s*\((\w*)\s*as\s*(i16|i32|f64)\)\s*(\+|\-)+\s*\((\w*)\sas\s*(i16|i32|f64)\);")
op_sc = re.compile("(\w*|\d*)\s*(\+|\-)\s*(\w*|\d*)")
op_cd = re.compile("\((\w*)\s*as\s*(i16|i32|f64)\)\s*(\+|\-)\s*(\w*)")
op_ci = re.compile("(\w*)\s*(\+|\-)\s\((\w*)\s*as\s*(i16|i32|f64)\)")
op_func_de = re.compile("(\w*)\s*=\s*(\w*)\s*(\+|\-)\s*(\w*)\((\w*)\)\s*;")
op_func_iz = re.compile("(\w*)\s*=\s*(\w*)\((\w*)\)\s*(\+|\-)\s*(\w*);")
op_func_do = re.compile("(\w*)\s*=\s*(\w*)\((\w*)\)\s*(\+|\-)\s*(\w*)\((\w*)\)\s*;")
cast = re.compile("\((\w*)\s*as\s*(i16|i32|f64)\)")
while_sent = re.compile("while\s(\w*)\s*(<|>|=|>=|<=)\s*(\w*)\s*{")
if_sent = re.compile("if\s(\w*)\s*(<|>|=|>=|<=)\s*(\w*)\s*{")
elseif_sent = re.compile("} else if ([A-z]) (<=|>=|>|<|=) ([A-z]+|[0-9]+) {")
else_sent= re.compile("}\s*else\s*{")
end_while = end_func = end_if = re.compile("}")
retorno_var_val = re.compile("return\s(\w*);")
retorno_opsc = re.compile("return\s(\w*|\d*)\s*(\+|\-)\s(\w*|\d*);")
retorno_ci = re.compile("return\s(\((\w*)\s*as\s*(i16|i32|f64)\)\s*(\+|\-)\s*(\w*));")
retorno_cd = re.compile("return\s(\w*)\s*(\+|\-)\s\((\w*)\s*as\s*(i16|i32|f64)\);")
retorno_dc = re.compile("return\s\((\w+)\s*as\s*(i16|i32|f64)\)\s*(\+|\-)\s*\((\w*)+\sas\s*(i16|i32|f64)\);")
func = re.compile("fn\s*(\w*)\((\w*):\s(i16|i32|f64)+\)\s*->\s*(i16|i32|f64)+{")
func_main = re.compile("fn main\(\)\s*{")
print_ln = re.compile("println!\s*\((\w+)\);")

def if_exec_static(line,lista,VARS):
	llaves_abiertas = 1
	COND = False
	obj = if_sent.match(line)
	if obj and not COND:
		boolean = bool(obj.group(1),obj.group(2),obj.group(3),VARS)
		if boolean:
			COND == True
			while len(lista) > 0:
				lista.pop(0)
				print(lista)
				line = lista[0]
				line = line.strip("\n")
				line = line.strip("\t")
				a = identifier(line)
				if llaves_abiertas == 0:
					break
				if a == SENT:
					lista.pop(0)
					VARS = sentence(line,VARS)
				if a == IF:
					VARS,lista = if_exec_static(line,lista,VARS)
				if a == WHILE:
					lista_while = while_list_static(line,lista)
					VARS,lista = exe_while_static(lista_while,lista,VARS)
				if a == END:
					llaves_abiertas = llaves_abiertas - 1
					lista.pop(0)
				if llaves_abiertas == 0:
					break
		else:
			lista.pop(0)
			while len(lista) > 0:
				line = lista[0]
				line = line.strip("\n")
				line = line.strip("\t")
				a = identifier(line)
				print(llaves_abiertas)
				if llaves_abiertas == 0:
					break
				if "{" in line and a == END:
					lista.pop(0)
				elif "{" in line:
					llaves_abiertas = llaves_abiertas + 1
					lista.pop(0)
				elif a == END:
					llaves_abiertas = llaves_abiertas - 1
					lista.pop(0)
				else:
					lista.pop(0)
				if llaves_abiertas == 0:
					break
	
	obj = elseif_sent.match(line)
	if obj and not COND:
		boolean = bool(obj.group(1),obj.group(2),obj.group(3),VARS)
		if boolean:
			COND == True
			while len(lista) > 0:
				line = lista[0]
				line = line.strip("\n")
				line = line.strip("\t")
				a = identifier(line)
				if a == SENT:
					VARS = sentence(line,VARS)
					lista.pop(0)
				if a == IF:
					VARS,lista = if_exec_static(line,lista,VARS)
				if a == WHILE:
					lista_while = while_list_static(line,lista)
					VARS,lista = exe_while_static(lista_while,lista,VARS)
				if a == END:
					llaves_abiertas = llaves_abiertas - 1
					lista.pop(0)
				if llaves_abiertas == 0:
					break
		else:
			while len(lista) > 0:
				line = lista[0]
				line = line.strip("\n")
				line = line.strip("\t")
				a = identifier(line)
				if "{" in line and a == END:
					lista.pop(0)
				elif "{" in line:
					llaves_abiertas = llaves_abiertas + 1
					lista.pop(0)
				elif a == END:
					llaves_abiertas = llaves_abiertas - 1
					lista.pop(0)
				if llaves_abiertas == 0:
					break
		
	obj = else_sent.match(line)
	if obj and not COND:
		while len(lista) > 0:
			line = lista[0]
			line = line.strip("\n")
			line = line.strip("\t")
			a = identifier(line)
			if a == SENT:
				VARS = sentence(line,VARS)
				lista.pop(0)
			if a == IF:
				VARS,lista = if_exec_static(line,lista,VARS)
			if a == WHILE:
				lista_while = while_list_static(line,lista)
				VARS,lista = exe_while(lista_while,lista,VARS)
			if a == END:
				llaves_abiertas = llaves_abiertas - 1
				lista.pop(0)
			if llaves_abiertas == 0:
				break
	return VARS,lista

def while_list_static(line,lista):
	obj = while_sent.match(line)
	var1 = obj.group(1)
	cond = obj.group(2)
	var2 = obj.group(3)
	lista_while = list()
	lista_while.append((var1,cond,var2))
	llaves_abiertas = 1
	print("______________________________")
	print("Creando Lista",lista_while)
	print("______________________________")
	while llaves_abiertas > 0:
		print("Creando Lista",lista_while)
		line = lista[0]
		line = line.strip("\n")
		line = line.strip("\t")
		a = identifier(line)
		if line == "":
			lista.pop(0)
			continue
		if "}" in line and "{" in line:
			lista.pop(0)
			lista_while.append(line)
		elif "}" in line:
			llaves_abiertas = llaves_abiertas - 1
			lista.pop(0)
			lista_while.append(line)
		elif "{" in line:
			llaves_abiertas = llaves_abiertas + 1
			lista_while.append(line)
		else:
			lista.pop(0)
			lista_while.append(line)
		if llaves_abiertas == 0:
			break
	print("______________________________")
	print("Lista Creada",lista_while)
	print("______________________________")
	return lista_while

def exe_while_static(lista_while,lista,VARS):
	Flag = bool(lista_while[0][0],lista_while[0][1],lista_while[0][2],VARS)
	print("While a ejecutar --> ",lista)
	while Flag:
		lista2 = lista
		print("Inicio ciclo while")
		print(VARS, "-->")
		for line in lista_while[1:]:
			line = line.strip("\n")
			line = line.strip("\t")
			print(lista_while)
			a = identifier(line)
			if a == SENT:
				print("While - Sentencia")
				VARS = sentence(line,VARS)
			elif a == IF:
				print("While - If")
				VARS,lista2 = if_exec_static(line,lista2,VARS)
			elif a == WHILE:
				lista_while = while_list_static(line,lista)
				VARS,lista = exe_while_static(lista_while,lista,VARS)
		print("-->",VARS)
		print("Final ciclo while")
		Flag = bool(lista_while[0][0],lista_while[0][1],lista_while[0][2],VARS)
		if Flag == False:
			break
	return VARS,lista

def exe_while(lista_while,fp,VARS):
	Flag = bool(lista_while[0][0],lista_while[0][1],lista_while[0][2],VARS)
	while Flag:
		llaves = 1
		for line in lista_while[1:]:
			print(llaves)
			line = line.strip("\n")
			line = line.strip("\t")
			print(line)
			a = identifier(line)
			if a == SENT:
				print("While - Sentencia")
				VARS = sentence(line,VARS)
				print(VARS)
			elif a == IF:
				print("While - If")
				VARS = if_exec(line,fp,VARS)
				print(VARS)
			elif a == WHILE:
				print(line)
				lista_while2 = while_list(line,fp)
				print("Lista While Anidado --> ",lista_while2)
				print(lista_while)
				VARS = exe_while(lista_while2,fp,VARS)
			elif "}" in line:
				llaves = llaves - 1
			Flag = bool(lista_while[0][0],lista_while[0][1],lista_while[0][2],VARS)
			if Flag == False or llaves == 0:
				break
		Flag = False
	return VARS

def bool(var,cond,var2,VARS):
	if var2.isdigit():
		var = get_val_value(var,VARS)
		var2 = int(var2)
	elif isfloat(var2):
		var = get_val_value(var,VARS)
		var2 = float(var2)
	elif compar_types(var,var2,VARS) == True:
		var = get_val_value(var,VARS)
		var2 = get_val_value(var2,VARS)
	else:
		print("Error Tipo")
		exit(1)
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
		exit(1)

def println(line,VARS):
	obj = print_ln.match(line)
	var = obj.group(1)
	type_var = VARS[var][1]
	print("El valor es: "+var+". Su tipo es: "+type_var)


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

def while_list(line,fp):
	fp2 = fp
	obj = while_sent.match(line)
	var1 = obj.group(1)
	cond = obj.group(2)
	var2 = obj.group(3)
	lista = list()
	lista.append((var1,cond,var2))
	llaves_abiertas = 1
	for line in fp2:
		line = line.strip("\n")
		line = line.strip("\t")
		print("Linea lista: ",line)
		a = identifier(line)
		lista.append(line)
		if llaves_abiertas == 0:
			break
		if line == "":
			continue
		if "}" in line:
			llaves_abiertas = llaves_abiertas - 1
		if "{" in line:
			llaves_abiertas = llaves_abiertas + 1
		if llaves_abiertas == 0:
			break
	return lista

def if_exec(line,fp,VARS):
	print("-------------- Entrando If --------------")
	print(line)
	llaves_abiertas = 1
	COND = True
	obj = if_sent.match(line)
	if obj and COND:
		print("Match con IF")
		boolean = bool(obj.group(1),obj.group(2),obj.group(3),VARS)
		if boolean:
			print("If condicion cumplida")
			COND = False
			for line in fp:
				line = line.strip("\n")
				line = line.strip("\t")
				print (line)
				a = identifier(line)
				if a == IF:
					VARS = if_exec(line,fp,VARS)
				if a == WHILE:
					lista_while = while_list(line,fp)
					VARS = exe_while(lista_while,fp,VARS)
				if a == SENT:
					VARS = sentence(line,VARS)
				if "}" in line:
					llaves_abiertas = llaves_abiertas - 1
					if llaves_abiertas == 0:
						break
				if "{" in line:
					llaves_abiertas = llaves_abiertas + 1
		else:
			print("If condicion NO cumplida")
			for line in fp:
				line = line.strip("\n")
				line = line.strip("\t")
				print (line)
				a = identifier(line)
				if "}" in line:
					llaves_abiertas = llaves_abiertas - 1
					if llaves_abiertas == 0:
						break
				if "{" in line:
					llaves_abiertas = llaves_abiertas + 1
	obj = elseif_sent.match(line)
	if obj:
		print("Match con ELSE IF")
		boolean = bool(obj.group(1),obj.group(2),obj.group(3),VARS)
		if boolean and COND:
			print("ELSE If condicion cumplida")
			COND = False
			llaves_abiertas = 1
			for line in fp:
				line = line.strip("\n")
				line = line.strip("\t")
				print (line)
				a = identifier(line)
				if a == IF:
					VARS = if_exec(line,fp,VARS)
				if a == WHILE:
					lista_while = while_list(line,fp)
					VARS = exe_while(lista_while,fp,VARS)
				if a == SENT:
					VARS = sentence(line,VARS)
				if "}" in line:
					llaves_abiertas = llaves_abiertas - 1
					if llaves_abiertas == 0:
						break
				if "{" in line:
					llaves_abiertas = llaves_abiertas + 1
		else:
			print("ELSE IF condicion NO cumplida")
			for line in fp:
				llaves_abiertas = 1
				line = line.strip("\n")
				line = line.strip("\t")
				print (line)
				a = identifier(line)
				if "}" in line:
					llaves_abiertas = llaves_abiertas - 1
					if llaves_abiertas == 0:
						break
				if "{" in line:
					llaves_abiertas = llaves_abiertas + 1
	obj = else_sent.match(line)
	if obj:
		if COND:
			print("Condicion ELSE Entra")
			for line in fp:
				line = line.strip("\n")
				line = line.strip("\t")
				print (line)
				a = identifier(line)
				if a == IF:
					VARS = if_exec(line,fp,VARS)
				if a == WHILE:
					lista_while = while_list(line,fp)
					VARS = exe_while(lista_while,fp,VARS)
				if a == SENT:
					VARS = sentence(line,VARS)
				if "}" in line:
					llaves_abiertas = llaves_abiertas - 1
					if llaves_abiertas == 0:
						break
				if "{" in line:
					llaves_abiertas = llaves_abiertas + 1
		else:
			print("ELSE Saltado")
			for line in fp:
				llaves_abiertas = 1
				line = line.strip("\n")
				line = line.strip("\t")
				print (line)
				a = identifier(line)
				if "}" in line:
					llaves_abiertas = llaves_abiertas - 1
					if llaves_abiertas == 0:
						break
				if "{" in line:
					llaves_abiertas = llaves_abiertas + 1
	print("-------------- Saliendo If --------------")
	return VARS

def sentence(line,VARS):
	line = line.strip("\t")
	line = line.strip("\n")
	obj = sent_op.match(line)
	if (obj):
		print(VARS)
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
				if not compar_types(obj.group(1),var2,VARS):
					print("Error de tipos")
					return exit(1)
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
					return exit(1)
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
					return exit(1)
				if not compar_types(obj.group(1),var,VARS):
					print("Error de tipos")
					return exit(1)
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
			return exit(1)

	obj = sent_val.match(line)
	if (obj):
		var = obj.group(1)
		val = obj.group(2)
		if var not in VARS.keys():
			print("Variable "+var+" no definida")
			return exit(1)
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
				return exit(1)
		else:
			print("Variable o variables no definidas")
	
	obj = sent_op_cast.match(line)
	if (obj):
		var = obj.group(1)
		var2 = obj.group(2)
		cast = obj.group(3)
		if var not in VARS.keys():
			print("Variable "+var+" no definida")
			return exit(1)
		if cast == VARS[var][1]:
			VARS[var][0] = var2
		else:
			print("Error de Tipo")
			return exit(1)

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
			return exit(1)

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
			else:
				print("Error de Tipo")
				exit(1)
		if cast == VARS[var][1] and cast == VARS[var3][1]:
			if op == "+":
				VARS[var][0] = str(int(VARS[var3][0]) + int(VARS[var2][0]))
				return VARS
			else:
				VARS[var][0] = str(int(VARS[var2][0]) - int(VARS[var3][0]))
				return VARS
		else:
			print("Error de Tipo")
			return exit(1)
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
				return exit(1)
			return VARS
		else:
			print("Error de Tipo")
			return exit(1)
	obj = sent_func.match(line)
	if obj:
		var = obj.group(1)
		func = obj.group(2)
		var2 = obj.group(3)
		print(VARS[var][1],Funciones[func][0][2])
		if VARS[var][1] == Funciones[func][0][2]:
			VARS[var][0] = exe_func(func,var2,VARS)
			return VARS
		else:
			print("Error de Tipo")
			exit(1)
	obj = op_func_de.match(line)
	if obj:
		print("MATCH")
		var = obj.group(1)
		var2 = obj.group(2)
		op = obj.group(3)
		func = obj.group(4)
		var3 = obj.group(5)
		print(var,var2,op,func,var3)
		print(VARS[var][1],Funciones[func][0][2])
		if VARS[var][1] == Funciones[func][0][2]:
			print(var2,func,var3)
			aux = exe_func(func,var3,VARS)
			print(aux)
			print(var,var2,func,var3,aux)
			VARS[var][0] = operation(var2+" "+op+" "+aux[0]+";",VARS)
			print(VARS)
			return VARS
		else:
			print("Error de Tipo")
			exit(1)
	obj = op_func_iz.match(line)
	if obj:
		var = obj.group(1)
		fun = obj.group(2)
		var2 = obj.group(3)
		op = obj.group(4)
		var3 = obj.group(5)
		if VARS[var][1] == Funciones[func][2]:
			aux = exe_func(func,var2,VARS)
			VARS[var][0] = operation(aux+op+var3,VARS)
			return VARS
		else:
			print("Error de Tipo")
			exit(1)
	obj = op_func_do.match(line)
	if obj:
		var = obj.group(1)
		fun1 = obj.group(2)
		var1 = obj.group(3)
		op = obj.group(4)
		var2 = obj.group(5)
		func2 = obj.group(6)
		if VARS[var][1] == Funciones[func1][2]:
			aux1 = exe_func(func1,var1,VARS)
			aux2 = exe_func(func2,var2,VARS)
			VARS[var][0] = operation(aux1+op+aux2,VARS)
			return VARS
		else:
			print("Error de Tipo")
			exit(1)
	if line == "":
		print("Linea en Blanco, pasando ...")
		return VARS
	print("no se encontro nada")
	exit(1)


def float_to_int(var,VARS):
	var = VARS[var][0].split(".")[0]
	return var

def int_to_float(var,VARS):
	var = VARS[var][0]+".0"
	return var

def declaration(line,VARS): # En Desarrollo
	obj = var_val.search(line)
	if(obj):
		var = obj.group(1)
		tipo = obj.group(2) 
		var2 = obj.group(3)
		if isfloat(var2) and tipo in ["i16","i32"]:
			print("Error de Tipo")
			exit(1)
		else:
			VARS[var] = [var2,tipo]
			
		return VARS
	obj = var_var.search(line)
	if(obj):
		var = obj.group(1)
		tipo = obj.group(2) 
		var2 = obj.group(3)
		if VARS[var2][1] == tipo:
			VARS[var] = [VARS[var2][0],tipo]
			return VARS
		else:
			print("Error de Tipo")
			exit(1)
	obj = var_op.search(line)
	if obj:
		var = obj.group(1)
		tipo = obj.group(2)
		var2 = obj.group(3)
		op = obj.group(4)
		var3 = obj.group(5)
		sent = var2+op+var3+";"
		if (var2.isdigit() or isfloat(var2)) and (obj.group(5).isdigit() or isfloat(obj.group(5))):
			VARS[var] = [operation(sent,VARS),tipo]
			return VARS
		elif (var2.isdigit() or isfloat(var2)):
			if VARS[var3][1] == tipo:
				VARS[var] = [operation(sent,VARS),tipo]
				return VARS
			else:
				print("Error Tipo")
				exit(1)
		elif (var3.isdigit() or isfloat(var3)):
			if VARS[var2][1] == tipo:
				VARS[var] = [operation(sent,VARS),tipo]
				return VARS
			else:
				print("Error Tipo")
				exit(1)
		elif compar_types(obj.group(3),obj.group(5),VARS):
			if get_val_type(obj.group(3),VARS) in ["i32","i16"]:
				if tipo == VARS[var2][1]:
					valor = operation(var2+op+var3+";",VARS)
					VARS = up_val(obj.group(1),valor,obj.group(2),VARS)
					return VARS
				else:
					print("Error Tipo")
					exit(1)
			elif VARS[obj.group(3)][1]=="f64" and VARS[obj.group(3)][1]=="f64":
				valor = operation(var2+op+var3+";",VARS)
				VARS = up_val(obj.group(1),valor,obj.group(2),VARS)
				return VARS
		else:
			print("Error de tipo")
			exit(1)
	obj = var_op_cast_cast.search(line)
	if obj:
		if compar_types(obj.group(3),obj.group(6)):
			if get_val_type(obj.group(3)) == ("i32" or "i16"):
				valor = ops[obj.group(5)](int(float(get_val_value(obj.group(3)))),int(float(get_val_value(obj.group(6)))))
				VARS = up_val(obj.group(1),valor,obj.group(2),VARS)
				return VARS
			else:
				valor = ops[obj.group(5)](float(get_val_value(obj.group(3))),float(get_val_value(obj.group(6))))
				VARS = up_val(obj.group(1),valor,obj.group(2),VARS)
				return VARS
		else:
			print("Error de tipo")	
	obj = var_op_valcasti.search(line)
	if obj:
		obj = sent_op_valcastd.search(line)
	obj = var_func.match(line)
	if obj:
		var = obj.group(1)
		tipo = obj.group(2)
		func = obj.group(3)
		var2 = obj.group(4)
		VARS[var] = [exe_func(func,var2,VARS),tipo]
		return VARS

	print("No Definido")
	exit(1)

def up_val(var,valor,tipo,VARS):
	VARS[var] = [valor,tipo]
	return VARS

def compar_types(var1,var2,VARS): ###
	if VARS[var1][1] == VARS[var2][1]:
		return True
	else:
		print("Error de tipo")
		return exit(1)

def cast(var,tipo,VARS): ###
	if var not in VARS.keys():
		return exit(1)
	VARS[var][1] = tipo

def get_val_type(var,VARS):
		return VARS[var][1]

def get_val_value(var,VARS):
	if VARS[var][0].isdigit():
		return int(VARS[var][0])
	else:
		return float(VARS[var][0])

def operation(line,VARS):
	obj = op_sc.match(line)
	if (obj):
		var = obj.group(1)
		op = obj.group(2)
		var2 = obj.group(3)
		if (var.isdigit() or isfloat(var)) and (var2.isdigit() or isfloat(var2)):
			if op == "+":
				return str(float(var) + float(var2))
			else:
				return str(float(var) - float(var2))
		elif var.isdigit() or isfloat(var):
			if VARS[var2][1] in ["i16","i32"]:
				if op == "+":
					return str(int(var) + int(VARS[var2][0]))
				else:
					return str(int(var) - int(VARS[var2][0]))
			else:
				if op == "+":
					return str(float(var) + float(VARS[var2][0]))
				else:
					return str(float(var) - float(VARS[var2][0]))
		elif var2.isdigit() or isfloat(var):
			if VARS[var][1] in ["i16","i32"]:
				if op == "+":
					return str(int(var2) + int(VARS[var][0]))
				if op == "-":
					return str(int(VARS[var][0]) - int(var2))
			else:
				if op == "+":
					return str(float(var2) + float(VARS[var][0]))
				if op == "-":
					return str(float(VARS[var][0]) - float(var2))
		elif var in VARS.keys() and var2 in VARS.keys():
			if compar_types(var,var2,VARS):
				if VARS[var][1] in ["i16","i32"] and VARS[var2][1] in ["i16","i32"]:
					if op == "+":
						return str(int(VARS[var][0]) + int(VARS[var2][0]))
					if op == "-":
						return str(int(VARS[var][0]) - int(VARS[var2][0]))
				elif VARS[var][1] == "f64" and VARS[var2][1] == "f64":
					if op == "+":
						return str(float(VARS[var][0]) + float(VARS[var2][0]))
					if op == "-":
						return str(float(VARS[var][0]) - float(VARS[var2][0]))
			else:
				print("Error de Tipos")
				exit(1)

		else:
			print("Variable "+var+" o "+var2+" no declarada")
			return exit(1)

	obj = sent_func.match(line)
	if (obj):  # Falta La funcion que ejecuta las funciones para llamarla aca
		var = obj.group(1)
		func = obj.group(2)
		var2 = obj.group(3)
		val = exe_func(func,var2,VARS)
		if VARS[var][1] == Funciones[func][0][2]:
			VARS[val][0] = val
		else:
			print("Error de Tipo")
			exit(1)
	obj = sent_var.match(line)
	if (obj):
		var = obj.group(1)
		var2 = obj.group(2)
		if var in VARS.keys() and var2 in VARS.keys():
			if compar_types(var,var2):
				return var2
			else:
				print("Error de Tipo")
				return exit(1)
		else:
			print("Variable o variables no definidas")
	
	obj = sent_val.match(line)
	if (obj):
		var = obj.group(1)
		val = obj.group(2)
		if var not in VARS.keys():
			print("Variable "+var+" no definida")
			return exit(1)
		return val
	
	obj = sent_op_cast.match(line)
	if (obj):
		var = obj.group(1)
		var2 = obj.group(2)
		cast = obj.group(3)
		if var not in VARS.keys():
			print("Variable "+var+" no definida")
			return exit(1)
		if cast == VARS[var][1]:
			return var2
		else:
			print("Error de Tipo")
			return exit(1)

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
			return exit(1)

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
			return exit(1)
	
	obj = retorno_opsc.match(line)
	if (obj):
		if obj.group(1) in VARS.keys():
			var = obj.group(1)
			op = obj.group(2)
			var2 = obj.group(3)
			if var.isdigit() and var2.isdigit():
				if op == "+":
					return str(int(var) + int(var2))
				elif op == "-":
					return str(int(var) - int(var2))
			elif var.isdigit():
				if not compar_types(obj.group(1),var2):
					print("Error de tipos")
					return exit(1)
				var2 = get_val_value(var2,VARS)
				if op == "+":
					return str(int(var) + var2)
				else:
					return str(int(var) - var2)
			elif var2.isdigit():
				if compar_types(obj.group(1),var,VARS) == False:
					print("Error de tipos")
					return exit(1)
				var = get_val_value(var,VARS)
				if op == "+":
					return str(var + int(var2))
				else:
					return str(var - int(var2))
			else:
				if compar_types(var,var2,VARS) == False:
					print("Error de tipos")
					return exit(1)
				if compar_types(obj.group(1),var,VARS) == False:
					print("Error de tipos")
					return exit(1)
				var = get_val_value(var,VARS)
				var2 = get_val_value(var2,VARS)
				if op == "+":
					return str(var + var2)
				else:
					return str(var - var2)
		else:
			print("Variable "+obj.group(1)+" no declarada")
			return exit(1)


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
				exit(1)
		else:
			print("Error de Tipo")
			exit(1)
	print("Error de Sintaxis --> ",line)
	exit(1)


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

def isfloat(a):
	if "." in a:
		return True
	else:
		return False

def exe_func(nombre,val,VARS):
	lista = Funciones[nombre][1:]
	if val.isdigit():
		VARS_Local = dict()
		VARS_Local[Funciones[nombre][0][0]] = [val,Funciones[nombre][0][1]]
	elif isfloat(val):
		VARS_Local = dict()
		VARS_Local[Funciones[nombre][0][0]] = [val,Funciones[nombre][0][1]]
	elif val in VARS.keys():
		VARS_Local = dict()
		VARS_Local[Funciones[nombre][0][0]] = [VARS[val][0],Funciones[nombre][0][1]]
	while len(lista) > 0:
		line = lista[0]
		print(lista)
		print(VARS_Local)
		line = line.strip("\n")
		line = line.strip("\t")
		a = identifier(line)
		if a == WHILE:
			lista_while = while_list_static(line,lista)
			VARS_Local,lista = exe_while_static(lista_while,lista,VARS_Local)
		elif a == IF:
			VARS_Local,lista = if_exec_static(line,lista,VARS_Local)
		elif a == SENT:
			VARS_Local = sentence(line,VARS_Local)
			lista.pop(0)
		elif a == RETURN:
			return ret_fun(line,Funciones[nombre][0][1],VARS_Local)


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

def main():
	fp = open("codigo_rust2.txt","r")
	i = 1
	DIC = dict()
	for line in fp:
		line = line.strip("\n")
		line = line.strip("\t")
		print(line)
		a = identifier(line)
		if a == FN:
			store_fun(line,fp)
			print("Evaluando funcion")
		elif a == WHILE:
			print("Evaluando while")
			lista = while_list(line,fp)
			exe_while(lista,fp,DIC)
		elif a == IF:
			print("Evaluando if")
			DIC= if_exec(line,fp,DIC)
		elif a == LET:
			print("Declarando: ",line)
			DIC = declaration(line,DIC)
			print(DIC)
		elif a == SENT:
			print("Sentenciando: ",line)
			DIC = sentence(line,DIC)
		elif a == PRINT:
			println(line,DIC)
		else:
			continue
	print("Termino del Archivo\n\n")
	print("Funciones -> ",Funciones,"\n")
	print("Variables en Main -> ",DIC)

if __name__ == '__main__':
	main()