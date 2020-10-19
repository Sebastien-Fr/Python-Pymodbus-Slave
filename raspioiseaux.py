from pymodbus.server.async import StartTcpServer
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from twisted.internet.task import LoopingCall
import RPi.GPIO as GPIO

import time
import string
import os
import glob


""" declare type d'adressage gpio"""
GPIO.setmode(GPIO.BOARD)
""" ignore les msg d'alarme """
GPIO.setwarnings(False)
""" affectation du type de gpio i/o """
"""affectation des pin gpio"""
GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)
"""sorties """
GPIO.setup(11, GPIO.OUT)
GPIO.setup(12, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)




"""**************************partie modbus avec pymodbus installé************************"""
if __name__ == '__main__':
   
         
    
            print ('Thread modbus ')
            """**************declare le nb de mots ***********************"""
            store = ModbusSlaveContext(
                di = ModbusSequentialDataBlock(0, [0]*100),
                co = ModbusSequentialDataBlock(0, [0]*100),
                hr = ModbusSequentialDataBlock(0, [0]*100),
                ir = ModbusSequentialDataBlock(0, [0]*100))
            context = ModbusServerContext(slaves=store, single=True)

            """**************************ecrit les entrees dans le module modbus************************"""
            def updating_writer(a):
                context  = a[0]
                register = 3
                slave_id = 0
                address  = 10 # mot w15 
                values = [GPIO.input(16),GPIO.input(18),GPIO.input(22),GPIO.input(7),]
                  
                context[slave_id].setValues(register,address,values)
                if values[0]==0:
                   print 'in 0 a 1'
                if values[1]==0:
                  print 'in 1 a 1'
                if values[2]==0:
                   print 'out 2 a 1'
                if values[3]==0:
                   print 'in 3 a 1'
                
            """*********lit les valeurs du module modbus et les ecrit sur les gpio************************"""
            def read_context(a):
                 context  = a[0]
                 register = 3
                 slave_id = 0
                 address  = 30 # mot w30 
                 value = context[slave_id].getValues(register,address,10)
                 
                 """ ecriture des sorties """
       
                 if value[0]==0:GPIO.output(11, GPIO.LOW)#w30
                 if value[0]==1:GPIO.output(11, GPIO.HIGH)
                 if value[1]==0:GPIO.output(12, GPIO.LOW)#w31
                 if value[1]==1:GPIO.output(12, GPIO.HIGH)
                 if value[2]==0:GPIO.output(13, GPIO.LOW)#w32
                 if value[2]==1:GPIO.output(13, GPIO.HIGH)
                 if value[3]==0:GPIO.output(15, GPIO.LOW)#w33
                 if value[3]==1:GPIO.output(15, GPIO.HIGH)
            
            
                 if value[0]==1:
                   print 'out 0 a 1'
                 if value[1]==1:
                  print 'out 1 a 1'
                 if value[2]==1:
                   print 'out 2 a 1'
                 if value[3]==1:
                   print 'out 3 a 1'
                
                 
                         
            read = LoopingCall(f=read_context, a=(context,))
            read.start(.2)

            write = LoopingCall(f=updating_writer, a=(context,))
            write.start(.2)

                    
            StartTcpServer(context)


