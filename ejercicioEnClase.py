import numpy as np
import matplotlib.pyplot as plt

def CapaImg(img:np.array, Capa:int)->np.array:
    """ Nombre: CapaImg
        Objetivo: Extraer una capa de una imagen
        Argumentos: img --> imagen a procesar
        
        Retorna: imgCapa --> imagen con la capa seleccionada
        Ejemplo de uso: CapaR=pi.CapaImg(MiImagen,0)
                        plt.imshow(CapaR)
                        plt.show()
    """
    fil, col, cap= img.shape
    imgCapa= np.zeros((fil, col, 3))
    imgCapa[:,:,Capa]= img[:,:,Capa]
    return imgCapa

def BrilloImg(img:np.array, Brillo:float)->np.array:
    """ Nombre: Brillo
    """
    Copiaimg:np.array=np.copy(img)
    return(Copiaimg+Brillo)

def AjusteCanal(img:np.array, brillo:float, capa:int)->np.array:
    """
    """
    Copiaimg:np.array=np.copy(img)
    Copiaimg[:,:,capa]=Copiaimg[:,:,capa]+brillo
    return Copiaimg

def Contraste(img:np.array, contraste:float,tipo:int):
    """
    """
    if (tipo==0):
        img= contraste*np.log10(1+img)
    else:
        img= contraste*np.exp(img-1)
    return img
