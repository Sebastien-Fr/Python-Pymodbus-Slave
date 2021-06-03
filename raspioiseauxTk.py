from pymodbus.server.asynchronous import StartTcpServer
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from twisted.internet.task import LoopingCall
import RPi.GPIO as GPIO
import threading
import time
from datetime import timedelta
from datetime import date
from datetime import datetime
import string
import os
import glob
import logging
from logging.handlers import RotatingFileHandler
import tkinter as tk
from tkinter import *
from tkinter import ttk
mainWin = Tk()
mainWin.title('O/Iseaux')

# declare type d'adressage gpio
GPIO.setmode(GPIO.BOARD)
#ignore les msg d'alarme 
GPIO.setwarnings(False)
#affectation du type de gpio i/o 
#affectation des pin gpio
GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)
"""sorties """
GPIO.setup(11, GPIO.OUT)
GPIO.setup(12, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)

###init
out1=0
out2=0
out3=0
out4=0
out5=0
out6=0
out7=0
out8=0
out=[0,0,0,0,0,0,0,0]
init=0
etat1=0
debut1=0
fin1=0
etat2=0
debut2=0
fin2=0
etat3=0
debut3=0
fin3=0
etat4=0
debut4=0
fin4=0
etat5=0
debut5=0
fin5=0

#**************declare le nb de mots  modbus***********************
store = ModbusSlaveContext(
di = ModbusSequentialDataBlock(0, [0]*100),
co = ModbusSequentialDataBlock(0, [0]*100),
hr = ModbusSequentialDataBlock(0, [0]*100),
ir = ModbusSequentialDataBlock(0, [0]*100))
context = ModbusServerContext(slaves=store, single=True)

#############################      logger    ################################
logger = logging.getLogger('Oiseaux')
logger.setLevel(logging.DEBUG)
fh= RotatingFileHandler('Oiseaux.log',maxBytes=1000000, backupCount=5)
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

######################### LOAD PARAMS at startup ###############################
def load():
    global init
    pr=[0,0,0,0,0]
    on=[0,0,0,0,0]
    debut=[0,0,0,0,0]
    fin=[0,0,0,0,0]
    days=[0, 0, 0, 0, 0]
    alldays=[]  
    fichier = "params.csv"
    f=open(fichier,"r")
    ligne=f.readlines()
    
    for index in range (0,5):
        pr[index]=ligne[index]
        #print(pr)
        on[index]= (pr[index][5:8])
        debut[index] =(pr[index][9:17])
        fin[index] =(pr[index][18:26])
        days[index]=(pr[index][28:47])
       
   
    #erase old values
    HOnEAU.delete(0,END)
    HOnNourit.delete(0,END)
    HOnJardin.delete(0,END)
    HOnFleurs.delete(0,END)
    HOnGuirl.delete(0,END)
    HOffEAU.delete(0,END)
    HOffNourit.delete(0,END)
    HOffJardin.delete(0,END)
    HOffFleurs.delete(0,END)
    HOffGuirl.delete(0,END)
   
    #load state of buttons#
    B1.config(text=on[0])
    B2.config(text=on[1])
    B3.config(text=on[2])
    B4.config(text=on[3])
    B5.config(text=on[4])
    #load debut entrys#
    HOnEAU.insert(0,debut[0])
    HOnNourit.insert(0,debut[1])
    HOnJardin.insert(0,debut[2])
    HOnFleurs.insert(0,debut[3])
    HOnGuirl.insert(0,debut[4])
    #load fin entrys#
    HOffEAU.insert(0,fin[0])
    HOffNourit.insert(0,fin[1])
    HOffJardin.insert(0,fin[2])
    HOffFleurs.insert(0,fin[3])
    HOffGuirl.insert(0,fin[4])
    #load days checked
    #mise en forme
    n=0
    chek=[]
    for x in range(0,5):
        for z in range (0,len(days[x])):
         if days[x][z].isnumeric():              
            chek.append(int(days[x][z]))
            #print (chek)
        
    for n in range (0,len(chek)):   
        vars[n].set(chek[n])
    f.close()
    init=1
    print ('load')
    
