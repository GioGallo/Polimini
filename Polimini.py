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

    for polimino in polimini:
        print(polimino.grafica())
        print(polimino)

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    name = askstring("Polimini", "Numero polimino")
    np = int(name)
    root.destroy()

    StampaPolimini(np)