import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
import pymysql
from datetime import date,datetime
from tkinter import *
from PIL import ImageTk, Image
import requests
import urllib.parse
from math import sin, cos, sqrt, atan2
import math

# Calcularea distanței dintre două puncte pe glob
def calculateDistances(latTrue,lonTrue,latPred,lonPred):
    R = 6373.0


    lat1 = math.radians(latTrue)
    lon1 = math.radians(lonTrue)
    lat2 = math.radians(latPred)
    lon2 = math.radians(lonPred)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c

    
    
    return distance

#prediction
def prediction(latitude, longitude):   
    i=0
    t=True
    #creem conexiunea cu baza de date
    connection = pymysql.connect(host="remotemysql.com",user="jERtaPoJ1f",passwd="2UtIYwosjH",database="jERtaPoJ1f" )
    cursor = connection.cursor()
    #setăm variabila today cu data în care ne aflăm
    today = date.today()
    #selecția pe care o facem pe baza de date
    querry= "SELECT `date`,`Latitude`,`Longitude` FROM `dates`"
    #executăm querry-ul
    cursor.execute(querry)
    rows = cursor.fetchall()
    connection.commit()
    connection.close()
    #intrăm într-un loop care se va oprii atunci când găsește locația unei eclipse la mai puțin de 2500 km de locația introdusă
    while(t):
        if calculateDistances(float(latitude),float(longitude),float(rows[i][1]),float(rows[i][2]))<2500:
            if today > rows[i][0]:
                i+=1
            else :   
                result=rows[i][0]
                t=False
        else :
            i+=1
    
    return result


class Test():
    def __init__(self):
        # inițializăm ecranul principal
        self.window= Tk()
        self.window.geometry("720x480")
        self.window.resizable(False, False)
        self.window.title("Solar prediction")
        self.bg = ImageTk.PhotoImage(Image.open("background.jpg")) 
        self.window.configure(background="gray")
        self.res= StringVar() #variabilă string care urmează să salveze și să afișeze rezultatul
        self.res.set("")
        self.again= StringVar() #variablia care v-a afișa un mesaj
        self.again.set("")
        self.loc= StringVar() #variabliă string care v-a prelua locația introdusă de utilizator 
        self.loc.set("")

        # Imagine
        self.label1= Label(self.window,image=self.bg)
        self.label1.place(x=0,y=0)


       
        
        #variabilă Label care v-a afișa rezultatul
        self.labelres= Label(self.window,textvariable=self.res,bg="black",fg="white",font="none 20 bold")

        #variabilă Label pentru a afișa un mesaj
        self.labelagain= Label(self.window,textvariable=self.again,bg="gray",fg="white",font="Helvetica 20 bold")
        
        #variabilă de tip Entry în care utilizatorul v-a putea introduce o locație
        self.location = Entry(self.window,width=15,bg="gray" ,font=("Helvetica", 16),textvariable=self.loc)
        
        #Introducerea unui placeholder în entry-ul de mai sus
        self.location.insert(0,"Introduceți locația")
        

        #Butonul de submit care v-a apela funcția click
        self.button1=Button(self.window,text="SUBMIT",width=6,command=self.click) 
        
        #plasarea variabilelor pe ecran
        self.location.place(x=275,y=230)
        self.labelagain.place(x=200,y=315)
        self.button1.place(x=338,y=400)
        self.labelres.place(x=290,y=435)

        #run the window loop
        self.window.mainloop()


    def click(self):
        #preia locția introdusă de utilizator
        address=self.location.get()
        
        url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(address) +'?format=json'
        #facem un request la url pentru date ale locatiei introduse
        response = requests.get(url).json()

        latitude= response[0]["lat"]
        longitude = response[0]["lon"]

        self.res.set(str(prediction(latitude,longitude)))
        self.again.set("Puteți introduce o altă locație")
        self.location.delete(0, END)


app=Test()