import numpy as np
import pandas as pd

def f(x,y,z):
    return 2.3 * x + 5.1 * y + 6.6 *z

def cross_over(a,b,prob_cross=0.9, prob_mut=0.2):
    """Esta función hace cross over en 2 arreglos. Lo hace con una probabilidad
    dada (por default 90%).

    Args:
        a (array): arreglo 1
        b (array): arreglo 2
        prob_cross (float): probabilidad de hacaer Cross Over
        prob_mut (float): probabilidad de hacaer Mutación
    """
    Cross = np.random.rand()
    if Cross <= prob_cross:
        Pc = np.random.randint(0,len(a)-1)
        #Esta parte hace el cross over
        for j in range(len(a)-1):
            if j != Pc:
                aux = a[1]
                a[j] = b[j]
                b[j] = aux

        #Hagamos mutación
        Mut = np.random.rand()
        if Mut < prob_mut:
            #Entrada a mutar
            Pm = np.random.randint(0,len(a)-1)
            #Haremos la mutación en a o en b    
            Cm = np.random.randint(1,2)
            if Cm == 1:
                a[Pm] = np.random.uniform(1,10)
            if Cm == 2:
                b[Pm] = np.random.uniform(1,10)
    
    return a[0:len(a)-1],b[0:len(b)-1]

def tournament_selection(pop):
    """Esta función se encarga de realizar la selección 
    por torneo.

    Args:
        pop: cantidad de población para limitar el rango superior
        de los enteros a escoger aleatoriamente.

    Returns:
        int: 2 enteros escogidos aleatoriamente por torneo
    """

    #Generamos dos números aleatorios entre el 2 y la población
    a = [np.random.randint(2,pop-1), np.random.randint(2,pop-1)]
    #Tomamos el índice del mayor para cambiarlo
    index_max = a.index(max(a))
    aux = a[index_max]
    a[index_max] = np.random.randint(2,pop-1)
    #Aseguremos que el valor por el que se cambiará sea distinto
    while aux == a[index_max]:
        a[index_max] = np.random.randint(2,pop-1)
    #Aseguremonos de que sean valores distintos
    while a[0] == a[1]:
        a[1] =   np.random.randint(2,pop-1) 
    return a[0], a[1]

def genetic_algorithm(pop, dim, generation, f):
    """Esta función realiza el algoritmo genético.

    Args:
        pop (int): número de población
        dim (int): número de dimensiones
        generation (int): cantidad de generaciones(iteraciones)
        f (function): función objetivo a evaluar

    Args:
        pop (_type_): _description_
        dim (_type_): _description_
        generation (_type_): _description_
        f (_type_): _description_

    Returns:
        np.array: Regresa un arreglo con las aproximaciones 
        y el fitness a obtener.
    """

    #Matriz que contiene las variables
    M_pop = np.random.uniform(-10,10, (pop,dim))
    #Matriz con los fitness
    M_target = np.zeros((pop,1))
    #Evaluamos los números aleatorios para obtener los fitness
    for i in range(pop):
        M_target[i] = f(M_pop[i][0], M_pop[i][1], M_pop[i][2])
    #Concatenamos las matrices de variables y fitness
    M_ag = np.concatenate((M_pop, M_target), axis=1)

    gen = 1
    while gen < generation:
        #ordenaremos de menor a mayor con base en la columna de fitness
        M_ag = M_ag[np.argsort(M_ag[:, -1])]
        #Creamos una matriz temporal
        M_temp = np.zeros((pop,dim))
        #Guardamos los dos primeros valores de M_ag en M_temp
        M_temp[0] = M_ag[0][0:3]
        M_temp[1] = M_ag[1][0:3]

        for AG in range(2,pop-1):
            #Hacemos la selección por torneo
            winner1, winner2 = tournament_selection(pop)
            Padre1 = M_ag[winner1]
            Padre2 = M_ag[winner2]
            #Guardamos los valores del cross over en la matriz temporal
            M_temp[AG], M_temp[AG+1] = cross_over(Padre1, Padre2)
        #Evaluamos los nuevos fitness
        for i in range(pop): 
            M_target[i] = f(M_temp[i][0], M_temp[i][1], M_temp[i][2])
        #Repetimos el proceso de concatenar ero ahora guardamos la matriz temporal
        M_ag = np.concatenate((M_temp, M_target), axis=1)

        #print('Generación ', gen)
        gen+=1
    #Reordenamos la ultima columna
    M_ag = M_ag[np.argsort(M_ag[:, -1])]

    return M_ag[0] 

#Inicializamos las contantes    
pop = 100       #Cantidad de candidatos
dim = 3         #Cantidad de variables a determinar
generation = 100 #Cantidad de iteraciones

#Generamos 100 soluciones y saquemos un promedio
solution = []
for i in range(20):
    solution.append(genetic_algorithm(pop, dim, generation, f))
    print(f"Solución {i+1}")

final_solution = sum(solution)/len(solution)
print("Variables reales:\t X = -9 \t Y = -10 \t Z = -8")
print(f"Variables estimadas: X = {final_solution[0]} , Y = {final_solution[1]}, Z = {final_solution[2]}")
