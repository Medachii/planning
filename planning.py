import tkinter as tk
import time as t
from time import *
import datetime as dt
import sqlite3 as sq
from functools import partial

class planning:
    def __init__(self,p=1):
        self.conn=sq.connect('planning.db')
        self.cur=self.conn.cursor()
        self.c=tk.Canvas(fenetre,width=1900,height=1000,bg='white')
        #self.planner=self.c.create_rectangle(20,20,1490,980,width=3)                         #peut être à effacer
        self.todolist=self.c.create_rectangle(1510,20,1880,977,fill='lavender',width=3,tags="todolist")
        self.c.tag_bind('todolist','<Button-1>',self.todo)
        self.todonom=self.c.create_text(1700,50,text='To do list',font=('Times','32','italic'))
        jours=['Lundi','Mardi','Mercredi','Jeudi','Vendredi','Samedi','Dimanche']
        couleurjours=['papaya whip','orange','lavender','hot pink','aquamarine','thistle2','light salmon']
        self.surligneur=['light cyan','light salmon','papaya whip','lavender','mint cream','aquamarine','light goldenrod yellow','tomato','white']
        self.jour=dict()
        self.case=dict()
        self.nomjour=dict()
        self.points=dict()
        self.taches=dict()
        self.supptachelab=dict()
        self.supptachebut=dict()
        self.surltachelab=dict()
        self.surltachebut=dict()
        self.affichage=dict()
        self.todoafaire=dict()
        self.supptodolab=dict()
        self.supptodobut=dict()
        self.todoaffich=dict()
        self.coulsur=dict()
        self.recttache=dict()
        m=0

        joursemaine=list(strptime(ctime(time())))[6]
        self.mois=list(strptime(ctime(time())))[1]
        self.annee=list(strptime(ctime(time())))[0]
        
        for i in range(7):      #jours
            self.jour[i]=self.c.create_rectangle(20+(210*i),65,20+(210*(i+1)),145,width=3,fill="{}".format(couleurjours[i]))
            self.nomjour[i]=self.c.create_text(120+210*i,105,text="{}".format(jours[i]),font=('Times','26'))
        for i in range(6):  
            for j in range(7):
                m=m+1
                self.case[m]=self.c.create_rectangle(20+(210*j),145+(138*i),20+(210*(j+1)),145+(138*(i+1)),width=3,tags='case',fill='white')
                self.c.tag_bind('case','<Button-1>',self.journee)
        for k in range(6):
            self.points[i]=self.c.create_oval(1530,130+(k*150),1540,140+(k*150),fill='black')
        self.moisactuel=self.c.create_text(750,35,text="",font=('Times','36','italic bold'))
        self.anneeactuelle=self.c.create_text(100,35,text="{}".format(self.annee),font=('Times','36','italic bold'))


        
        self.c.pack()
        print(str(list(self.c.find_withtag('case'))[2]))
        for i in range(len(self.c.find_withtag('case'))):
            self.afftache(int(list(self.c.find_withtag('case'))[i]))
        
        
        self.suivant=self.c.create_line(850,35,900,35,arrow=tk.LAST,width=3,tags='suivant')
        self.precedent=self.c.create_line(650,35,600,35,arrow=tk.LAST,width=3,tags='precedent')
        self.c.tag_bind('suivant','<Button-1>',self.suivantbutton)
        self.c.tag_bind('precedent','<Button-1>',self.precedentbutton)

        
        self.mise_en_place_jours(self.mois)
        self.afftodo()
        

        

    def suivantbutton(self,event): #fonction qui permet de changer de mois
        self.mois+=1
        if self.mois==13:
            self.mois=1
            self.annee+=1
    
        self.mise_en_place_jours(self.mois)

    def precedentbutton(self,event):    #fonction qui permet de changer de mois
        self.mois-=1
        if self.mois==0:
            self.mois=12
            self.annee-=1
        self.mise_en_place_jours(self.mois)
        
    def mise_en_place_jours(self,mois):     #fonction qui met bien tous les numéros au bon jour quand on change de mois
        self.c.delete("effmois")
        print(self.taches)
        self.c.delete("tache")
        print(self.taches)
        
        self.c.delete(self.moisactuel)
        self.c.delete(self.anneeactuelle)
        self.c.delete('numero')
        self.moisactuel=self.c.create_text(750,35,text="{}".format(self.traduction(mois)),font=('Times','36','italic bold'))
        self.anneeactuelle=self.c.create_text(100,35,text="{}".format(self.annee),font=('Times','36','italic bold'))
        premierjoursem=self.cur.execute("Select jour from annee where mois={}".format(mois)).fetchone()[0]
        nbr=self.cur.execute("Select nbrjour from annee where mois={}".format(mois)).fetchone()[0]
        for k in range(premierjoursem,nbr+premierjoursem):
            a,b,c,d=self.c.coords(self.case[k])
            self.numero=self.c.create_text(a+25,b+30,text="{}".format(k+1-premierjoursem),font=('Times','22'),tags='numero')
        for i in range(len(self.c.find_withtag('case'))):
            self.afftache(int(list(self.c.find_withtag('case'))[i]))


    def traduction(self,a):         #Traduction anglais -> francais
        mois=['Janvier','Février','Mars','Avril','Mai','Juin','Juillet','Août','Septembre','Octobre','Novembre','Décembre']
        return mois[a-1]

    def journee(self,event):    #Quand on clique sur une case
        

        
        self.x,self.y=event.x,event.y
        self.casechoisie=self.c.find_closest(event.x,event.y)[0]
        print(self.casechoisie)            
        self.F1=tk.Toplevel()
        self.ajtache=tk.Button(self.F1,text="Ajouter une tâche",command=self.ajoutertache)
        self.suptache=tk.Button(self.F1,text="Supprimer tâche",command=self.supprimertache)
        self.surlignebutton=tk.Button(self.F1,text="Surligner une tache",command=self.surligner)
        self.ajtache.grid(row=0,column=0)
        self.suptache.grid(row=1,column=0)
        self.surlignebutton.grid(row=100,column=0)
        print(self.cur.execute("Select * from taches where mois={} and id={}".format(self.mois,self.casechoisie)).fetchall())   #[('mois','id','heure','minute','tache')]
        liste=self.cur.execute("Select * from taches where mois={} and id={} order by heure,minute".format(self.mois,self.casechoisie)).fetchall()
        
        for i in range(len(liste)):
            self.affichage[i]=tk.Label(self.F1,text="{}h{}: {}".format(liste[i][2],self.changeminute(liste[i][3]),liste[i][4]),font=('Times','30'),background=self.surligneur[liste[i][6]],width=40)
            self.affichage[i].grid(row=2+i,column=0)
        
            
            
    def ajoutertache(self):             # quand on clique sur ajouter une tache
        self.F2=tk.Toplevel()
        self.labelentreheure=tk.Label(self.F2,text="Heure:")
        self.entryajheure=tk.Entry(self.F2,textvariable=tk.StringVar())
        self.labelheure=tk.Label(self.F2,text="h")
        self.entryajminute=tk.Entry(self.F2,textvariable=tk.StringVar())
        self.labeltache=tk.Label(self.F2,text="Tâche:")
        self.entryajtache=tk.Entry(self.F2,textvariable=tk.StringVar())
        self.ValideF2=tk.Button(self.F2,text="Ajouter tâche",command=self.ValiderF2)
        self.labelentreheure.grid(row=0,column=0)
        self.entryajheure.grid(row=0,column=1)
        self.labelheure.grid(row=0,column=2)
        self.entryajminute.grid(row=0,column=3)
        self.labeltache.grid(row=1,column=0)
        self.entryajtache.grid(row=1,column=1)
        self.ValideF2.grid(row=2,column=0)
        

    def ValiderF2(self):                # quand on valide l'ajout d'une tache
        self.heure=self.entryajheure.get()
        self.minute=self.entryajminute.get()
        self.tache=self.entryajtache.get()
        print(self.tache)
        self.cur.execute("""Insert into taches(mois,id,heure,minute,tache,couleur) values({},{},{},{},"{}",{})""".format(self.mois,self.casechoisie,self.heure,self.minute,self.tache,-1) )        #mois id heures minute tache
        self.conn.commit()
        self.c.delete("recttach{}".format(self.casechoisie))
        self.afftache(self.casechoisie)
        self.journeemaj()
        self.F2.destroy()

    def afftache(self,idd):                 #fonction qui reinitialise les taches
        self.c.delete("oui{}".format(idd))
        #self.c.delete("recttach")
        a,b,c,d=self.c.coords(idd)
        liste=self.cur.execute("Select * from taches where mois={} and id={} order by heure,minute".format(self.mois,idd)).fetchall()
       
        for i in range(len(liste)):
            if i<=5:
                
                self.recttache[i]=self.c.create_rectangle(a+45,b+10+(20*i),a+200,b+30+(20*i),fill=self.surligneur[liste[i][6]],outline=self.surligneur[liste[i][6]],tags=("recttach{}".format(idd),"effmois"))
                self.taches[i]=self.c.create_text(a+120,b+20+(20*i),text="{}h{}: {}".format(liste[i][2],self.changeminute(liste[i][3]),liste[i][4]),font=('Times','10','bold'),fill='black',tags=("tache","oui{}".format(idd)))
                
            else:
                print("<3")
            
        
        
    def supprimertache(self):           #quand on clique sur supprimer une tache
        self.F3=tk.Toplevel()
        liste=self.cur.execute("Select * from taches where mois={} and id={} order by heure,minute".format(self.mois,self.casechoisie)).fetchall()
        print(self.cur.execute("Select cle from taches where mois={} and id={}".format(self.mois,self.casechoisie)).fetchall())   # [(1,),(2,)]
        supp=self.cur.execute("Select cle from taches where mois={} and id={} order by heure,minute".format(self.mois,self.casechoisie)).fetchall()
        self.suppliste=[int(supp[i][0]) for i in range(len(supp))]
        print(self.suppliste)
        for i in range(len(liste)):
            self.supptachelab[i]=tk.Label(self.F3,text="{}h{}: {}".format(liste[i][2],self.changeminute(liste[i][3]),liste[i][4]),font=('Times','20'))
            self.supptachelab[i].grid(row=i,column=0)
            self.supptachebut[i]=tk.Button(self.F3,text="Supprimer",command=partial(self.supprimer,i))
            self.supptachebut[i].grid(row=i,column=1)

    def supprimer(self,i):          # quand on valide la suppresion
        
        self.cur.execute("Delete from taches where cle={}".format(self.suppliste[i]))
        self.supptachelab[i].destroy()
        self.supptachebut[i].destroy()
        self.conn.commit()
        self.c.delete("recttach{}".format(self.casechoisie))
        self.afftache(self.casechoisie)
        self.journeemaj()
        self.F3.destroy()

    def journeemaj(self):                   #met a jour la fenetre intermediaire
        for i in range(len(self.affichage)):
            self.affichage[i].destroy()    
        liste=self.cur.execute("Select * from taches where mois={} and id={} order by heure,minute".format(self.mois,self.casechoisie)).fetchall()
        for i in range(len(liste)):
            self.affichage[i]=tk.Label(self.F1,text="{}h{}: {}".format(liste[i][2],self.changeminute(liste[i][3]),liste[i][4]),font=('Times','30'),background=self.surligneur[liste[i][6]],width=40)
            self.affichage[i].grid(row=2+i,column=0)

    
    def surligner(self):
        print('oui')
        self.F7=tk.Toplevel()
        liste=self.cur.execute("Select * from taches where mois={} and id={} order by heure,minute".format(self.mois,self.casechoisie)).fetchall()
       # [(1,),(2,)]
        
        for i in range(len(liste)):
            self.surltachelab[i]=tk.Label(self.F7,text="{}h{}: {}".format(liste[i][2],self.changeminute(liste[i][3]),liste[i][4]),font=('Times','20'),background=self.surligneur[liste[i][6]])
            self.surltachelab[i].grid(row=i,column=0)
            self.surltachebut[i]=tk.Button(self.F7,text="Surligner",command=partial(self.surlignage,i))
            print("oui1",self.surltachebut[i])
            self.surltachebut[i].grid(row=i,column=1)

    def surlignage(self,j):
        self.numtruccolor=j
        self.F8=tk.Toplevel()
        
        self.csur=tk.Canvas(self.F8,width=400,height=360,bg='white')
        self.csur.pack()
        self.L=[]
        for i in range(8):
            if i<4:
                self.coulsur[i]=self.csur.create_rectangle(100,50+(70*i),150,100+(70*i),fill=self.surligneur[i],tags="couleur")
                self.csur.tag_bind("couleur",'<Button-1>',self.colorier)
                self.L.append(self.csur.find_withtag(self.coulsur[i]))
            elif i>=4:
                self.coulsur[i]=self.csur.create_rectangle(250,50+(70*(i-4)),300,100+(70*(i-4)),fill=self.surligneur[i],tags="couleur")
                self.csur.tag_bind("couleur",'<Button-1>',self.colorier)
                self.L.append(self.csur.find_withtag(self.coulsur[i]))
        print("self.L",self.L)

    def colorier(self,event):  #i numero de la couleur    j numero du truc a colorier
        
        self.a,self.b=event.x,event.y
        self.idcouleur=self.csur.find_closest(self.a,self.b)[0]
        #print("idcouleur",self.idcouleur)
        #print(self.csur.find_withtag(self.idcouleur))
        I=self.idcouleur-1
        print("I",I)
        
        if I==8:
            I=-1
        print("oui2",self.surltachelab[self.numtruccolor])
        self.surltachelab[self.numtruccolor].config(background="{}".format(self.surligneur[I]))
       
        clesur=self.cur.execute("Select cle from taches where mois={} and id={} order by heure,minute".format(self.mois,self.casechoisie)).fetchall()
        print("clesur",clesur)
        self.cur.execute("Update taches set couleur={} where cle={}".format(I,clesur[self.numtruccolor][0]))
        self.conn.commit()
        self.c.delete("recttach{}".format(self.casechoisie))
        self.afftache(self.casechoisie)
        self.journeemaj()
        self.F8.destroy()
        self.F7.destroy()



    def changeminute(self,minute):
        
        
        if minute==0:
            minute='00'
        

        return minute
        
                
            
            
        
        






