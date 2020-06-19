import tkinter as tk
from tkinter import *
from tkinter import Message ,Text
import os

root=Tk()

root.geometry("700x400")

def quit():
    root.destroy()

label1=tk.Label(root,text="Password",width=8,fg="white",bg="red",font=('times',20,'bold'))
label1.place(x=50,y=50)
text1=tk.Entry(root,fg="red",bg="red",font=('times',20,'bold'))
text1.place(x=200,y=50)

label2=tk.Label(root,text="Id",width=8,fg="white",bg="red",font=('times',20,'bold'))
label2.place(x=50,y=100)
text2=tk.Entry(root,fg="white",bg="red",font=('times',20,'bold'))
text2.place(x=200,y=100)

label3=tk.Label(root,text="Name",width=8,fg="white",bg="red",font=('times',20,'bold'))
label3.place(x=50,y=150)
text3=tk.Entry(root,fg="white",bg="red",font=('times',20,'bold'))
text3.place(x=200,y=150)

label4=tk.Label(root,text="Email",width=8,fg="white",bg="red",font=('times',20,'bold'))
label4.place(x=50,y=200)
text4=tk.Entry(root,fg="white",bg="red",font=('times',20,'bold'))
text4.place(x=200,y=200)

button1=tk.Button(root,text="Clear",width=8,fg="white",bg="red",font=('times',20,'bold'))
button1.place(x=500,y=50)

button2=tk.Button(root,text="Quit",command=quit,width=8,fg="white",bg="red",font=('times',20,'bold'))
button2.place(x=500,y=150)

button3=tk.Button(root,text="Add New",width=8,fg="white",bg="red",font=('times',20,'bold'))
button3.place(x=100,y=300)

button4=tk.Button(root,text="Delete",width=8,fg="white",bg="red",font=('times',20,'bold'))
button4.place(x=400,y=300)
root.mainloop()