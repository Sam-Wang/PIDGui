from PySide.QtCore import*
from PySide.QtGui import *


import sys
import time
import PIDGui
import serial
import pyqtgraph as pg
import numpy as np

import serial.tools.list_ports


class errorCom(Exception):
    def __init__(self, valor):
        self.valor = valor

    def __str__(self):
        return "Error " + str(self.valor)

class GUI(QDialog, PIDGui.Ui_GUI):
    def __init__(self,parent=None):
            super(GUI, self).__init__(parent)
            self.setupUi(self)


############leer datos guardados en archivo de texto
            try:
                archi=open('datos.txt','r')
                linea=archi.readline()

                keywords  = linea.split(";") 
                #print keywords
                  
                while linea!="":
                    #print linea 
                    linea=archi.readline()
                archi.close()
                #asignar cada valor de la separacion split a su variable
                self.varFlag, self.rangoPlot, self.COMCONTROL= keywords 
                ##########terminar de leer datos
            except:
                self.rangoPlot=100 #rango a graficar
                self.COMCONTROL='COM6'
                


                        
            #################Variables            
            self.comVar=0
            self.graphVar=0
            self.contadorSerial=0
            self.limiteCadena=0
            self.vector=0
            #creacion de vectores para guardar datos iniciados en 0
            #self.rangoPlot=100 #rango a graficar
            self.vectorErr=np.arange(int(self.rangoPlot))
            self.vectorCurrent=np.arange(int(self.rangoPlot))
            self.data=np.arange(int(self.rangoPlot))
            self.vectorErr[:]=0
            self.vectorCurrent[:]=0
            
            #iniciacion de cuadro de Plot
            win = pg.GraphicsWindow(title="PIDGui")
            win.resize(800,600)
            win.setWindowTitle('PIDGui')

            p2 = win.addPlot(title="Error plot")
            self.curve = p2.plot()

            ####################################actions buttons
            self.connect(self.btnCom, SIGNAL("clicked()"), self.actionCom)
            self.connect(self.btnLoad, SIGNAL("clicked()"), self.actionLoad)
            self.connect(self.btnSave, SIGNAL("clicked()"), self.actionSave)
            self.connect(self.btnGraph, SIGNAL("clicked()"), self.actionGraph)
            self.connect(self.btnStepUp, SIGNAL("clicked()"), self.actionStepUp)
            self.connect(self.btnStepDown, SIGNAL("clicked()"), self.actionStepDown)
            self.connect(self.btnRestar, SIGNAL("clicked()"), self.actionRestar)
            self.connect(self.btnClose, SIGNAL("clicked()"), self.actionClose)
            ############################################################################
            ####################################begin text Edit
            self.textEditCom.setText(self.COMCONTROL)
            self.textEditPlot.setText(self.rangoPlot)
            self.textEditP.setText('0')
            self.textEditI.setText('0')
            self.textEditD.setText('0')
            self.textEditC.setText('0')
            self.textEditF.setText('0')

            

            #####btn in disable
            self.btnLoad.setEnabled(False)
            self.btnSave.setEnabled(False)
            self.btnGraph.setEnabled(False)
            self.btnStepUp.setEnabled(False)
            self.btnStepDown.setEnabled(False)

            ############time interrupts
            timer=QTimer(self)
            timer.timeout.connect(self.Timer)
            timer.setInterval(1) #time in mS
            timer.start()

