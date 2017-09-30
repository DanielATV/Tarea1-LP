import re

Variables = dict()
Funciones = dict()
In_Fun = False
In_While = False

var_val = re.compile("let mut\s*(\w*)\s*:\s*(i16|i32|f64)\s*=\s*(\d*)")
var_var = re.compile("let mut\s*(\w*)\s*:\s*(i16|i32|f64)\s*=\s*(\w*)")
op_sc = re.compile("(\w*|\d*)\s*(\+|\-)\s(\w*|\d*)")
op_cd = re.compile("\((\w*)\s*as\s*(i16|i32|f64)\)\s*(\+|\-)\s*(\w*)")
op_ci = re.compile("(\w*)\s*(\+|\-)\s\((\w*)\s*as\s*(i16|i32|f64)\)")
cast = re.compile("\((\w*)\s*as\s*(i16|i32|f64)\)")
while_sent = re.compile("while\s(\w*)\s(<|>|=|>=|<=)\s(\w*)\s{")
end_while = re.compile("}")
if_sent = re.compile("if\s(\w*)\s(<|>|=|>=|<=)\s(\w*)\s{")
enf_if = re.compile("}")
retorno_var_val = re.compile("return\s(\w*);")
retorno_opsc = re.compile("return\s((\w*|\d*)\s*(\+|\-)\s(\w*|\d*));")
retorno_cd = re.compile("return\s(\((\w*)\s*as\s*(i16|i32|f64)\)\s*(\+|\-)\s*(\w*));")
retorno_ci = re.compile("return\s(\w*)\s*(\+|\-)\s\((\w*)\s*as\s*(i16|i32|f64)\);")

"""
Nombre variable: [A-z]+
Valores: [0-9]+
Asignacion de variables
Declaracion de variables
    Variable -> Valor : let mut\s*(\w*)\s*:\s*(i16|i32|f64)\s*=\s*(\d*);
    Variable -> Variable : let mut\s*(\w*)\s*:\s*(i16|i32|f64)\s*=\s*(\w*);
Funciones: fn ([A-z]+)\(([A-z]+): (i16|i32|f64)\) -> (i16|i32|f64){
Funcion main: fn ([A-z]+)\(\) {
Retorno: println!\([A-z]+\);
Operaciones: [A-z]+|[0-9]+|\(([A-z]+) as (i16|i32|f64)\) +|- [A-z]+|[0-9]+|\(([A-z]+) as (i16|i32|f64)\) 
    +/- sin cast -> (\w*|\d*)\s*(\+|\-)\s(\w*|\d*)
    +/- con cast -> \((\w*)\s*as\s*(i16|i32|f64)\)\s*(\+|\-)\s*(\w*) <- cast por la derecha
    +/- con cast -> (\w*)\s*(\+|\-)\s\((\w*)\s*as\s*(i16|i32|f64)\) <- cast por la izquierda
Boleanos(< <= > >= =) -> (\w*)\s(<|>|=|>=|<=)\s(\w*)
If, else if, else, while
Cast: \(([A-z]+) as (i16|i32|f64)\)
Print: println!\(([A-z][A-z,0-9]*)\);
"""

"""
Funciones > diccionario; llave: nombre; valor: lista(tipo vari entrada,tipo vari salida,sentencias)
Variabloes > diccionario; llaves: nombre; valor: lista(tipo,valor)
"""