######################### STORE PARAMS ################################
def store(*args):
    global init
    #print(init)
    
    global etat1,debut1,fin1,etat2,debut2,fin2,etat3,debut3,fin3,etat4,debut4,fin4,etat5,debut5,fin5,flag
    debut1=datetime.strptime(HOnEAU.get(), "%H:%M:%S").strftime("%H:%M:%S")
    debut2=datetime.strptime(HOnNourit.get(), "%H:%M:%S").strftime("%H:%M:%S")
    debut3=datetime.strptime(HOnJardin.get(), "%H:%M:%S").strftime("%H:%M:%S")
    debut4=datetime.strptime(HOnFleurs.get(), "%H:%M:%S").strftime("%H:%M:%S")
    debut5=datetime.strptime(HOnGuirl.get(), "%H:%M:%S").strftime("%H:%M:%S")
    fin1=datetime.strptime(HOffEAU.get(), "%H:%M:%S").strftime("%H:%M:%S")
    fin2=datetime.strptime(HOffNourit.get(), "%H:%M:%S").strftime("%H:%M:%S")
    fin3=datetime.strptime(HOffJardin.get(), "%H:%M:%S").strftime("%H:%M:%S")
    fin4=datetime.strptime(HOffFleurs.get(), "%H:%M:%S").strftime("%H:%M:%S")
    fin5=datetime.strptime(HOffGuirl.get(), "%H:%M:%S").strftime("%H:%M:%S")
    etat1=B1.config('text')[-1]
    etat2=B2.config('text')[-1]
    etat3=B3.config('text')[-1]
    etat4=B4.config('text')[-1]
    etat5=B5.config('text')[-1]


    checked=[0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,
            0,0,0,0,0,0,0]
                
    for x in range(0,35):
        checked[x]=vars[x].get()
    #print (checked)
    if init ==1:
        fichier = "params.csv"
        f=open(fichier,"w")
        f.writelines ('prg1:'+str(etat1)+";"+str(debut1)+";"+str(fin1)+";"+str(checked[0:7])+"\n"+
                      'prg2:'+str(etat2)+";"+str(debut2)+";"+str(fin2)+";"+str(checked[7:14])+"\n"+
                      'prg3:'+str(etat3)+";"+str(debut3)+";"+str(fin3)+";"+str(checked[14:21])+"\n"+
                      'prg4:'+str(etat4)+";"+str(debut4)+";"+str(fin4)+";"+str(checked[21:28])+"\n"+
                      'prg5:'+str(etat5)+";"+str(debut5)+";"+str(fin5)+";"+str(checked[28:35])+"\n")
        
        
        f.close()
        print ('update')
    

########################   partie modbus avec pymodbus installé              ##########################
class modbus(threading.Thread):
    def __init__(self,nom = 'modbus'):
      threading.Thread.__init__(self)
      self.nom=nom
      self.terminated = False
    def run(self):
            time.sleep(1) 
            logger.info('Start Modbus')
            print ('Thread modbus ')
            #**************************ecrit les entrees dans le module modbus************************
            def updating_writer(a):
                context  = a[0]
                register = 3
                slave_id = 0
                address  = 10 # mot w15 
                values = [GPIO.input(7),GPIO.input(22),GPIO.input(18),GPIO.input(16),]  
                context[slave_id].setValues(register,address,values)
            #########################################################################################    
            def updating_writer_internal(value):
                global context
                register = 3
                slave_id = 0
                address  = 30 # mot 
                values= value
                context[slave_id].setValues(register,address,values)   
                
            #*********lit les valeurs du module modbus et les ecrit sur les gpio************************
            def read_context(a):
                 global out1,out2,out3,out4,out5,out6,out7,out8
                 context  = a[0]
                 register = 3
                 slave_id = 0
                 address  = 30 # mot w30 
                 value = context[slave_id].getValues(register,address,10)
   
                 ######### local plc write value   ################
                 if  out1 == 1 :#eau
                     value[1] = out1
                 if out2==1:#nourritt
                     value[2] = out2
                 if out3==1:#jardin
                     value[3] = out3
                 if out4==1:#fleur
                     value[0] = out4
                 if out5==1:#guirl
                     value[4] = out5
                 ##########@@@@@@###############
                 #ecriture des sorties
       
                 if value[0]==0:GPIO.output(11, GPIO.LOW)#w30 fleurs
                 if value[0]==1:GPIO.output(11, GPIO.HIGH)
                 if value[1]==0:GPIO.output(12, GPIO.LOW)#w31 eau
                 if value[1]==1:GPIO.output(12, GPIO.HIGH)
                 if value[2]==0:GPIO.output(13, GPIO.LOW)#w32 graines
                 if value[2]==1:GPIO.output(13, GPIO.HIGH)
                 if value[3]==0:GPIO.output(15, GPIO.LOW)#w33 jardin
                 if value[3]==1:GPIO.output(15, GPIO.HIGH)

            
                 #affichage io
                 #input
                 labelai6.config(text=str((not GPIO.input(16),not GPIO.input(18),not GPIO.input(22),not GPIO.input(7))))
                 #output
                 labelai7.config(text=str((GPIO.input(11),GPIO.input(12),GPIO.input(13),GPIO.input(15))))
                            
            read = LoopingCall(f=read_context, a=(context,))
            read.start(.2)

            write = LoopingCall(f=updating_writer, a=(context,))
            write.start(.2)
            StartTcpServer(context)
