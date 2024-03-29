import os
from tkinter import *
import tkinter.filedialog
import tkinter as tk
import shutil
import sqlite3


class ParentWindow(Frame):
    def __init__(self, master):
        Frame.__init__(self)

        self.master = master
        self.master.minsize(500, 200)
        self.master.maxsize(500, 200)
        self.master.title('Check Files')
        self.master.config(bg='lightgray')

        self.varSource = str()
        self.varDest = str()

        self.txtBrowse1 = Entry(self.master, text=self.varSource, font=("Helvetica", 16), fg='black', bg='white')
        self.txtBrowse1.grid(row=3, column=1, rowspan=1, columnspan=5, padx=(30, 40), pady=(30, 0))

        self.txtBrowse2 = Entry(self.master, text=self.varDest, font=("Helvetica", 16), fg='black', bg='white')
        self.txtBrowse2.grid(row=4, column=1, rowspan=1, columnspan=6, padx=(30, 40), pady=(30, 0))

        self.btnBrowse1 = Button(self.master, text="Select Source", width=15, height=1, command=lambda: onSelect(self))
        self.btnBrowse1.grid(row=3, column=0, padx=(30, 0), pady=(30, 0))

        self.btnBrowse2 = Button(self.master, text="Select Destination", width=15, height=1,
                                 command=lambda: onSelect2(self))
        self.btnBrowse2.grid(row=4, column=0, padx=(30, 0), pady=(30, 0))

        self.btnCheckFiles = Button(self.master, text="Check for files...", width=15, height=2,
                                    command=lambda: onCheck(self))
        self.btnCheckFiles.grid(row=5, column=1, padx=(30, 0), pady=(30, 0))


#  Allow's user to browse computer to select source directory

def onSelect(self):
    fileName1 = tkinter.filedialog.askdirectory()
    self.txtBrowse1.insert(0, fileName1)


#  Allow's user to browse computer to select destination directory
def onSelect2(self):
    fileName2 = tkinter.filedialog.askdirectory()
    self.txtBrowse2.insert(0, fileName2)


def onCheck(self):
    source = self.txtBrowse1.get()
    source2 = self.txtBrowse2.get()
    dirs = os.listdir(source)
    for file in dirs:
        if file.endswith(".txt"):
            print(file)
            abPath = (os.path.join(source, file))
            modification_time = os.path.getmtime(abPath)
            print(modification_time)

            destination = shutil.move(abPath, source2)
            print(destination)

            conn = sqlite3.connect('Moved_Files.db')

            with conn:
                cur = conn.cursor()
                cur.execute("CREATE TABLE IF NOT EXISTS tbl_moved_files(\
                    ID INTEGER PRIMARY KEY AUTOINCREMENT, \
                    col_files TEXT,\
                    col_timeStamp TEXT \
                    );")

                conn.commit()
            conn.close()

            conn = sqlite3.connect('Moved_Files.db')

            with conn:
                cur = conn.cursor()
                cur.execute("INSERT INTO tbl_moved_files(col_files, col_timeStamp) VALUES (?,?)",
                            (abPath, modification_time))

                print(cur.fetchall())




if __name__ == "__main__":
    root = tk.Tk()
    App = ParentWindow(root)
    root.mainloop()