####################################Funtions             
    def actionCom(self):
        print ("actionCom")
        self.COMCONTROL=self.textEditCom.text() #read a num port Com
        #print(self.COMCONTROL)

        self.contadorSerial=0
        self.limiteCadena=0
        self.controlData = ''
        
        
        try:
            if(self.comVar==0):
                try:
                    self.control.close()
                    print('Prot COM closed')
                except:
                    print('Prot no COM closed')
                self.control=serial.Serial(self.COMCONTROL,19200,timeout=0.5) #config a port com
                self.control.flushInput()
                #time.sleep(5)
                print ("conectando")                        
                    
                #print (self.controlData)
                print ("port com connect")
        except errorCom, e:
            self.comVar=1
            print e
        except:
            self.comVar=1
            print ("no port com connect")
        
            
        if(self.comVar==0):
            self.comVar=1
            self.btnCom.setText("Disconnet")
           #####btn in disable
            self.btnLoad.setEnabled(True)
            self.btnSave.setEnabled(True)
            self.btnGraph.setEnabled(True)
            self.btnStepUp.setEnabled(True)
            self.btnStepDown.setEnabled(True)
        else:
            self.comVar=0
            self.btnCom.setText("Connet")
            #####btn in disable
            self.btnLoad.setEnabled(False)
            self.btnSave.setEnabled(False)
            self.btnGraph.setEnabled(False)
            self.btnStepUp.setEnabled(False)
            self.btnStepDown.setEnabled(False)
            
            try:
                self.control.close()
                print('Prot COM closed')
            except:
                print('Prot no COM closed')
            
        
            
            #self.control.close() #close port Com
            
        #print(self.comVar)
    def actionLoad(self): #reading configuration
        
        print ("actionLoad")
        self.controlData = ''
        try:
            
            self.limiteCadena=0
            self.contadorSerial=0
            self.control.flushInput()
            self.control.write("@")
            print ("cadena enviada")
            while self.limiteCadena==0:
                
                self.controlData += self.control.read()
                self.contadorSerial=self.contadorSerial+1
                
                if self.contadorSerial>=27:
                       self.limiteCadena=1
                       self.contadorSerial=0


            print self.controlData
            self.textEditP.setText (self.controlData[2:5])
            self.textEditI.setText (self.controlData[7:10])
            self.textEditD.setText (self.controlData[12:15])
            self.textEditC.setText (self.controlData[17:20])
            self.textEditF.setText (self.controlData[22:25])
            
        except:
            print("Faild Readin configuration")
            
    def actionSave(self):#send configuration
        print ("actionSave")
        self.controlData=str('P'+self.textEditP.text()+';')
        self.control.write(self.controlData)
        self.controlData=str('I'+self.textEditI.text()+';')
        self.control.write(self.controlData)
        self.controlData=str('D'+self.textEditD.text()+';')
        self.control.write(self.controlData)
        self.controlData=str('C'+self.textEditC.text()+';')
        self.control.write(self.controlData)
        self.controlData=str('F'+self.textEditF.text()+';')
        self.control.write(self.controlData)

        ##capturar datos de textEditors
        self.COMCONTROL=self.textEditCom.text()
        self.rangoPlot=self.textEditPlot.text()
        

        #Borrar linea que contiene $
        f = open('datos.txt')
        output = []
        for line in f:
            if not "$" in line:
                output.append(line)
        f.close()
        f = open('datos.txt', 'w')
        f.writelines(output)
        f.close()

        #guardar nuevos datos leidos            
        archi=open('datos.txt','a')
        #escribir en este orden en el archivo TXT
        archi.write("$;"+self.rangoPlot+";"+self.COMCONTROL)
        archi.close()
        print ("Datos guardados")
        
        
    def actionGraph(self):
        print ("actionGraph")
        if(self.graphVar==0): #clic para graficar
            self.graphVar=1
            self.btnGraph.setText("Stop")  #switch a text label
            #####btn in disable
            self.btnLoad.setEnabled(False)
            self.btnSave.setEnabled(False)
            self.btnStepUp.setEnabled(False)
            self.btnStepDown.setEnabled(False)
            try:
                self.control.write("U1")  #imprimir por el puerto serial 
            except:
                print("Faild Write port com")
            
        else: #clic para detener grafica
            self.graphVar=0
            self.btnGraph.setText("Graph") #switch a text label
            #####btn in disable
            self.btnLoad.setEnabled(True)
            self.btnSave.setEnabled(True)
            self.btnStepUp.setEnabled(True)
            self.btnStepDown.setEnabled(True)
            try:
                self.control.write("U0")  #imprimir por el puerto serial 
            except:
                print("Faild Write port com")
