import tkinter as tk
from tkinter import *
from tkinter import Message ,Text
import os
import cv2 as cv
import mysql.connector
import csv

mydb=mysql.connector.connect(host="127.0.0.1",port="3306",user="root",passwd="Sarath@1998",database="mine")
mycursor=mydb.cursor()


root=Tk()

root.geometry("700x400")

def add_new():
    Id=(text2.get())
    Name=(text3.get())
    Email=(text4.get())
    if(is_number(Id) and Name.isalpha()):
        cam = cv.VideoCapture(0)
        harcascadePath = "haarcascade_frontalface_default.xml"
        detector=cv.CascadeClassifier(harcascadePath)
        sampleNum=0
        while(True):
            ret, img = cam.read()
            gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)
            for (x,y,w,h) in faces:
                cv.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)        
                #incrementing sample number 
                sampleNum=sampleNum+1
                #saving the captured face in the dataset folder TrainingImage
                cv.imwrite("Images\ "+Name +"."+Id +'.'+ str(sampleNum) + ".jpg", gray[y:y+h,x:x+w])
                #display the frame
                cv.imshow('frame',img)
            #wait for 100 miliseconds 
            if cv.waitKey(100) & 0xFF == ord('q'):
                break
            # break if the sample number is morethan 100
            elif sampleNum>60:
                break
        cam.release()
        cv.destroyAllWindows() 
        res = "Images Saved for ID : " + Id +" Name : "+ Name
        row = (Id, Name,Email)
        sql="INSERT INTO student_database (Id,Name,Email) VALUES (%s,%s,%s)"
        mycursor.execute(sql,row)
        mydb.commit()
        mycursor.execute("SELECT * FROM student_database")
        data=mycursor.fetchall()
        with open('StudentDetails\StudentDetails.csv','w') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerow(["Id","Name","Email"])
            writer.writerows(data)
        f.close()
        message.configure(text= res)
    else:
        if(is_number(Id)):
            res = "Enter Alphabetical Name"
            message.configure(text= res)
        if(Name.isalpha()):
            res = "Enter Numeric Id"
            message.configure(text= res)

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