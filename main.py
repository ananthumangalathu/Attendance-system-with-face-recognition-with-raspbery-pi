import tkinter as tk
from tkinter import *
from tkinter import Message ,Text
import os

window=Tk() 
window.geometry("700x400")

def add_new():
    os.system("python second.py")
button1=tk.Button(window,text="ADD NEW",width=40,height=2,font=("times new roman",20),bg="red",fg='white',command=add_new)
button1.place(x=50,y=10)

button2=tk.Button(window,text="MARK ATTENDANCE",width=40,height=2,font=("times new roman",20),bg="red",fg='white',command="")
button2.place(x=50,y=110)

button3=tk.Button(window,text="ATTENDANCE SHEET",width=40,height=2,font=("times new roman",20),bg="red",fg='white',command="")
button3.place(x=50,y=210)

button4=tk.Button(window,text="QUIT",width=40,height=2,font=("times new roman",20),bg="red",fg='white',command=window.destroy)
button4.place(x=50,y=310)

window.mainloop()