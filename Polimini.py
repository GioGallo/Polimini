import sys
import tkinter as tk
from tkinter.simpledialog import askstring

class Polimino(object):

    def __init__(self, iterable):
        self.quadrati = tuple(sorted(iterable))

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, repr(self.quadrati))

    def __iter__(self):
        return iter(self.quadrati)

    def __len__(self):
        return len(self.quadrati)

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __hash__(self):
        """Determina una chiave univoca per il polimino"""
        polimino = self.translate()
        chiave = polimino.chiave()
        for _ in range(3):
            polimino = polimino.ruota().translate()
            chiave = min(chiave, polimino.chiave())
        return chiave

    def chiave(self):
        return hash(self.quadrati)

    def ruota(self):
        """Ritorna il polimino ruotato in senso orario"""
        return Polimino((-y, x) for x, y in self)

    def translate(self):
        """Ritorna il polimino traslato rispetto a 0,0"""
        minX = min(s[0] for s in self)
        minY = min(s[1] for s in self)
        return Polimino((x-minX, y-minY) for x, y in self)

    def successivo(self):
        """Ritorna una lista di polimini cin grado superiore"""
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

    def grafica(self):
        """Rappresentazione grafica di un polimino"""
        polimino = self.translate()
        n = len(polimino)
        stampa = ""
        for y in range(n):
            stampa +="\n"
            for x in range(n):
                if((x,y) in polimino.quadrati):
                    stampa+="X"
                else:
                    stampa+="-"
        return stampa



def StampaPolimini(n):
    stato = 1
    polimini = set([Polimino(((0,0),))])

    while stato < n:
        stato += 1
        poliminiSuccessivi = set()
        for polimino in polimini:
            poliminiSuccessivi.update(polimino.successivo())
        polimini = poliminiSuccessivi

    max =0
    for polimino in polimini:
        print(polimino.grafica())
        #print(polimino.quadrati)
        lastY =0
        pos = []
        for index,quadrato in enumerate(polimino.quadrati,start=1):
            lastY=printPolimino(quadrato[0],quadrato[1],index,max)
            pos.append(lastY)
            print("LAST Y {}".format(lastY))

        pos.sort()
        max= pos[-1]
        print(max)
        max=printVerticalSpace(max + 5)
        
        

def printVerticalSpace(max):
    w.create_rectangle(0, max,500, max+40, fill="white", outline="")
    return max+45

def printPolimino(x,y,i,startPos):


    listX = []
    listY = []
    listX.append(x)
    listY.append(y)

    ultInsX = listX[-1]
    ultInsY = listY[-1]

    pezzoN = i

    if i == pezzoN:
        if x == -1:
            xInitPos = 5
        if x == 0:
            xInitPos = 35
        if x == 1: 
            xInitPos = 65

        if y == -1:
            yInitPos = startPos+5
        if y == 0:
            yInitPos = startPos+35
        if y == 1:
            yInitPos = startPos+65
        pezzoN = -1




    squareWidth = 30
    xFinPos = xInitPos + squareWidth
    yFinPos = yInitPos + squareWidth
    w.create_rectangle(xInitPos, yInitPos, xFinPos, yFinPos, fill="red")
    return yFinPos

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    name = askstring("Polimini", "Numero polimino")
    np = int(name)
    root.destroy()
    master = tk.Tk()
    canvas_width = 500
    canvas_height = 500
    w = tk.Canvas(master, width=canvas_width, height=canvas_height, bg="white")
    w.pack()

    StampaPolimini(np)
    tk.mainloop()