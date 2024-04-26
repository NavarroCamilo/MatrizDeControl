
from sympy import symbols, Eq, solve
import re


# Código de resolución de sistema de ecuaciones para hallar la matriz de control
def resolver_sistema_ecuaciones(mat, term):
        # Crear símbolos para las variables
        n=len(mat[0])
        variables = symbols('A:{}'.format(chr(ord('A') + n-1)))
        # Crear ecuaciones a través de la multiplicación de matrices
        ecuaciones = [Eq(sum([mat[i][j] * variables[j] for j in range(len(variables))]), term[i]) for i in range(len(mat))]
        # Resolver el sistema de ecuaciones
        soluciones = solve(ecuaciones, variables)
        
        # Imprimir las soluciones. Se incluyen las variables independientes
        for var in variables:
            if var not in soluciones.keys():
                soluciones[var]= soluciones[var]=var 
        
        #Se coloca en un diccionario ordenado y se extraen los coeficientes
        soluciones = {key: str(value) for key, value in soluciones.items()}
        soluciones = {str(clave): valor for clave, valor in soluciones.items()}
        soluciones = {k: soluciones[k] for k in sorted(soluciones)}
        #print(soluciones)
        return extraer_coeficientes(soluciones)

# Código de formateo de la expresión. Separa los coeficientes de las variables. Con este formato (coeficiente)variable
def extraer_coeficientes(diccionario):
    nuevo_diccionario = {}
    f ={}
    for key, value in diccionario.items():
        # Encuentra todos los coeficientes y variables en la expresión
        coeficientes = re.findall(r'([-+]?\d*\.?\d*)\*?([A-Za-z]+)', value)
        f[key] = extraer_fracciones(value)
        # Formatea los coeficientes como (coeficiente)variable
        coeficientes = [(f"({c})" if c != '+' else '(1)') + v for c, v in coeficientes]
        # Forma la nueva expresión
        nueva_expresion = '+'.join(coeficientes)
        nueva_expresion = nueva_expresion.replace('()', '(1)')
        nueva_expresion = nueva_expresion.replace('(-)', '(-1)')
        nuevo_diccionario[key] = nueva_expresion
    #Cuando encuentra un paréntesis, se añade la fracción
    for clave, valores in f.items():
        if f[clave]:
            pos=[]
            for i, char in enumerate(nuevo_diccionario[clave]):
                if char == ')':
                    if i > 0 and nuevo_diccionario[clave][i-1].isdigit():
                        # Verificar si hay un '/' antes del número
                        if i > 1 and nuevo_diccionario[clave][i-2] == '/':
                            pos.append(i)
            for i in range(len(pos)):
                nuevo_diccionario[clave] = nuevo_diccionario[clave][:pos[i]+(i*2)] + f'/{f[clave][i]})' + nuevo_diccionario[clave][pos[i]+1+(i*2):]
    return nuevo_diccionario

# Extrae las fracciones de la expresión, las formatea y las añade a la expresión
def extraer_fracciones(cadena):
    simbolos = []
    i = 0
    while i < len(cadena):
        if cadena[i].isalpha():
            j = i + 1
            while j < len(cadena) and cadena[j] != '+' and cadena[j] != '-':
                if cadena[j] == '/':
                    j += 1
                    simbolo = ''
                    while j < len(cadena) and cadena[j] != '+' and cadena[j] != '-':
                        simbolo += cadena[j]
                        j += 1
                    simbolos.append(simbolo)
                else:
                    j += 1
            i = j
        else:
            i += 1
    return simbolos

# Convierte a Zp los coeficientes
def convertir_coef (dicc, q):
    for clave, valor in dicc.items():
        subs = re.findall(r'\((.*?)\)', valor)
        for i in range(len(subs)):
            if '/' not in subs[i]:
                dicc[clave]=dicc[clave].replace(f'({subs[i]})',str(int(subs[i])%q))
            else:
                parts=subs[i].split('/')
                num=str((int(parts[0])%q * pow(int(parts[1]), -1, q))%q)
                dicc[clave]=dicc[clave].replace(f'({subs[i]})',num)
    return dicc

def mat_control(sis):
    #Se crea la matriz de control
    #Se buscan las posiciones de las variables
    #Representan sacar el factor común de las variables, para hallar los elementos de la matriz
    H=[]
    for clave in sis:
        cl=str(clave)
        x=[]
        for clave in sis:
            v=str(sis[clave])
            if cl in v:
                pos=v.find(cl)
                x.append(int(v[pos-1]))
            else:
                x.append(0)
        t=all(e == 0 for e in x)
        if not t:
            H.append(x)
    return H

if __name__ == "__main__":
    mat = [[1, 0, 1], [0, 1, 1]]
    term = [0, 0, 0]#tantos 0 como columnas tenga la matriz G
    sis=resolver_sistema_ecuaciones(mat, term)
    sis=convertir_coef(sis, 2)
    mat_control(sis)
    
