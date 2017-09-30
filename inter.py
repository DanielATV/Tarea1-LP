import re

"""
Nombre variable: [A-z]+
Asignacion de variables
Declaracion de variables
    Variable -> Valor : let mut\s*(\w*)\s*:\s*(i16|i32|f64)\s*=\s*(\d*);
    Variable -> Variable : let mut\s*(\w*)\s*:\s*(i16|i32|f64)\s*=\s*(\w*);
Funciones: fn\s(\w*)\((\w*):\s(i16|i32|f64)\)\s->\s(i16|i32|f64){ || 
Retorno
Operaciones(+ -)
    +/- sin cast -> (\w*|\d*)\s*(\+|\-)\s(\w*|\d*)
    +/- con cast -> \((\w*)\s*as\s*(i16|i32|f64)\)\s*(\+|\-)\s*(\w*) <- cast por la derecha
    +/- con cast -> (\w*)\s*(\+|\-)\s\((\w*)\s*as\s*(i16|i32|f64)\) <- cast por la izquierda
Boleanos(< <= > >= =)
If, else if, else, while
cast \(([A-z][A-z,0-9]*)\sas\s(i16|i32|f64)\)
print println!\(([A-z][A-z,0-9]*)\);
"""

"""
Funciones > diccionario; llave: nombre; valor: lista(tipo vari entrada,tipo vari salida,sentencias)
Variabloes > diccionario; llaves: nombre; valor: lista(tipo,valor)
"""
