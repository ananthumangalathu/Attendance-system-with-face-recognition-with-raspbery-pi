import tkinter as tk
from tkinter import *
from tkinter import Message ,Text
import os
import cv2 as cv
import mysql.connector
import csv
import numpy as np
from PIL import Image, ImageTk
import time
import pyrebase

mydb=mysql.connector.connect(host="192.168.56.1",port="3306",user="sarath",passwd="NJANADA@008",database="student_database")
mycursor=mydb.cursor(buffered=True)

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

root=Tk()
root.geometry("700x400")

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

message1 = tk.Label(root,text="",bg="red"  ,fg="white"  ,width=30  ,height=2,font=('times', 15, ' bold '))
message1.place(x=50,y=250)

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    return False

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
        row = (Id, Name,Email)
        sql="INSERT INTO student_database (Id,Name,Email) VALUES (%s,%s,%s)"
        mycursor.execute(sql,row)
        mydb.commit()
        mycursor.execute("SELECT Id,Name,Email FROM student_database")
        data=mycursor.fetchall()
        with open('StudentDetails\StudentDetails.csv','w') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerow(["Id","Name","Email"])
            writer.writerows(data)
        f.close()
        message1.configure(text="Images Saved for ID : " + Id +" Name : "+ Name)
    else:
        if(is_number(Id)):
            message1.configure(text="Enter Alphabetical Name")
        if(Name.isalpha()):
            message1.configure(text="Enter Numeric Id")

def TrainImages():
    recognizer = cv.face_LBPHFaceRecognizer.create()#recognizer = cv2.face.LBPHFaceRecognizer_create()#$cv2.createLBPHFaceRecognizer()
    harcascadePath = "haarcascade_frontalface_default.xml"
    detector =cv.CascadeClassifier(harcascadePath)
    faces,Id = getImagesAndLabels("Images")
    recognizer.train(faces, np.array(Id))
    recognizer.save("ImageLabel\Trainner.yml")
    message1.configure(text="Trainning compleated")
    
def getImagesAndLabels(path):
    #get the path of all the files in the folder
    imagePaths=[os.path.join(path,f) for f in os.listdir(path)] 
    #print(imagePaths)
    
    #create empth face list
    faces=[]
    #create empty ID list
    Ids=[]
    #now looping through all the image paths and loading the Ids and the images
    for imagePath in imagePaths:
        #loading the image and converting it to gray scale
        pilImage=Image.open(imagePath).convert('L')
        #Now we are converting the PIL image into numpy array
        imageNp=np.array(pilImage,'uint8')
        #getting the Id from the image
        Id=int(os.path.split(imagePath)[-1].split(".")[1])
        # extract the face from the training image sample
        faces.append(imageNp)
        Ids.append(Id)        
    return faces,Ids

def cloudupload():
    path_on_cloud="StudentDetails/StudentDetails.csv"
    path_local="StudentDetails\StudentDetails.csv"
    storage.child(path_on_cloud).put(path_local)
    message1.configure(text="Students list uploaded")

def quit():
    TrainImages()
    time.sleep(3)
    cloudupload()
    time.sleep(3)
    root.destroy()

def clear():
    text2.delete(0, 'end')
    text3.delete(0, 'end')
    text4.delete(0, 'end')
    
def delete():
    Id=(text2.get())
    mycursor.execute("SELECT name FROM student_database WHERE Id=Id")
    name=mycursor.fetchone()
    Name=''.join(name)
    samplenum=1
    while (samplenum<=61):
        os.remove("Images/ "+str(Name) +"."+Id +'.'+ str(samplenum) + ".jpg")
        samplenum=samplenum+1
    sql = "DELETE FROM student_database WHERE Id=Id"
    mycursor.execute(sql)
    mydb.commit()
    mycursor.execute("SELECT Id,Name,Email FROM student_database")
    data=mycursor.fetchall()
    with open('StudentDetails\StudentDetails.csv','w') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(["Id","Name","Email"])
        writer.writerows(data)
    f.close()
    message1.configure(text="Deleted "+Name+" "+Id)

button1=tk.Button(root,text="Clear",command=clear,width=8,fg="white",bg="red",font=('times',20,'bold'))
button1.place(x=500,y=200)

button2=tk.Button(root,text="Quit",command=quit,width=8,fg="white",bg="red",font=('times',20,'bold'))
button2.place(x=500,y=275)

button3=tk.Button(root,text="Add New",command=add_new,width=8,fg="white",bg="red",font=('times',20,'bold'))
button3.place(x=500,y=50)

button4=tk.Button(root,text="Delete",command=delete,width=8,fg="white",bg="red",font=('times',20,'bold'))
button4.place(x=500,y=125)
root.mainloop()