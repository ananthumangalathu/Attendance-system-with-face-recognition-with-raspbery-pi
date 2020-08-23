# Create gmail id, mysql database,Google firebase storage
# student_database- database name
# mydata- Table
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

yagmail.register("Gmail Id","Password")
yag=yagmail.SMTP("Gmail Id")

mydb=mysql.connector.connect(host="Your host",user="Your User",passwd="Your Password",database="student_database")
mycursor=mydb.cursor(buffered=True)

date = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d')

config={"Google firebase connection key"}
firebase=pyrebase.initialize_app(config)
storage=firebase.storage()

window=Tk() 
window.geometry("700x400")
window.title("Attendance System")

message1 = tk.Label(window,text="",bg="red"  ,fg="white"  ,width=50  ,height=4,font=('times', 15, ' bold '))
message1.place(x=50,y=20)
def add_new():
    os.system("python second.py")

def convert(s): 
  
    # initialization of string to "" 
    new = "" 
  
    # traverse in the string  
    for x in s: 
        new += x  
  
    # return string  
    return new

def mark_attendance():
    recognizer = cv.face.LBPHFaceRecognizer_create()#cv2.createLBPHFaceRecognizer()
    recognizer.read("ImageLabel\Trainner.yml")
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv.CascadeClassifier(harcascadePath);    
    df=pd.read_csv("StudentDetails\StudentDetails.csv")
    cam = cv.VideoCapture(0)
    font = cv.FONT_HERSHEY_SIMPLEX          
    while(True):
        ret, im =cam.read()
        gray=cv.cvtColor(im,cv.COLOR_BGR2GRAY)
        faces=faceCascade.detectMultiScale(gray, 1.2,5)    
        for(x,y,w,h) in faces:
            cv.rectangle(im,(x,y),(x+w,y+h),(225,0,0),2)
            Id, conf = recognizer.predict(gray[y:y+h,x:x+w])                                   
            if(conf < 60):  
                mycursor.execute("SELECT Name FROM mydata WHERE Id='"+str(Id)+"'")
                result=mycursor.fetchone()
                Name=convert(result)           
                cv.putText(im,str(Name),(x,y+h), font, 1,(255,255,255),2)
                message1.configure(text="Attendance marked for"+str(Name)+" "+str(Id))
                mycursor.execute("UPDATE mydata SET Status='PRESENT' where Id='"+str(Id)+"'")
                mydb.commit()
            else:
                Id='Unknown'                
                tt=str(Id)  
            if(conf > 75):
                noOfFile=len(os.listdir("ImagesUnknown"))+1
                cv.imwrite("ImagesUnknown\Image"+str(noOfFile) + ".jpg", im[y:y+h,x:x+w])                        
        cv.imshow('image',im) 
        if cv.waitKey(100) & 0xFF == ord('q'):
                break
        cam.release()
    cv.destroyAllWindows()
    mycursor.execute("SELECT Id,Name,Status FROM mydata")
    data=mycursor.fetchall()
    with open("Attendance\ " +date+ ".csv",'w') as f:
        a = csv.writer(f, delimiter=',')
        a.writerow(["Id","Name","Status"])  ## etc
        a.writerows(data)
    f.close()
        
def attendancesheet():
    mycursor.execute("SELECT Id,Name,Status FROM mydata")
    data=mycursor.fetchall()
    with open("Attendance\ " +date+ ".csv",'w') as f:
        a = csv.writer(f, delimiter=',')
        a.writerow(["Id","Name","Status"])  ## etc
        a.writerows(data)
    f.close()
    path_on_cloud="Attendance/ " +date+ ".csv"
    path_local="Attendance\ " +date+ ".csv"
    storage.child(path_on_cloud).put(path_local)
    mycursor.execute("SELECT Name,Email FROM mydata WHERE Status='ABSENT'")
    result=mycursor.fetchall()
    for Name,Email in result:
        content=['Your child '+str(Name)+' was absent today']
        yag.send(Email,'absent',content)
    sql = "UPDATE mydata SET Status='ABSENT' where Status='PRESENT'"
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