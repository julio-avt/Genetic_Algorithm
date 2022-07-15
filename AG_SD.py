import numpy as np

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
            #Cambiar el espacio de búsqueda
            if Cm == 1:
                a[Pm] = np.random.uniform(0, 1)
                #if Pm == 0: #Valores de R_s
                #    a[Pm] = np.random.uniform(0, 0.5)
                #if Pm == 1: #Valores de R_sh
                #    a[Pm] = np.random.uniform(0, 100)
                #if Pm == 2: #Valores de I_ph
                #    a[Pm] = np.random.uniform(0, 1)
                #if Pm == 3: #Valores de I_sd
                #    a[Pm] = np.random.uniform(0, 1)
                #if Pm == 4: #Valores de n
                #    a[Pm] = np.random.uniform(1, 2)
            if Cm == 2:
                a[Pm] = np.random.uniform(0, 1)
                #if Pm == 0: #Valores de R_s
                #    b[Pm] = np.random.uniform(0, 0.5)
                #if Pm == 1: #Valores de R_sh
                #    b[Pm] = np.random.uniform(0, 100)
                #if Pm == 2: #Valores de I_ph
                #    b[Pm] = np.random.uniform(0, 1)
                #if Pm == 3: #Valores de I_sd
                #    b[Pm] = np.random.uniform(0, 1)
                #if Pm == 4: #Valores de n
                #    b[Pm] = np.random.uniform(1, 2)
    
    return a[0:len(a)-1],b[0:len(b)-1]

################################################################################
#Inicializamos las contantes    
pop = 100       #Cantidad de candidatos
dim = 5         #Cantidad de variables a determinar
generation = 100 #Cantidad de iteraciones
q = 1.602 * 10**(-19) #Carga del electrón
k = 1.380 * 10**(-23) #Cte de Boltzmann
T = 310              #Temperatura Kelvin
V_m = -0.2057
I_m = 0.764
fitness = 100 #Criterio de paro
solution = [] #Guardaremos las soluciones
################################################################################

cont = 0
while abs(fitness) >= 1:
    #Matriz que contiene las variables
    M_pop = np.zeros((pop,dim))
    #Matriz con los fitness
    M_target = np.zeros((pop,1))
    #Llenamos la matriz de valores aleatorios cuidando el rango
    for i in range(pop):
        for j in range(pop):
            if j == 0: #Valores de R_s
                M_pop[i][j] = np.random.uniform(0, 0.5)
            if j == 1: #Valores de R_sh
                M_pop[i][j] = np.random.uniform(0, 100)
            if j == 2: #Valores de I_ph
                M_pop[i][j] = np.random.uniform(0, 1)
            if j == 3: #Valores de I_sd
                M_pop[i][j] = np.random.uniform(0, 1)
            if j == 4: #Valores de n
                M_pop[i][j] = np.random.uniform(1, 2)

    #Evaluamos los números aleatorios para obtener los fitness
    for i in range(pop):
        cociente1 = q * (V_m +  M_pop[i][0] * I_m) / (M_pop[i][4] * k * T)
        exponencial = np.exp(cociente1)
        cociente2 =  (V_m +  M_pop[i][0] * I_m) / M_pop[i][1]
        M_target[i] = M_pop[i][2] - M_pop[i][3] * (exponencial -1) - cociente2
    #Concatenamos las matrices de variables y fitness
    M_ag = np.concatenate((M_pop, M_target), axis=1)

    gen = 1
    while gen < generation:
        #ordenaremos de menor a mayor con base en la columna de fitness
        M_ag = M_ag[np.argsort(M_ag[:, -1])]
        #Creamos una matriz temporal
        M_temp = np.zeros((pop,dim))
        #Guardamos los dos primeros valores de M_ag en M_temp
        M_temp[0] = M_ag[0][:dim]
        M_temp[1] = M_ag[1][:dim]

        for AG in range(2,pop-1):
            #Hacemos la selección por torneo
            winner1, winner2 = tournament_selection(pop)
            Padre1 = M_ag[winner1]
            Padre2 = M_ag[winner2]
            #Guardamos los valores del cross over en la matriz temporal
            M_temp[AG], M_temp[AG+1] = cross_over(Padre1, Padre2)
        #Evaluamos los nuevos fitness
        for i in range(pop):
            cociente1 = q * (V_m +  M_temp[i][0] * I_m) / (M_temp[i][4] * k * T)
            exponencial = np.exp(cociente1)
            cociente2 =  (V_m +  M_temp[i][0] * I_m) / M_temp[i][1]
            M_target[i] = M_temp[i][2] - M_temp[i][3] * (exponencial -1) - cociente2
        #Repetimos el proceso de concatenar ero ahora guardamos la matriz temporal
        M_ag = np.concatenate((M_temp, M_target), axis=1)

        #print('Generación ', gen)
        gen+=1
    #Reordenamos la ultima columna
    M_ag = M_ag[np.argsort(M_ag[:, -1])]

    solution.append(M_ag[0][-1])
    fitness = sum(solution) / len(solution)
    cont+=1
    print("-"*20)
    print(f"Iteracion {cont}: {fitness}")
    print("-"*20)
    


print(f"""Fitness: {I_m - M_ag[0][-1]}""")
print(f"I_med = {I_m}")
print(f"I_est = {M_ag[0][-1]}")
print(f"R_s = {M_ag[0][0]}")
print(f"R_sh = {M_ag[0][1]}")
print(f"I_ph = {M_ag[0][2]}")
print(f"R_s = {M_ag[0][3]}")
print(f"R_s = {M_ag[0][4]}")

