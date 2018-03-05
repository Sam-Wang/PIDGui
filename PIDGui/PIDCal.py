from PySide.QtCore import*
from PySide.QtGui import *


import sys
import time
import PIDGui
import serial
import pyqtgraph as pg
import numpy as np


class GUI(QDialog, PIDGui.Ui_GUI):
    def __init__(self,parent=None):
            super(GUI, self).__init__(parent)
            self.setupUi(self)
            #################Variables
            self.comVar=0
            self.graphVar=0
            self.contadorSerial=0
            self.limiteCadena=0
            self.vector=0
            #creacion de vectores para guardar datos iniciados en 0
            self.rangoPlot=100 #rango a graficar
            self.vectorErr=np.arange(self.rangoPlot)
            self.vectorCurrent=np.arange(self.rangoPlot)
            self.data=np.arange(self.rangoPlot)
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
            self.textEditCom.setText('COM12')
            self.textEditP.setText('0')
            self.textEditI.setText('0')
            self.textEditD.setText('0')
            self.textEditC.setText('0')
            self.textEditF.setText('0')
            self.textEditPM.setText('0')
            self.textEditPC.setText('0')
            self.textEditErr.setText('0')

            #####btn in disable
            self.btnLoad.setEnabled(False)
            self.btnSave.setEnabled(False)
            self.btnGraph.setEnabled(False)
            self.btnStepUp.setEnabled(False)
            self.btnStepDown.setEnabled(False)

            ############time interrupts
            timer=QTimer(self)
            timer.timeout.connect(self.Timer)
            timer.setInterval(100) #tiem in mS
            timer.start()

####################################Funtions             
    def actionCom(self):
        print ("actionCom")
        self.COMCONTROL=self.textEditCom.text() #read a num port Com
        print(self.COMCONTROL)
        if(self.comVar==0):
            self.comVar=1
            self.btnCom.setText("Disconnet")
            #####btn in disable
            self.btnLoad.setEnabled(True)
            self.btnSave.setEnabled(True)
            self.btnGraph.setEnabled(True)
            self.btnStepUp.setEnabled(True)
            self.btnStepDown.setEnabled(True)
            try:
                self.control.close()
                print('Prot COM closed')
            except:
                print('Prot no COM closed')
            try:
                self.control=serial.Serial(self.COMCONTROL,19200,timeout=0.5) #config a port com
                self.control.flushInput()
                print ("port com connect 1")
                #self.control=open() #open Port Com
                #print ("port com connect 2")
            except:
                print ("no port com connect")
            
        else:
            self.comVar=0
            self.btnCom.setText("Connet")
            #####btn in disable
            self.btnLoad.setEnabled(False)
            self.btnSave.setEnabled(False)
            self.btnGraph.setEnabled(False)
            self.btnStepUp.setEnabled(False)
            self.btnStepDown.setEnabled(False)
            
            self.control.close() #close port Com
            
        #print(self.comVar)
    def actionLoad(self):
        print ("actionLoad")
        try:   
            self.control.write("@")
            while self.limiteCadena==0:                           
                self.controlData += self.control.read()
        except:
            print("Faild Readin configuration")
            
    def actionSave(self):
        print ("actionSave")
        
    def actionGraph(self):
        print ("actionGraph")
        if(self.graphVar==0): #clic para graficar
            self.graphVar=1
            self.btnGraph.setText("Stop")  #switch a text label
            try:
                self.control.write("U1")  #imprimir por el puerto serial 
            except:
                print("Faild Write port com")
            
        else: #clic para detener grafica
            self.graphVar=0
            self.btnGraph.setText("Graph") #switch a text label
            try:
                self.control.write("U0")  #imprimir por el puerto serial 
            except:
                print("Faild Write port com")
                
    def actionStepUp(self):
        print ("actionStepUp")
    def actionStepDown(self):
        print ("actionStepDown")
    def actionRestar(self):
        print ("actionRestar")
        self.textEditP.setText('0')
        self.textEditI.setText('0')
        self.textEditD.setText('0')
        self.textEditC.setText('0')
        self.textEditF.setText('0')
        self.textEditPM.setText('0')
        self.textEditPC.setText('0')
        self.textEditErr.setText('0')
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
#                        print self.cadena
                        
            except:
                print ('the port can not be read')

        #################data spacer
            self.error=int(self.cadena[1:7])-500
            self.current=int(self.cadena[8:14])
            print self.error
            print self.current
            self.vector=self.vector+1
            if(self.vector>(self.rangoPlot-1)):#rango de graficar
                self.vector=(self.rangoPlot-1)
                for i in range(0, (self.rangoPlot-1)):
                    self.vectorErr[i]=self.vectorErr[i+1]
                    

                
            #datos leidos guardadso en el vector
            self.vectorErr[self.vector]=self.error
            self.vectorCurrent[self.vector]=self.current
            #graficar
            self.data =self.vectorErr
            self.curve.setData(self.data)
            
    

        
###########################################################################
app=QApplication(sys.argv)
form=GUI()
form.show()
app.exec_()
