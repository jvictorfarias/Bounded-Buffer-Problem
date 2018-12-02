#  @Author: Joao Victor Farias
# -*- coding: utf-8 -*-
import os, sys, random, time
from multiprocessing import Process, Lock, Semaphore, Array, Value


def produtor(lock, empty, full, buffer, a_produzir, BUFFER_SIZE, numProdutor, timeout):
    while(True and time.time() < timeout):

        #  Verificando se tem posições livre no buffer
        empty.acquire()

        #  Se possível, o mutex é iniciado e entra na região crítica(Se ela estiver livre)
        lock.acquire()
        print 'Produtor %d entrando na região crítica.' % (numProdutor)

        #  Produzindo ...
        valor = random.randint(1, 1000)
        buffer[a_produzir.value] = valor
        print 'Produtor %d produziu o valor %d e o inseriu na posição %d' % (numProdutor, valor, a_produzir.value)
        a_produzir.value = (a_produzir.value + 1) % BUFFER_SIZE

        #  Libera a região crítica
        lock.release()
        print 'Produtor %d saindo da região crítica.' % (numProdutor)

        #  Sinaliza o consumidor para que ele possa consumir
        full.release()

        #  Coloca a thread para dormir
        sono = random.randint(0,10)
        print 'Produtor %d dormindo por %d' % (numProdutor, sono)
        time.sleep(sono)
    return
def consumidor(lock, empty, full, buffer, a_consumir, BUFFER_SIZE, numConsumidor, timeout):
    while(True and time.time() < timeout):

        #  Verificando se tem posições a serem consumidas no buffer
        full.acquire()
       
        
        #  Se possível, o mutex é iniciado e entra na região crítica
        lock.acquire()
        print 'Consumidor %d entrando na região crítica.' % (numConsumidor)

        #  Consumindo ...
        valor = buffer[a_consumir.value]
        print 'Consumidor %d consumiu o valor %d na posição %d.' % (numConsumidor, valor, a_consumir.value)
        a_consumir.value = (a_consumir.value + 1) % BUFFER_SIZE

        #  Libera a região crítica
        lock.release()
        print 'Consumidor %d saindo da região crítica.' % (numConsumidor)

        #  Sinaliza o produtor para que ele possa produzir
        empty.release()

        #  Coloca a thread para dormir
        sono = random.randint(0,10)
        print 'Consumidor %d dormindo por %d segundos.' % (numConsumidor, sono)
        time.sleep(sono)
    return


if __name__ == '__main__': 
    
    BUFFER_SIZE = 5                             #  Tamanho do buffer
    buffer = Array('i', BUFFER_SIZE)            #  Nosso buffer limitado inicializado
    lock = Lock()                               #  Lock mutex
    empty = Semaphore(BUFFER_SIZE)              #  Semaforo que guarda a quantidade de posições livres
    full = Semaphore(0)                         #  Semaforo que guarda o número de posicoes ocupadas
    a_consumir = Value('i', 0)                  #  Índice do próximo item a ser consumido
    a_produzir = Value('i', 0)                  #  Índice do próximo item a ser produzido
    timeout = time.time() + int(sys.argv[1])    #  Tempo que o algoritmo irá rodar
    produtores = []                             #  Lista de inicialização dos produtores
    consumidores = []                           #  Lista de inicialização dos consumidores

    #  Iniciando os produtores
    for i in range (int(sys.argv[2])):
        Process(target = produtor, args=(lock, empty, full, buffer, a_produzir, BUFFER_SIZE, i, timeout)).start()
    #  Iniciando os consumidores
    for j in range (int(sys.argv[3])):
        Process(target = consumidor, args=(lock, empty, full, buffer, a_consumir, BUFFER_SIZE, j, timeout)).start()
    
    while(True):
        if(time.time() > timeout):
            os.abort()






