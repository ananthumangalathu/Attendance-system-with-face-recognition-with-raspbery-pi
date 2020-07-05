import tkinter as tk
from tkinter import *
from tkinter import Message ,Text
import os
import cv2 as cv
import pandas as pd
import datetime
import time
import mysql.connector
import csv
import pyrebase
import yagmail

yagmail.register("classattendance27@gmail.com","attendance@geck")
yag=yagmail.SMTP("classattendance27@gmail.com")

mydb=mysql.connector.connect(host="192.168.56.1",port="3306",user="sarath",passwd="NJANADA@008",database="student_database")
mycursor=mydb.cursor()

date = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d')

config={
    "apiKey": "AIzaSyAOtCeT6JpkIUFSbQbQ6xNp4HNjyEtnbMM",
    "authDomain": "attendence-system-270913.firebaseapp.com",
    "databaseURL": "https://attendence-system-270913.firebaseio.com",
    "projectId": "attendence-system-270913",
    "storageBucket": "attendence-system-270913.appspot.com",
    "messagingSenderId": "861579886336",
    "appId": "1:861579886336:web:3aeab2978154da12a37de5",
    "measurementId": "G-QZH8G1NGT4"
    }
firebase=pyrebase.initialize_app(config)
storage=firebase.storage()

window=Tk() 
window.geometry("700x400")

message1 = tk.Label(window,text="",bg="red"  ,fg="white"  ,width=50  ,height=4,font=('times', 15, ' bold '))
message1.place(x=50,y=20)
def add_new():
    os.system("python second.py")

def mark_attendance():
    recognizer = cv.face.LBPHFaceRecognizer_create()#cv2.createLBPHFaceRecognizer()
    recognizer.read("ImageLabel\Trainner.yml")
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv.CascadeClassifier(harcascadePath);    
    df=pd.read_csv("StudentDetails\StudentDetails.csv")
    cam = cv.VideoCapture(0)
    font = cv.FONT_HERSHEY_SIMPLEX           
    while True:
        ret, im =cam.read()
        gray=cv.cvtColor(im,cv.COLOR_BGR2GRAY)
        faces=faceCascade.detectMultiScale(gray, 1.2,5)    
        for(x,y,w,h) in faces:
            cv.rectangle(im,(x,y),(x+w,y+h),(225,0,0),2)
            Id, conf = recognizer.predict(gray[y:y+h,x:x+w])                                   
            if(conf < 60):  
                aa=df.loc[df['Id'] == Id]['Name'].values
                tt=str(Id)+"-"+aa
                mycursor.execute("SELECT Name FROM student_database WHERE Id=Id")
                Name=mycursor.fetchone()
                sql = "UPDATE student_database SET Status='PRESENT' where Id=Id"
                mycursor.execute(sql)
                mydb.commit()
            else:
                Id='Unknown'                
                tt=str(Id)  
            if(conf > 75):
                noOfFile=len(os.listdir("ImagesUnknown"))+1
                cv.imwrite("ImagesUnknown\Image"+str(noOfFile) + ".jpg", im[y:y+h,x:x+w])            
            cv.putText(im,str(Name),(x,y+h), font, 1,(255,255,255),2)
            message1.configure(text="Attendance marked for"+str(Name)+" "+str(Id))            
        cv.imshow('im',im) 
        if (cv.waitKey(5000)):
            break
        cam.release()
    cv.destroyAllWindows()
    mycursor.execute("SELECT Id,Name,Status FROM student_database")
    data=mycursor.fetchall()
    with open("Attendance\ " +date+ ".csv",'w') as f:
        a = csv.writer(f, delimiter=',')
        a.writerow(["Id","Name","Status"])  ## etc
        a.writerows(data)
    f.close()
    message1.configure(text="Attendance marked for"+str(Name)+" "+str(Id))    

def attendancesheet():
    path_on_cloud="Attendance/ " +date+ ".csv"
    path_local="Attendance\ " +date+ ".csv"
    storage.child(path_on_cloud).put(path_local)
    mycursor.execute("SELECT Name,Email FROM student_database WHERE Status='ABSENT'")
    result=mycursor.fetchall()
    for Name,Email in result:
        content=['Your child '+str(Name)+' was absent today']
        yag.send(Email,'absent',content)
    sql = "UPDATE student_database SET Status='ABSENT' where Status=PRESENT"
    mycursor.execute(sql)
    mydb.commit()
    message1.configure(text="Attendance sheet generated and uploaded to cloud")

button1=tk.Button(window,text="ADD NEW",width=20,height=2,font=("times new roman",20),bg="red",fg='white',command=add_new)
button1.place(x=20,y=150)

button2=tk.Button(window,text="MARK ATTENDANCE",width=20,height=2,font=("times new roman",20),bg="red",fg='white',command=mark_attendance)
button2.place(x=380,y=150)

button3=tk.Button(window,text="ATTENDANCE SHEET",width=20,height=2,font=("times new roman",20),bg="red",fg='white',command=attendancesheet)
button3.place(x=20,y=250)

button4=tk.Button(window,text="QUIT",width=20,height=2,font=("times new roman",20),bg="red",fg='white',command=window.destroy)
button4.place(x=380,y=250)

window.mainloop()