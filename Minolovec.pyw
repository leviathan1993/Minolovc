import sys

if sys.version_info[0] == 2: #Python 2.7.x
    from Tkinter import *
    import tkMessageBox as messagebox
else:
    from tkinter import *
    from tkinter import messagebox
import random
import time


class Gumb:
    def __init__(self, gumb, mina, sosedi):
        self.gumb = gumb
        self.mina = mina
        self.sosedi = sosedi

    def __repr__(self):
        return 'Gumb({0}, {1}, {2})'.format(self.gumb, self.mina, self.sosedi)

class Minesweeper():
    def __init__(self, master, vrstice,stolpci,mine):
        self.igra = False
        self.master = master
        self.st_vrstic = vrstice
        self.st_stolpcev = stolpci
        self.mines = mine
        #Nastavi nove vrednosti -Podatke uporabi iz nastavitev
        self.st_vrstic1234 = vrstice
        self.st_stolpcev1234 = stolpci
        self.mines1234=mine
        # Full screen app
        self.state = False
        self.master.bind("<F11>", self.toggle_fullscreen)
        self.master.bind("<Escape>", self.end_fullscreen)
        #konfiguracija menija
        self.menu = Menu(master)
        master.config(menu=self.menu)
        self.menu.add_command(label="Quit", command=root.destroy)
        self.menu.add_command(label="Reset", command=self.nova_igra)
        self.menu.add_command(label="Nastavi", command=self.nastavitve)
        self.menu.add_command(label="Štoparica", command=self.stoparica)

        self.nova_igra()

    def stoparica(self):
        okno = Timer(self)

    def nastavitve(self):
        okno = Nastavitve(self)

    def zbrisi_polje(self):
        '''Zbriše polje'''
        for vrstica in range(self.st_vrstic):
            for stolpec in range(self.st_stolpcev):
                self.buttons[vrstica][stolpec].gumb.destroy()
        self.buttons=None

    def nova_igra(self):
##        if self.igra:
##            self.izbrane_mine = None
##            gumb = None
##            self.zbrisi_polje()
        #Uporabi podatke iz okna nastavitve


        self.mines=self.mines1234
        self.st_vrstic = self.st_vrstic1234
        self.st_stolpcev = self.st_stolpcev1234
        self.buttons = [[None for i in range(self.st_stolpcev)] for j in range(self.st_vrstic)]
        self.izbrane_mine = random.sample([i for i in range(self.st_vrstic * self.st_stolpcev)], self.mines1234)
        self.st_poklikanih = self.st_vrstic * self.st_stolpcev
        # print("nova igra")
        num_proximity_mines = 0
        frame = Frame(self.master)
        Grid.rowconfigure(root, 0, weight=1)
        Grid.columnconfigure(root, 0, weight=1)
        frame.grid(row=0, column=0, sticky=N + S + E + W)
        self.label1 = Label(frame, text="Minesweeper")
        self.label1.grid(row=0, column=0, columnspan=10)
        st = 0
        for vrstica in range(self.st_vrstic):
            Grid.rowconfigure(frame, vrstica, weight=1)
            for stolpec in range(self.st_stolpcev):
                Grid.columnconfigure(frame, stolpec, weight=1)
                mine = False
                if st in self.izbrane_mine:
                    mine = True

                gumb = Gumb(Button(frame, bg="green", width=3), mine, num_proximity_mines)  # Objekt

                self.buttons[vrstica][stolpec] = gumb
                # GLUPI PYTHON NAROBE DELA SPREMENLJIVKE V LAMBDAH
                self.buttons[vrstica][stolpec].gumb.bind('<Button-1>',
                                                         (lambda v, s: lambda e: self.lclick(v, s))(vrstica, stolpec))
                self.buttons[vrstica][stolpec].gumb.bind('<Button-3>',
                                                         (lambda v, s: lambda e: self.rclick(v, s))(vrstica, stolpec))
                self.buttons[vrstica][stolpec].gumb.grid(row=vrstica, column=stolpec, sticky=N + S + E + W)
                st+=1

        for v in range(self.st_vrstic):
            for s in range(self.st_stolpcev):
                self.buttons[v][s].sosedi = self.sosednje_mine(v, s)

        self.master.attributes("-topmost", True)

    def sosedi(self, vrstica, stolpec):
        sez = [(vrstica - 1, stolpec - 1), (vrstica - 1, stolpec), (vrstica - 1, stolpec + 1),
               (vrstica, stolpec - 1), (vrstica, stolpec + 1),
               (vrstica + 1, stolpec - 1), (vrstica + 1, stolpec), (vrstica + 1, stolpec + 1)]
        return [(v, s) for (v, s) in sez if 0 <= v < self.st_vrstic and 0 <= s < self.st_stolpcev]

    def sosednje_mine(self, vrstica, stolpec):
        """Stevilo sosednjih polj, ki so mina"""
        m = 0
        for (v, s) in self.sosedi(vrstica, stolpec):
            if self.buttons[v][s].mina == 1: m += 1
        return m

    def lclick(self, vrstica, stolpec, preveri_konec=True):
        a = self.st_poklikanih == self.st_vrstic*self.st_stolpcev
        if a: self.t1 = time.time()

        sez = self.buttons[vrstica][stolpec]
        # print(sez)
        if sez.gumb["bg"] == "green":
            # polje se ni odkrito, ga odkrijemo
            self.st_poklikanih -= 1
            if sez.mina == 1 and a == True:
                sez.mina=0
                self.mines-=1
                m = sez.sosedi  # stevilo sosednjih min
                if m != 0: sez.gumb.config(text=str(m))
                sez.gumb.config(bg="green yellow")
            elif sez.mina == 1:
                # stopili smo na mino
                for i in range(len(self.buttons)):
                    for x in range(len(self.buttons[i])):
                        if self.buttons[i][x].mina == 1:
                            self.buttons[i][x].gumb.config(bg="red")
                self.konec_igre(False)
            else:
                # polje je bilo prazno
                m = sez.sosedi  # stevilo sosednjih min
                if m != 0: sez.gumb.config(text=str(m))
                sez.gumb.config(bg="green yellow")
                if m == 0:
                    # print ("odpiramo sosede od {0}".format((vrstica,stolpec)))
                    for (v, s) in self.sosedi(vrstica, stolpec):
                        self.lclick(v, s, preveri_konec=False)

        # ali je konec igre?
        if preveri_konec and self.st_poklikanih-self.mines == 0:
            self.konec_igre(True)

    def rclick(self, vrstica, stolpec):
        sez = self.buttons[vrstica][stolpec]
        if sez.gumb["bg"] == "green":
            sez.gumb.config(bg="blue", text=chr(9873) if sys.version_info[0] == 3 else ':)')
            self.st_poklikanih -= 1
            if sez.mina == 1:
                self.mines -= 1

        elif sez.gumb["bg"] == "blue":
            if sez.gumb == 1:
                self.mines += 1
            self.st_poklikanih += 1
            sez.gumb.config(bg="green", text="")

        if self.st_poklikanih == 0 and self.mines == 0:
            self.konec_igre(True)

    def konec_igre(self, od_kje):
        self.t2 = time.time()
        self.igra = True
        if od_kje:
            result = messagebox.askyesno('Winner!', 'Igram znova?\nČas igranja {0}'.format(int(self.t2-self.t1)))
        else:
            result = messagebox.askyesno('Looser!', 'Igram znova?\nČas igranja {0}'.format(int(self.t2-self.t1)))
        if result:
            self.zbrisi_polje()
            self.nova_igra()
            return
        else:
            self.master.destroy()
            return

    def toggle_fullscreen(self, event=None):
        self.state = not self.state  # Just toggling the boolean
        self.master.attributes("-fullscreen", self.state)
        return "break"

    def end_fullscreen(self, event=None):
        self.state = False
        self.master.attributes("-fullscreen", False)
        return "break"