#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def todo(self,event):
        self.F4=tk.Toplevel()
        self.ajtodoafaire=tk.Button(self.F4,text="Ajouter un \"To do\"",command=self.ajtodo)
        self.suptodoafaire=tk.Button(self.F4,text="Supprimer un \"To do\"",command=self.suptodo)
        self.ajtodoafaire.grid(row=0,column=0)
        self.suptodoafaire.grid(row=1,column=0)



        
        todoliste=self.cur.execute("Select afaire from todolist").fetchall()
            
        for i in range(len(todoliste)):
            self.todoafaire[i]=tk.Label(self.F4,text="♦ {}".format(todoliste[i][0]),font=('Times','30'),background='white',width=40)
            self.todoafaire[i].grid(row=2+i,column=0)

    def ajtodo(self):
        self.F5=tk.Toplevel()
        self.todolabel=tk.Label(self.F5,text="To do:")
        self.todoentry=tk.Entry(self.F5,textvariable=tk.StringVar())
        self.todovalider=tk.Button(self.F5,text="Valider",command=self.todovalide)
        self.todolabel.grid(row=0,column=0)
        self.todoentry.grid(row=0,column=1)
        self.todovalider.grid(row=1,column=0)
        if len(self.cur.execute("Select afaire from todolist").fetchall())==6:
            self.F5.destroy()

    def todovalide(self):
        tacheajoutee=self.todoentry.get()
        self.cur.execute("""Insert into todolist(afaire) values("{}")""".format(tacheajoutee))
        self.conn.commit()
        self.afftodo()
        self.todomaj()
        self.F5.destroy()
        
        
        

    def suptodo(self):
        self.F6=tk.Toplevel()

        liste=self.cur.execute("Select afaire from todolist").fetchall()
        supp=self.cur.execute("Select cletodo from todolist").fetchall()
        
        
        
        self.supplistetodo=[int(supp[i][0]) for i in range(len(supp))]
        
        for i in range(len(liste)):
            self.supptodolab[i]=tk.Label(self.F6,text="{}".format(liste[i][0]),font=('Times','20'))
            self.supptodolab[i].grid(row=i,column=0)
            self.supptodobut[i]=tk.Button(self.F6,text="Supprimer",command=partial(self.supprimertodo,i))
            self.supptodobut[i].grid(row=i,column=1)
        

    def supprimertodo(self,i):
        self.cur.execute("Delete from todolist where cletodo={}".format(self.supplistetodo[i]))
        self.supptodolab[i].destroy()
        self.supptodobut[i].destroy()
        self.conn.commit()
        self.afftodo()
        self.todomaj()
        self.F6.destroy()

    def afftodo(self):
        self.c.delete("todo")
        liste=self.cur.execute("Select afaire from todolist").fetchall()
        for i in range(len(liste)):
            self.todoaffich[i]=self.c.create_text(1700,130+(150*i),text="{}".format(liste[i][0]),font=('Times','20'),tags="todo")


    def todomaj(self):
        for i in range(len(self.todoafaire)):
            self.todoafaire[i].destroy()
        
        todoliste=self.cur.execute("Select afaire from todolist").fetchall()
        for i in range(len(todoliste)):
            self.todoafaire[i]=tk.Label(self.F4,text="♦ {}".format(todoliste[i][0]),font=('Times','30'),background='white',width=40)
            self.todoafaire[i].grid(row=2+i,column=0)
        
            
        

        
        

    
        
        
        
        
        
    
        
        
        
        
        
        
    



        




fenetre=tk.Tk()
App=planning(1)
fenetre.mainloop()
