import sys
import random
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
        """Ritorna una lista di polimini con grado superiore"""
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
        color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
        lastY =0
        pos = []
        minY =0
        minX=0
        for quadrato in polimino.quadrati:
            tempY=quadrato[1]
            tempX=quadrato[0]
            if(tempY<minY):
                minY=tempY
            if(tempX<minX):
                minX=tempX
        for quadrato in polimino.quadrati:
            lastY=printPolimino(quadrato[0],quadrato[1],color,max,minY,minX)
            pos.append(lastY)

        pos.sort()
        max= pos[-1]
        max=printVerticalSpace(max + 5)
    return max
        
        

def printVerticalSpace(max):
    canvas.create_rectangle(0, max,500, max+40, fill="white", outline="")
    return max+45

def printPolimino(x,y,color,startPos,minY,minX):

    if(x==minX):
        xInitPos = 5
    else:
        diff = x-minX
        xInitPos = 5
        xInitPos+= diff*30

    if(y == minY):
        yInitPos = startPos+5
    else:
        diff = y-minY
        yInitPos = startPos+5
        yInitPos+= diff*30
        
    squareWidth = 30
    xFinPos = xInitPos + squareWidth
    yFinPos = yInitPos + squareWidth
    canvas.create_rectangle(xInitPos, yInitPos, xFinPos, yFinPos, fill=color)
    return yFinPos

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    name = askstring("Polimini", "Numero polimino")
    np = int(name)
    root.destroy()

    master = tk.Tk()

    frame=tk.Frame(master,width=800,height=800)
    frame.pack(expand=True, fill="both")
    canvas=tk.Canvas(frame,bg='#FFFFFF',width=800,height=800,scrollregion=(0,0,300,300))
    vbar=tk.Scrollbar(frame,orient="vertical")
    vbar.pack(side="right",fill="y")
    vbar.config(command=canvas.yview)
    canvas.config(width=800,height=800)
    canvas.config(yscrollcommand=vbar.set)
    canvas.pack(side="left",expand=True,fill="both")


    max=StampaPolimini(np)

    canvas.configure(scrollregion=(0,0,max,max))
    tk.mainloop()