class Nastavitve():
    def __init__(self, minesweeper):
        self.minesweeper = minesweeper
        self.top = Toplevel()
        self.top.title("Nastavi")
        self.top.attributes("-topmost", True)

        frame = Frame(self.top)

        frame.pack()

        Label(frame, text="Število vrstic").grid(row=0, column=0, sticky=W)
        Label(frame, text="Število stolpcev").grid(row=1, column=0, sticky=W)
        Label(frame, text="Število min").grid(row=2, column=0, sticky=W)
##        Button(frame, text="+").grid(row=0, column=2)
##        Button(frame, text="-").grid(row=1, column=2)
        self.e1 = Entry(frame)
        self.e2 = Entry(frame)
        self.e3 = Entry(frame)

        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        self.e3.grid(row=2, column=1)

        b = Button(self.top, text="OK", command=self.callback)
        b.pack()

    def callback(self):
        self.minesweeper.st_vrstic1234 = int(self.e1.get())
        self.minesweeper.st_stolpcev1234 = int(self.e2.get())
        self.minesweeper.mines1234 = max(int(0.1*self.minesweeper.st_stolpcev1234*self.minesweeper.st_vrstic1234),min(int(self.e3.get()),self.minesweeper.st_stolpcev1234*self.minesweeper.st_vrstic1234)) #Število min ne sme biti večje od velikosti igralnega polja, vsaj 10% min.

        self.top.destroy()
        self.minesweeper.zbrisi_polje()
        self.minesweeper.nova_igra()

##Timer

class Timer:
    def __init__(self,minesweeper):
        self.sec = 0
        self.minesweeper = minesweeper
        self.timer = Toplevel()
        self.timer.title("Čas")
        self.timer.attributes("-topmost", True)
        self.time = Label(self.timer, fg='green')
        self.time.pack()
        Button(self.timer, fg='blue', text='Start', command=self.tick).pack()



    def tick(self):
        self.sec += 1
        self.time['text'] = self.sec
        # Take advantage of the after method of the Label
        self.time.after(1000, self.tick)

root = Tk()
root.title('Minolovec')
minesweeper = Minesweeper(root,10,10,10)
root.mainloop()
