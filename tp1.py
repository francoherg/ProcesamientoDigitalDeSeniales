import matplotlib.pyplot as plt
import numpy as np

def plotear(datos):
    t, y = datos
    fig, ax = plt.subplots()
    ax.plot(t, y, linewidth=2.0)
    plt.style.use('seaborn-v0_8-notebook')
    # Ejes con líneas horizontales y verticales
    ax.axhline(y=0, color="black", linestyle="--")  # Eje X
    ax.axvline(x=0, color="black", linestyle="--")  # Eje Y
    plt.show()

def plotear_stem(datos):
    t, y = datos
    fig, ax = plt.subplots()
    
    # Gráfico tipo "stem" (líneas verticales con puntos)
    ax.stem(t, y, linefmt="b-", markerfmt="bo", basefmt="k-") 
    
    plt.style.use('seaborn-v0_8-notebook')

    # Ejes con líneas horizontales y verticales
    ax.axhline(y=0, color="black", linestyle="--")  # Eje X
    ax.axvline(x=0, color="black", linestyle="--")  # Eje Y

    plt.show()

def plotear_grid(datos, ax, titulo):
    t, y = datos
    ax.plot(t, y, linewidth=2.0)
    ax.axhline(y=0, color="black", linestyle="--", alpha=0.5)
    ax.axvline(x=0, color="black", linestyle="--", alpha=0.5)
    ax.set_title(titulo)

print(plt.style.available)


def senoidal(tini,tfin,fm,fs, phi):
    T = 1/fm
    t = np.arange(tini,tfin, T)
    y = np.sin(2 *np.pi * fs * t + phi)
    return t,y

#senoidal(-np.pi,np.pi,20,10,1)

def sinc(tini,tfin,fm,fs, phi):
    T = 1/fm
    t = np.arange(tini,tfin, T)

    x=2 * np.pi *fs * t

    y_zero = 1
    y = np.sin(x)/x
    y = np.where(t == 0, y_zero, y)
    return x,y

#sinc(-np.pi,np.pi,20,10,1)

def ondaCuadrada(tini,tfin,fm,fs, phi):
    T = 1/fm #paso
    t = np.arange(tini,tfin, T)

    x=2 * np.pi *fs * t
    y = np.where(np.mod(x + phi,  2*np.pi) >= np.pi, 1, -1)
    return x,y

# EJERCICIO 2
## Invertir horizontalmente, la variable independiente
def invertir(datos):
    return -datos[0],datos[1]

#plotear(invertir(ondaCuadrada(0,1,100,3,3)))

## rectificacion, que no tenga valores negativos.

### rectificacion de media onda: la parte negativa se hace 0
def rectificacionMediaOnda(datos):
    t, y = datos
    y_rectificado = np.where(y < 0, 0, y)
    return t, y_rectificado

#plotear(rectificacionMediaOnda(senoidal(0,1,100,3,3)))

### rectificacion de onda completa: lo que es negativo se hace positivo
def rectificacionOndaCompleta(datos):
    t, y = datos
    y_rectificado = np.where(y < 0, -y, y)
    return t, y_rectificado

#plotear(rectificacionOndaCompleta(senoidal(0,1,100,3,3)))
# se puede ver cortado en las puntas por la frecuencia de muestreo.
# por ejemplo en 300 de fm se ve bien.


# cuantizar: amplitud ya no es continua. 
# se discretiza en un numero de niveles o escalones.
def cuantizar(niveles,tam_cuanto,datos):
    x,y = datos
    # funciona solo con positivos. le resto el minimo y luego se lo sumo
    minimo = np.min(y)
    y = y - minimo
    condicion = [
        (x < 0),  
        (x >= 0) & (x < tam_cuanto * (niveles - 1)),  
        (x >= (niveles - 1))  
    ]
    funciones = [
        0, 
        np.round(y/tam_cuanto) * tam_cuanto,
        (niveles - 1) * tam_cuanto
    ]
    y_resultado = np.select(condicion,funciones)

    #devolver parte negariva
    y_resultado = y_resultado + minimo

    return x,y_resultado

#plotear(cuantizar(8,1/4,senoidal(0,1,300,3,0)))

def ejercicio2():
    fig, axes = plt.subplots(3, 1, figsize=(8, 10))  # grilla de 3x1

    plotear_grid(cuantizar(8, 1/4, senoidal(0, 1, 300, 3, 0)), axes[0], "Cuantización")
    plotear_grid(rectificacionOndaCompleta(senoidal(0, 1, 300, 3, 0)), axes[1], "Rectificación de Onda Completa")
    plotear_grid(invertir(senoidal(0, 1, 300, 3, 0)), axes[2], "Inversión")

    plt.tight_layout() 
    plt.show()

#ejercicio2()

def ejercicio3():
    
    tini = 0
    tfin = 0.1

    # si en 0.01 hay 9 muestreos
    # en 1 segundo hay 900
    fm = 900
    
    #frecuencia de señal: en 0.1s hubo 2 ciclos completos
    # si fs es ciclos completos por segundo
    # 0.1 => 2
    # 1 => 20
    fs = 20 
    
    phi = -2 * np.pi * fs * (0.007)
    a = 3 

    x,y = senoidal(tini,tfin,fm,fs,phi)
    plotear_stem((x,y * a))
    
#ejercicio3()

def ejercicio4():
    tini = 0
    tfin = 1
    fs = 5  # Hz
    phi = 0
    
    fm_list = [100, 25, 10, 4, 1, 0.5]
    
    fig, axes = plt.subplots(3, 2, figsize=(10, 10))
    
    axes = axes.ravel()
    for i, fm in enumerate(fm_list):
        t, y = senoidal(tini, tfin, fm, fs, phi)
        axes[i].plot(t, y)
        axes[i].set_title(f'Frecuencia Muestral: {fm}')
    
    plt.tight_layout()
    plt.show()

#ejercicio4()




def ejercicio5():
    
    tini = 0
    tfin = 2

    fm = 129

    fs = 4000
    phi = 0

    x,y = senoidal(tini,tfin,fm,fs,phi)
    plotear((x,y))
# Queda visualmente como si fuera una sinusoidal de 1 hz

#ejercicio5()

# EJERCICIO 6
def Iescalon(t):
    return 1 if t >= 0 and t < 1 else 0

def Ilineal(t):
    return 1 - abs(t) if abs(t) < 1 else 0


def Isinc(t):
    return np.sin(t)/t if t != 0 else 1


def interpolar(funcion_i, fm_i, muestras):
    t, s = muestras
    T = t[1] - t[0] # T o delta t seria el paso viejo
    Ti = 1/fm_i

    tam_intervalo = (t[-1] - t[0])
    n_muestras = int(tam_intervalo /Ti) # cuantas muestras van a haber con el nuevo paso

    t_interp = np.linspace(t[0], t[-1], n_muestras)  # conseguir los nuevos t con el nuevo paso
    s_interp = np.zeros(len(t_interp)) # inicializar los s en 0
    
    for i in range(len(t_interp)):
        for j in range(len(t)):
            s_interp[i] += s[j] * funcion_i((t_interp[i] - t[j]) / T)
    
    return t_interp, s_interp


    
def ejercicio6():
    
    tini = 0
    tfin = 6

    fm = 10

    fs = 1
    phi = 0

   
    plotear( interpolar(Isinc,4*fm, senoidal(tini,tfin,fm,fs,phi)))



ejercicio6()
