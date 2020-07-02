import tkinter as tk
from tkinter import ttk, messagebox

fen = tk.Tk()
fen.geometry("300x300")
fen.title("Test")


a = messagebox.askyesnocancel("Save ?","Sauvegarder les changements ?")
print(a)

# a = filedialog.asksaveasfilename(initialdir='./Ressources/Maps',title='select file')
# print(a)






fen.mainloop()