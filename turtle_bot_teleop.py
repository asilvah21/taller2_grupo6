#!/usr/bin/env python3

import tkinter
from logging import root
from tokenize import String
from numpy import expand_dims

import rospy
from pynput import keyboard
from geometry_msgs.msg import Twist

global vel_msg

ventana=tkinter.Tk()
ventana.title("Archivo de Escritura")
ventana.resizable(0,0)
frame=tkinter.Frame(ventana)
frame.pack(expand=True)
label1=tkinter.Label(frame, text="Asigne un nombre si desea guardar el archivo txt del recorrido",padx=10)
label1.grid(row=0,column=0)
nombre=tkinter.StringVar()
cuadrotexto1=tkinter.Entry(frame, textvariable=nombre,width=45)
cuadrotexto1.grid(row=1,column=0, padx=10, pady=10)
label2=tkinter.Label(frame, text="Nombre de la carpeta personal",padx=10)
label2.grid(row=2,column=0)
carpeta=tkinter.StringVar()
cuadrotexto2=tkinter.Entry(frame, textvariable=carpeta,width=45)
cuadrotexto2.grid(row=3,column=0, padx=10, pady=10)

def archivo():
    nombrearchivo=nombre.get()
    tipoarchivo=".txt"
    carpetapersonal=carpeta.get()
    ruta1="/home/"
    ruta2="/catkin_ws/src/mi_robot_6/results/"
    archivocompleto=ruta1+carpetapersonal+ruta2+nombrearchivo+tipoarchivo
    archivo1=open(archivocompleto,"w")
    archivo1.close()
    return archivocompleto


boton1=tkinter.Button(ventana, text="Guardar",command=archivo, padx=20)
boton1.pack()
boton2=tkinter.Button(ventana,text="Cerrar",command=ventana.destroy, padx=26)
boton2.pack()

ventana.mainloop()

nombrearchivo=archivo()

def on_press(key):
    global vel_msg,archivo


    if format(key.char)=="d":
        vel_msg.linear.x=0.5
        vel_msg.angular.z=(1/0.1533)
    
    if format(key.char)=="w":
        vel_msg.linear.x=1.0
        vel_msg.angular.z=0.0
    
    if format(key.char)=="s":
        vel_msg.linear.x=-1.0
        vel_msg.angular.z=0.0
        
    if format(key.char)=="a":
        vel_msg.linear.x=0.5
        vel_msg.angular.z=-(1/0.1533)
    
    archivoescritura = open(nombrearchivo,'a')
    archivoescritura.write('\n' + format(key.char))

    try:
        print('Tecla alfanumérica {0} presionada'.format(key.char))
    except AttributeError:
        print('Tecla especial {0} presionada'.format(key.char))

def on_release(key):
    vel_msg.linear.x=0.0
    vel_msg.angular.z=0.0
    print('Tecla {0} liberada'.format(key))
    if key == keyboard.Key.esc:
        # Stop listener
        return False

listener = keyboard.Listener(on_press=on_press,on_release=on_release)
listener.start()  
        
if __name__ == '__main__':
    try:
        rospy.init_node('turtle_bot_teleop',anonymous=False)
        vel_pub=rospy.Publisher('/turtlebot_cmdVel',Twist, queue_size=10)
        vel_msg=Twist()
        while not rospy.is_shutdown():
            vel_pub.publish(vel_msg)
    except rospy.ROSInterruptException:
        nombrearchivo.close()
        pass    
