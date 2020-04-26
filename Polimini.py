#importazione librerie
import sys
import random
import tkinter as tk                        #libreria grafica
from tkinter.simpledialog import askstring  #modulo specifico della libreria grafica per creare il pop up

#Classe che rappresenta un polimino 
class Polimino(object):

    #Costruttore della classe Polimino che imposta le coordinate dei quadrati
    #che gli appartengono (tuple) in modo ordinato
    def __init__(self, iterable):
        self.quadrati = tuple(sorted(iterable))

    #Ritorna l’iterator dei quadrati del polimino
    def __iter__(self):
        return iter(self.quadrati)

    #Ritorna se l’hash del polimino corrente è uguale all’hash del polimino
    #passato in input
    def __eq__(self, other):
        return hash(self) == hash(other)

    #Questa funzione permette di calcolare una chiave univoca per ogni polimino in base alle
    #coordinate dei quadrati che gli appartengono. Se si presentano due polimini specchiati
    #l’hash sarebbe lo stesso così da semplificare l’aggregazione delle soluzioni corrette
    def __hash__(self):
        polimino = self.translate()
        chiave = polimino.chiave()
        for n in range(3):
            polimino = polimino.ruota().translate()
            chiave = min(chiave, polimino.chiave())
        return chiave

    #Funzione che restituisce la chiave univoca del polimino
    def chiave(self):
        return hash(self.quadrati)

    #Funzione che ritorna il polimino ruotato in senso orario
    def ruota(self):
        return Polimino((-y, x) for x, y in self)

    #Funzione che ritorna il polimino traslato rispetto a (0,0)
    def translate(self):
        minX = min(s[0] for s in self)
        minY = min(s[1] for s in self)
        return Polimino((x-minX, y-minY) for x, y in self)

    #Ritorna la lista di polimini di grado superiore, lavorando sui lati dei
    #quadrati
    def successivo(self):
        polimini = []
        for quadrato in self:
            vicini = (vicino for vicino in (
                (quadrato[0] + 1, quadrato[1]),
                (quadrato[0] - 1, quadrato[1]),
                (quadrato[0], quadrato[1] + 1),
                (quadrato[0], quadrato[1] - 1),
            ) if vicino not in self)
            for vicino in vicini:
                polimini.append(
                    Polimino(list(self) + [vicino])
                )
        return polimini    

#Crea i polimini del grado richiesto e li stampa nel canvas per la
#visualizzazione
def StampaPolimini(n):
    ordine = 1
    polimini = set([Polimino(((0,0),))])        #Inizializzo una lista di polimini con il polimino di ordine 1

    while ordine < n:                           #Finchè l'ordine dei polimini è minore del numero inserito dall'utente
        ordine += 1                             #Aumento l'ordine
        poliminiSuccessivi = set()              #Inizializzzo una lista vuota di polimini 
        for polimino in polimini:               
            poliminiSuccessivi.update(polimino.successivo()) #aumento l'ordine del polimino
        polimini = poliminiSuccessivi           #Aggiorno la lista iniziale con i polimini di ordine successivo

    max =0                                      #coordinata Y massima del canvas
    for polimino in polimini:
        color = "#{:06x}".format(random.randint(0, 0xFFFFFF)) #Prendo un colore random
        lastY =0
        pos = []
        minY =0
        minX=0
        for quadrato in polimino.quadrati:      #ciclo per calcolare le coordinate x e y minime del polimino
            tempY=quadrato[1]
            tempX=quadrato[0]
            if(tempY<minY):
                minY=tempY
            if(tempX<minX):
                minX=tempX
        for quadrato in polimino.quadrati:      #ciclo per stampare i quadrati del polimino nel canvas
            lastY=printPolimino(quadrato[0],quadrato[1],color,max,minY,minX) 
            pos.append(lastY)

        pos.sort()
        max= pos[-1]                            #prendo l'ultima posizione , ovvero il valore più grande
        max=printVerticalSpace(max + 5)         #Aggiungo uno spazio bianco e aggiorno max
    return max
        
        
#funzione per stampare uno spazio bianco tra un polimino e l'altro
def printVerticalSpace(max):
    canvas.create_rectangle(0, max,500, max+40, fill="white", outline="")
    return max+45

#funzione che viene richiamata per stampare ogni singolo quadratino
#gli vengono passati i parametri x e y per la posizione del quadratino
#il colore per far cambiare il colore al quadrato
#startPos
#minX e minY servono per capire di quanto spostarsi in base al pezzo che arriva
def printPolimino(x,y,color,startPos,minY,minX):

    xInitPos = 5+((x-minX)*30)
    yInitPos = startPos+5+((y-minY)*30)
    
    #definizione punti finali in base ai parametri settati sopra
    squareWidth = 30
    xFinPos = xInitPos + squareWidth
    yFinPos = yInitPos + squareWidth
    #creazione quadratino effettivo in base alle posizioni passate
    canvas.create_rectangle(xInitPos, yInitPos, xFinPos, yFinPos, fill=color)
    return yFinPos


#Funzione che viene richiamata per chiedere all'utente il numero di quadratini
#da cui deve essere formato il polimino
def FormInserimento():
    #creazione della form per l'input del numero N per la creazione dei Polimino
    root = tk.Tk()
    root.withdraw()
    name = askstring("Polimini", "Numero polimino")
    np = int(name)
    root.destroy()
    #fine form inserimento
    return np

#Funzione che viene richiamata per creare il canvas dove mostrare i polimini
def InitCanvas(np):
    master = tk.Tk()
    master.title("Generazione per " + str(np) + " polimini")
    master.iconbitmap(default='./Polimini/Cattura.ico')
    frame=tk.Frame(master,width=800,height=800)                                             #crezione del frame per il contenimento del canvas
    frame.pack(expand=True, fill="both")
    canvas=tk.Canvas(frame,bg='#FFFFFF',width=800,height=800,scrollregion=(0,0,300,300))    #creazione del canvas e inserimento nel frame, definendo dimensioni e scrollabilità
    vbar=tk.Scrollbar(frame,orient="vertical")                                              #creazione scrollbarverticale
    vbar.pack(side="right",fill="y")
    vbar.config(command=canvas.yview)
    canvas.config(yscrollcommand=vbar.set)
    canvas.pack(side="left",expand=True,fill="both")
    return canvas


if __name__ == "__main__":
    np=FormInserimento()
    #inizializzazione canvas per mostrare i polimini
    canvas=InitCanvas(np)
    max=StampaPolimini(np)                                                                  #ricezione della posizione Y dell'ultimo quadratino
    canvas.configure(scrollregion=(0,0,max,max))                                            #aggiorno la regione per lo scroll e la facio arrivare fino all'ultimo quadratino
    tk.mainloop()                                                                           #funzione necessaria per il mantenimento della finestra attiva