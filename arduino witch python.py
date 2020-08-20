# -*- coding: utf-8 -*-
import serial
import csv
import numpy as np
from numpy import fft, angle
import matplotlib.pyplot as plt
import time

# antes de iniciar ver em que porta esta ligado a porta arduino
ser = serial.Serial('COM3', baudrate=9600, timeout=1000)
ser.flushInput()

while True:
    try:

        AMOSTRAS = 128
        dado = []

        for i in range (0,AMOSTRAS):
            ser_bytes = ser.readline()
            decoded_bytes = float(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
            # print(decoded_bytes)
            dado.append(int(decoded_bytes))
        # print(dado)
        ser.close()


        # Definicao de parametros
        n_ondas = 2		# escolhe o num. de ondas capturadas
        n = n_ondas*64		# 64 dados capturados para cada onda
        T = n_ondas*1.0/50	# periodo em funcao do num. de ondas
        dt = T/n		# intervalo de cada medida
        t = dt*np.arange(0,n)	# gera vetor com os instantes
        

        # Calculo da transformada de Fourier
        Fk = fft.fft(dado)/(n)	# coeficientes de Fourier normalizados
        nu = fft.fftfreq(n,dt)	# frequencias naturais
        delta = angle(Fk)	# angulo de fase de cada componente
        print(Fk)

        # Salvando dados no arquivo dados.txt
        # ofile  = open('dado.csv', "wb")
        # writer = csv.writer(ofile, delimiter='\t', quotechar='"', quoting=csv.QUOTE_ALL)

        # with open("test_data.csv","a") as f:
        #     writer = csv.writer(f,delimiter=",")
        #     writer.writerow([time.time(),decoded_bytes])


        # for i in range (0,AMOSTRAS):
        #     writer.writerow([dado[i], nu[i], abs(Fk[i]), delta[i]])
        # ofile.close()

        # Escreve os dados na tela
        # print(nu)
        # print(abs(Fk))
        # print(angle(Fk))

        # Gráficos
        plt.subplot(2, 1, 1)		# grafico dos dados x tempo
        plt.xlim(0.001, T)
        plt.ylim(0, 1200)
        plt.plot(t,dado)
        plt.xlabel('tempo(s)')
        plt.ylabel('amplitude')
        #----------------

        plt.subplot(2, 1, 2)		# grafico da amplitude x harmonicas     
        plt.xlim(0, 50)
        plt.ylim(0, 800)
        plt.bar(nu, abs(Fk),
        width=2,
        align='center',
        alpha=0.4,
        color='b',
        label='Frequencia'
        )
        plt.xlabel('freq. (Hz)')
        plt.ylabel('|A(freq.)|')

        plt.show()			# mostra os graficos
        
    except:
        print("Keyboard Interrupt")
        break