#envio de pasos +
    def actionStepUp(self):
        print ("actionStepUp")
        self.comboBoxVar= int( self.comboBoxStep.currentText())
        if self.comboBoxVar>100:
            self.control.write("+250;")
            self.control.write("+250;")
            self.control.write("+250;")
            self.control.write("+250;")
            print("+1000;")
        else:
            self.controlData=str('+'+self.comboBoxStep.currentText()+';')
            self.control.write(self.controlData)
            print self.controlData
#envio de pasos -            
    def actionStepDown(self):
        print ("actionStepDown")
        self.comboBoxVar= int( self.comboBoxStep.currentText())
        if self.comboBoxVar>100:
            self.control.write("-250;")
            self.control.write("-250;")
            self.control.write("-250;")
            self.control.write("-250;")
            print ("-1000;")
        else:
            self.controlData=str('-'+self.comboBoxStep.currentText()+';')
            self.control.write(self.controlData)
            print self.controlData
    
    def actionRestar(self):
        print ("actionRestar")
        self.textEditP.setText('0')
        self.textEditI.setText('0')
        self.textEditD.setText('0')
        self.textEditC.setText('0')
        self.textEditF.setText('0')
        
    def actionClose(self):
        print ("actionClose")
        try:
            self.control.close()
            print('Prot COM closed')
        except:
            print('Prot no COM closed')
            
        sys.exit()
        
    def Timer(self):
                
        
        ##read radioButton and comboBox            
        try:
            self.radioButtonVar=self.radioButtonR.isChecked()
            #print (self.radioButtonVar)
            self.comboBoxVar=self.comboBoxStep.currentText()
            #print (self.comboBoxVar)
        except:
            print ('the data can not be read')

#test if port COM is connected in pc
        if(self.comVar==1):#pregunta si esta en modo enable la comuniccion
            self.x=list(serial.tools.list_ports.comports())
            #print self.x
            self.xLong=len(self.x)
            
            for i in range(0,int(self.xLong)):
                self.xTemp=str(self.x[i])
                if self.xTemp.find(self.COMCONTROL)>0:
                    self.portConnected=1
                    break
                else:
                    self.portConnected=0
            if self.portConnected==0:       
                self.graphVar=0
                self.btnGraph.setText("Graph")
                self.actionCom()
            
            
#############read port Com            
        if(self.graphVar==1):
            self.cadena = ''
            try:              
                #funcion de lectura de comunicacion Serial para hacer la cadena
                            
                self.limiteCadena=0
                self.contadorSerial=0
                self.control.flushInput()
                while self.limiteCadena==0:                           
                    self.cadena += self.control.read()
                    self.contadorSerial=self.contadorSerial+1
                            
                    if self.contadorSerial>=15:
                        self.limiteCadena=1
                        self.contadorSerial=0
    #                   print self.cadena
                                
            except:
                print ('the port can not be read')
    #################data spacer
            try:
                self.error=int(self.cadena[1:7])-500
                self.current=int(self.cadena[8:14])
                #print self.error
                #print self.current
                self.vector=self.vector+1
                if(self.vector>(int(self.rangoPlot)-1)):#rango de graficar
                    self.vector=(int(self.rangoPlot)-1)
                    for i in range(0, (int(self.rangoPlot)-1)):
                        self.vectorErr[i]=self.vectorErr[i+1]
                                                    
                #datos leidos guardadso en el vector
                self.vectorErr[self.vector]=self.error
                self.vectorCurrent[self.vector]=self.current
                #graficar
                self.data =self.vectorErr
                self.curve.setData(self.data)
            except:
                print "no readed data"
        
###########################################################################
app=QApplication(sys.argv)
form=GUI()
form.show()
app.exec_()