########################################################################################            
if __name__ == '__main__':
            
                
            #### PLC ####  
            def update_Out():
                now = time.strftime("%H:%M:%S")
                label10.configure(text=now)
                mainWin.after(1000, update_Out)
                
                global out1,out2,out3,out4,out5
                
                ######### jours   #######

                NumJour= datetime.today().weekday()
                checked=[0,0,0,0,0,0,0,
                         0,0,0,0,0,0,0,
                         0,0,0,0,0,0,0,
                         0,0,0,0,0,0,0,
                         0,0,0,0,0,0,0]
                
                for x in range(0,35):
                    checked[x]=vars[x].get()

                if checked[NumJour]==1:
                    daycheck1=True
                else:
                    daycheck1=False
                if checked[NumJour+7]==1 :
                    daycheck2=True
                else:
                    daycheck2=False
                if checked[NumJour+14]==1:
                    daycheck3=True
                else:
                    daycheck3=False
                if checked[NumJour+21]==1:
                    daycheck4=True
                else:
                    daycheck4=False
                if checked[NumJour+28]==1:
                    daycheck5=True
                else:
                    daycheck5=False

                if B6.config('text')[-1]=='On 'or (B1.config('text')[-1]=='On 'and
                                                  now >datetime.strptime(HOnEAU.get(), "%H:%M:%S").strftime("%H:%M:%S") and
                                                  now <datetime.strptime(HOffEAU.get(), "%H:%M:%S").strftime("%H:%M:%S")and daycheck1==True ):
                    out1=1
                else :
                    out1=0   
                if B7.config('text')[-1]=='On 'or (B2.config('text')[-1]=='On 'and
                                                  now >datetime.strptime(HOnNourit.get(), "%H:%M:%S").strftime("%H:%M:%S") and
                                                  now <datetime.strptime(HOffNourit.get(), "%H:%M:%S").strftime("%H:%M:%S")and daycheck2==True ):
                    out2=1
                else :
                    out2=0   
                if B8.config('text')[-1]=='On 'or (B3.config('text')[-1]=='On 'and
                                                  now >datetime.strptime(HOnJardin.get(), "%H:%M:%S").strftime("%H:%M:%S") and
                                                  now <datetime.strptime(HOffJardin.get(), "%H:%M:%S").strftime("%H:%M:%S")and daycheck3==True ):
                    out3=1
                else :
                    out3=0   
                if B9.config('text')[-1]=='On 'or (B4.config('text')[-1]=='On 'and
                                                  now >datetime.strptime(HOnFleurs.get(), "%H:%M:%S").strftime("%H:%M:%S") and
                                                  now <datetime.strptime(HOffFleurs.get(), "%H:%M:%S").strftime("%H:%M:%S")and daycheck4==True ):
                    out4=1
                else :
                    out4=0  
                if B10.config('text')[-1]=='On 'or (B5.config('text')[-1]=='On 'and
                                                   now >datetime.strptime(HOnGuirl.get(), "%H:%M:%S").strftime("%H:%M:%S") and
                                                   now <datetime.strptime(HOffGuirl.get(), "%H:%M:%S").strftime("%H:%M:%S")and daycheck5==True ):
                    out5=1
                else :
                    out5=0
             
            """**************************hmi***********************"""
            """buttons horo"""
            def OnEauOiseaux():
                global etat1
                if  B1.config('text')[-1]=='Off':
                    B1.config(text='On ')
                    etat1=B1.config('text')[-1]
                    store()
                else:
                    B1.config(text='Off')
                    etat1=B1.config('text')[-1]
                    store()
            def OnNourritureOiseaux():
                global etat2
                if  B2.config('text')[-1]=='Off':
                    B2.config(text='On ')
                    etat2=B2.config('text')[-1]
                    store()
                else:
                    B2.config(text='Off')
                    etat2=B2.config('text')[-1]
                    store()
            def OnJardin():
                global etat3
                if  B3.config('text')[-1]=='Off':
                    B3.config(text='On ')
                    etat3=B3.config('text')[-1]
                    store()
                else:
                    B3.config(text='Off')
                    etat3=B3.config('text')[-1]
                    store()
            def OnFleurs():
                global etat4
                if  B4.config('text')[-1]=='Off':
                    B4.config(text='On ')
                    etat4=B4.config('text')[-1]
                    store()
                else:
                    B4.config(text='Off')
                    etat4=B4.config('text')[-1]
                    store()
            def OnGuirlandes():
                global etat5
                if  B5.config('text')[-1]=='Off':
                    B5.config(text='On ')
                    etat5=B5.config('text')[-1]
                    store()
                else:
                    B5.config(text='Off')
                    etat5=B5.config('text')[-1]
                    store()
                       
            """buttons forçage"""
            def FOnEauOiseaux():
                if  B6.config('text')[-1]=='Off':
                    B6.config(text='On ')
                else:
                    B6.config(text='Off')
            def FOnNourritureOiseaux():
                if  B7.config('text')[-1]=='Off':
                    B7.config(text='On ')
                else:
                    B7.config(text='Off')
            def FOnJardin():
                if  B8.config('text')[-1]=='Off':
                    B8.config(text='On ')
                else:
                    B8.config(text='Off')
            def FOnFleurs():
                if  B9.config('text')[-1]=='Off':
                    B9.config(text='On ')
                else:
                    B9.config(text='Off')
            def FOnGuirlandes():
                if  B10.config('text')[-1]=='Off':
                    B10.config(text='On ')    
                else:
                    B10.config(text='Off')

            #Labels column1
            bai1 = ttk.Label(mainWin, width=13, text='EAU Oiseaux: ')
            bai1.grid(row=2,column=1)
            bai2 = ttk.Label(mainWin, width=13, text='Nourriture: ')
            bai2.grid(row=3,column=1)
            bai3 = ttk.Label(mainWin, width=13, text='Jardin: ')
            bai3.grid(row=4,column=1)
            bai4 = ttk.Label(mainWin, width=13, text='Fleurs: ')
            bai4.grid(row=5,column=1)
            bai5 = ttk.Label(mainWin, width=13, text='Guirlandes: ')
            bai5.grid(row=6,column=1)
            label10 = ttk.Label(mainWin, width=13)#heure
            label10.grid(row=8,column=1)

            #Buttons Column 2
            B1 = ttk.Button( text ="On ", command = OnEauOiseaux)
            B1.grid(row=2,column=2)
            B2 = ttk.Button( text ="On ", command = OnNourritureOiseaux)
            B2.grid(row=3,column=2)
            B3 = ttk.Button( text ="Off", command = OnJardin)
            B3.grid(row=4,column=2)
            B4 = ttk.Button( text ="Off", command = OnFleurs)
            B4.grid(row=5,column=2)
            B5 = ttk.Button( text ="Off", command = OnGuirlandes)
            B5.grid(row=6,column=2)
            
            #Labels column2
            
            labelai12 = ttk.Label(mainWin, width=13,text='Programmation horaire')
            labelai12.grid(row=1,column=2)
            
            
            #Labels column3
            labelai1 = ttk.Label(mainWin, width=7,text='Debut: ')
            labelai1.grid(row=2,column=3)
            labelai2 = ttk.Label(mainWin, width=7,text='Debut: ')
            labelai2.grid(row=3,column=3)
            labelai3 = ttk.Label(mainWin, width=7,text='Debut: ')
            labelai3.grid(row=4,column=3)
            labelai4 = ttk.Label(mainWin, width=7,text='Debut: ')
            labelai4.grid(row=5,column=3)
            labelai5 = ttk.Label(mainWin, width=7,text='Debut: ')
            labelai5.grid(row=6,column=3)
            

            #Entry Column4
            var6 = tk.StringVar()
            HOnEAU = ttk.Entry(mainWin, width=8,textvariable=var6)
            HOnEAU.grid(row=2,column=4)
            HOnEAU.insert(0,'7:00:00')
            var6.trace("w",store)

            var7 = tk.StringVar()
            HOnNourit= ttk.Entry(mainWin, width=8,textvariable=var7)
            HOnNourit.grid(row=3,column=4)
            HOnNourit.insert(0,'7:10:00')
            var7.trace("w",store)

            var8 = tk.StringVar()
            HOnJardin = ttk.Entry(mainWin, width=8,textvariable=var8)
            HOnJardin.grid(row=4,column=4)
            HOnJardin.insert(0,'7:20:00')
            var8.trace("w",store)

            var9 = tk.StringVar()
            HOnFleurs= ttk.Entry(mainWin, width=8,textvariable=var9)
            HOnFleurs.grid(row=5,column=4)
            HOnFleurs.insert(0,'7:30:00')
            var9.trace("w",store)

            var10 = tk.StringVar()
            HOnGuirl = ttk.Entry(mainWin, width=8,textvariable=var10)
            HOnGuirl.grid(row=6,column=4)
            HOnGuirl.insert(0,'18:00:00')
            var10.trace("w",store)
            
            #Labels Column5
            labelai1 = ttk.Label(mainWin, width=4,text=' Fin: ')
            labelai1.grid(row=2,column=5)
            labelai2 = ttk.Label(mainWin, width=4,text=' Fin: ')
            labelai2.grid(row=3,column=5)
            labelai3 = ttk.Label(mainWin, width=4,text=' Fin: ')
            labelai3.grid(row=4,column=5)
            labelai4 = ttk.Label(mainWin, width=4,text=' Fin: ')
            labelai4.grid(row=5,column=5)
            labelai5 = ttk.Label(mainWin, width=4,text=' Fin: ')
            labelai5.grid(row=6,column=5)
            
            #Entry column6
            var = tk.StringVar()
            HOffEAU = ttk.Entry(mainWin, width=8,textvariable=var)
            HOffEAU.grid(row=2,column=6)
            HOffEAU.insert(0,'7:01:00')
            var.trace("w",store)

            var1 = tk.StringVar()
            HOffNourit= ttk.Entry(mainWin, width=8,textvariable=var1)
            HOffNourit.grid(row=3,column=6)
            HOffNourit.insert(0,'7:11:00')
            var1.trace("w",store)

            var2 = tk.StringVar()
            HOffJardin = ttk.Entry(mainWin, width=8,textvariable=var2)
            HOffJardin.grid(row=4,column=6)
            HOffJardin.insert(0,'7:30:00')
            var2.trace("w",store)

            var3 = tk.StringVar()
            HOffFleurs= ttk.Entry(mainWin, width=8,textvariable=var3)
            HOffFleurs.grid(row=5,column=6)
            HOffFleurs.insert(0,'7:32:00')
            var3.trace("w",store)

            var4 = tk.StringVar()
            HOffGuirl = ttk.Entry(mainWin, width=8,textvariable=var4)
            HOffGuirl.grid(row=6,column=6)
            HOffGuirl.insert(0,'23:59:00')
            var4.trace("w",store)

            #labels column7
            labelai11 = ttk.Label(mainWin, width=7,text='Forçage')
            labelai11.grid(row=1,column=7)
            bai6 = ttk.Label(mainWin, width=13, text='digit input: ')
            bai6.grid(row=7,column=7)
            bai7 = ttk.Label(mainWin, width=13, text='digit output: ')
            bai7.grid(row=8,column=7)
            
            #Buttons Column 7
            B6 = ttk.Button( text ="Off", command = FOnEauOiseaux)
            B6.grid(row=2,column=7)
            B7 = ttk.Button( text ="Off", command = FOnNourritureOiseaux)
            B7.grid(row=3,column=7)
            B8 = ttk.Button( text ="Off", command = FOnJardin)
            B8.grid(row=4,column=7)
            B9 = ttk.Button( text ="Off", command = FOnFleurs)
            B9.grid(row=5,column=7)
            B10 = ttk.Button( text ="Off", command = FOnGuirlandes)
            B10.grid(row=6,column=7)
            
            #labels column8
            
            labelai6 = ttk.Label(mainWin, width=45,text='')
            labelai6.grid(row=7,column=16)
            labelai7 = ttk.Label(mainWin, width=45,text='')
            labelai7.grid(row=8,column=16)
            
            ## checkbox column 8 -> 14
            labelai13 = ttk.Label(mainWin, width=6,text='JOURS')
            labelai13.grid(row=1,column=8)

            vars=[]
            
            checkboxNames=['L1','Ma1','Me1','J1','V1','S1','D1',
                           'L2','Ma2','Me2','J2','V2','S2','D2',
                           'L3','Ma3','Me3','J3','V3','S3','D3',
                           'L4','Ma4','Me4','J4','V4','S4','D4',
                           'L5','Ma5','Me5','J5','V5','S5','D5']
                   
            i=0
            k=0
            for j in range (0,35):
                    vars.append(tk.IntVar())
                    name= ttk.Checkbutton(mainWin,width=4,text=checkboxNames[j] ,variable =vars[j] )
                    name.grid(row=[k+2],column=[i+8])
                    i=i+1
                    if i!=0 and i%7== 0:
                        i=0
                        k=k+1
   
            """load at startup"""
            if init==0:
                load()

            """Modbus"""
            mod = modbus()
            mod.start()                
            update_Out()
            mainWin.mainloop()
            
            
  #######################################################################  
 

                    
            
            

