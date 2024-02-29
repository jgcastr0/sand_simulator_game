import numpy as np
from time import time
from numba import njit

inicio = time()
numeros = np.array(list(range(1, 100_000_000)))


def teste(x):
    if x % 2 == 0:
        x = x * 2
        return x
    else:
        return 0
    
numeros = np.vectorize(teste)(numeros)

fim = time() - inicio
print(fim)