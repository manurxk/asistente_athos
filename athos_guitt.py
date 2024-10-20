#importacion de las bibliotecas de python para el asistente
import speech_recognition as sr
import subprocess as sub
import pyttsx3
import pywhatkit
import wikipedia
import datetime
import keyboard
import cam
import os
from tkinter import *
from PIL import Image, ImageTk
from pygame import mixer
import threading as tr
import whatsapp as whapp
import database
import webbrowser as browser
from chatterbot import ChatBot
from chatterbot import preprocessors
from chatterbot.trainers import ListTrainer
from tuyapy import TuyaApi

#configuracion de los datos para la api de tuyasmart
api = TuyaApi()
api.init('angi020101@gmail.com', 'Baes#512', '595')
device_id = 'ebe498cf2510583e114ldk'
switch = api.get_device_by_id(device_id)

#configura el titula de la ventana y dimensiones
main_window = Tk()
main_window.title("ASISTENTE DE TRABAJO, HERRAMIENTAS Y OPERACIONES DEL SISTEMA")
main_window.geometry("750x900")
main_window.resizable(0,0)
main_window.configure(bg='#4b6cb7')

#recordatorio de las funciones que realiza el asistente
comandos = """
    Comandos que puedes usar:
    - Reproduce..(canción)
    - Busca...(algo)
    - Abre...(página web o app)
    - Alarma..(hora en 24H)
    - Archivo...(nombre)
    - Termina
"""
# aca se puede editar el titulo y la imagen del asistente
label_title = Label (main_window, text= "ATHOS AI", bg="#6DD5FA", fg="#2c3e50",
                     font=('Arial', 30, 'bold'))
label_title.pack(pady=10)

canvas_comandos= Canvas(bg="#2193b0", height=250, width=250)
canvas_comandos.place(x=500, y=650)
canvas_comandos.create_text(120,80, text=comandos,fill="white", font='Arial 8')

#cuadro de habla
text_info = Text(main_window, bg="#6dd5ed", fg="#434343")
text_info.place(x=0, y=650, height=250, width=500)

#foto del asistente
asistente_photo = ImageTk.PhotoImage(Image.open("athos.png"))
window_photo = Label(main_window, image=asistente_photo)
window_photo.pack(pady=5)

#variables de las voces
def mexican_voice():
    change_voice(0)

def spanish_voice():
    change_voice(1)

def english_voice():
    change_voice(2)

def change_voice(id):
    engine.setProperty('voice', voices[id].id)
    engine.setProperty('rate', 145)
    talk("Iniciando el Programa del Asistente de trabajo,herramientas y Operaciones en el sistema ATHOS!")

#Nombre del asistente
name = "ATHOS"
listener = sr.Recognizer()
engine = pyttsx3.init()

voices = engine.getProperty('voices')
engine.setProperty('voice' , voices[0].id)
engine.setProperty('rate' , 145)
for voice in voices:
    print(voice)
    
# variable para que el asistente escuche y escribe   
def charge_data(name_dict, name_file):
    try:
        with open(name_file) as f:
            for line in f:
                (key, val) = line.split(",")
                val = val.rstrip("\n")
                name_dict[key] = val
    except FileNotFoundError as e:
        pass
    
#variables de los sitios. app. paginas web y contactos
sites = dict()
charge_data(sites, "pages.txt")
files = dict()
charge_data(files, "archivos.txt")
programs = dict()
charge_data(programs, "apps.txt")
contacts = dict()
charge_data(contacts, "contacts.txt")


def talk(text):
    engine.say(text)
    engine.runAndWait()

def read_and_talk():
    text = text_info.get("1.0", "end")
    talk(text)

def write_text(text_wiki):
    text_info.insert(INSERT, text_wiki)

def listen(phrase=None):
    listener = sr.Recognizer()    
    with sr.Microphone() as source:            
        listener.adjust_for_ambient_noise(source)
        talk(phrase)
        pc = listener.listen(source)
    try:
        rec = listener.recognize_google(pc, language="es")
        rec = rec.lower()
    except sr.UnknownValueError:
        print("No te entendí, intenta de nuevo")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
    return rec
#//////////////////////////////////////////////#
# Funciones asociadas a las palabras claves


def reproduce(rec):
    music = rec.replace('reproduce', '')
    print("Reproduciendo " + music)
    talk("Reproduciendo " + music)
    pywhatkit.playonyt(music)


def busca(rec):
    search = rec.replace('busca', '')
    wikipedia.set_lang("es")
    wiki = wikipedia.summary(search, 1)
    talk(wiki)
    write_text(search + ": " + wiki)


def thread_alarma(rec):
    t = tr.Thread(target=clock, args=(rec,))
    t.start()


def colores(rec):
    talk("Enseguida")
    t = tr.Thread(target=cam.capture)
    t.start()
    

def abre(rec):
    task = rec.replace('abre', '').strip()

    if task in sites:
        for task in sites:
            if task in rec:
                sub.call(f'start chrome.exe {sites[task]}', shell=True)
                talk(f'Abriendo {task}')
    elif task in programs:
        for task in programs:
            if task in rec:
                talk(f'Abriendo {task}')
                os.startfile(programs[task])
    else:
        talk("Lo siento, parece que aún no has agregado esa app o página web, \
            usa los botones de agregar!")


def archivo(rec):
    file = rec.replace('archivo', '').strip()
    if file in files:
        for file in files:
            if file in rec:
                sub.Popen([files[file]], shell=True)
                talk(f'Abriendo {file}')
    else:
        talk("Lo siento, parece que aún no has agregado ese archivo, \
            usa los botones de agregar!")


def escribe(rec):
    try:
        with open("nota.txt", 'a') as f:
            write(f)

    except FileNotFoundError as e:
        file = open("nota.txt", 'a')
        write(file)
def clock(rec):
    num = rec.replace('alarma', '')
    num = num.strip()
    talk("Alarma activada a las " + num + " horas")
    if num[0] != '0' and len(num) < 5:
        num = '0' + num
    print(num)
    while True:
        if datetime.datetime.now().strftime('%H:%M') == num:
            print("DESPIERTA!!!")
            mixer.init()
            mixer.music.load("auronplay-alarma.mp3")
            mixer.music.play()
        else:
            continue
        if keyboard.read_key() == "s":
            mixer.music.stop()
            break

def enviar_mensaje(rec):
    talk("¿A quién quieres enviar el mensaje?")
    contact = listen("Te escucho")
    contact = contact.strip()

    if contact in contacts:
        for cont in contacts:
            if cont == contact:
                contact = contacts[cont]
                talk("¿Qué mensaje quieres enviarle?")
                message = listen("Te escucho")
                talk("Enviando mensaje...")
                whapp.send_message(contact, message)
    else:
        talk("Parece qué aún no has agregado a ese contacto, usa el botón de agregar!")

def cierra(rec):
    for task in programs:
        kill_task = programs[task].split('\\')
        kill_task = kill_task[-1]
        if task in rec:
            sub.call(f'TASKKILL /IM {kill_task} /F', shell=True)
            talk(f'Cerrando {task}')
        if 'todo' in rec:
            sub.call(f'TASKKILL /IM {kill_task} /F', shell=True)
            talk(f'Cerrando {task}')
    if 'ciérrate' in rec:
        talk('Adiós!')
        sub.call('TASKKILL /IM athos_guit.exe /F', shell=True)
        
def buscame(rec):
    something = rec.replace('búscame', '').strip()
    talk("Buscando " + something)
    browser.search(something)            

#def reconocimiento(rec):
 #   rec = rec.replace('reconocimiento', '').strip()
  #  if rec == 'activado':
   #     t = tr.Thread(target=fr.face_rec, args=(0,))
    #    t.start()
     #   talk("Activando alarma de reconocimiento...")
    #elif 'aguacate':
     #   fr.face_rec(1)


# Diccionario con palabras claves
key_words = {
    'reproduce': reproduce,
    'busca': busca,
    'alarma': thread_alarma,
    'colores': colores,
    'abre': abre,
    'archivo': archivo,
    'escribe': escribe,
    'mensaje': enviar_mensaje,
    'cierra': cierra,
    'ciérrate': cierra,
    'búscame': buscame,



}
#////////////////////////////////////////////
def FileNotFountError ():
    pass
def run_alex():
    v=0
    while v==0:
        rec = listen() 
        if 'reproduce' in rec:
            v=1
            music = rec.replace('reproduce', '')
            print("Reproduciendo " + music)
            talk("Reproduciendo " + music)
            pywhatkit.playonyt(music)
            
            
        elif 'busca' in rec:
            v=1
            search = rec.replace ('busca','')
            wikipedia.set_lang("es")
            wiki = wikipedia.summary(search, 1)
            talk(wiki)
            write_text(search + ": " + wiki)
            
            
        elif 'alarma' in rec:
            v=1
            t = tr.Thread(target=clock, args=(rec,)) 
            t.start()
            
            
        elif 'colores' in rec:
            v=1
            talk("Enseguida")
            cam.capture()
            
            
        elif 'abre' in rec:
            v=1
            task = rec.replace ('abre', '').strip
            
            if task in sites:
                for task in sites:
                    if task in rec:
                        sub.call(f'start chrome.exe {sites[task]}', shell=True)
                        talk(f'Abriendo{task}')
            elif task in programs:
                for task in programs:
                    if task in rec:
                        talk(f'Abriendo {task}')
                        sub.Popen(programs[task])
                        
            else:
                talk("LO SIENtO, PERO PARECE QUE AUN NO SE AÑADIDO ESA PAGINA WEB O APP,NO OLVIDES USAR LOS BOTONES PARA AGREGAR")
        
        elif 'archivo' in rec:
            v=1
            file = rec.replace('archivo','').strip()
            if file in files:
                for file in files:
                    if file in rec:
                        sub.Popen([files[file]], shell=True)
                        talk(f'abriendo{file}')
            else:
                talk("LO SIENtO, PERO PARECE QUE AUN NO SE AÑADIDO EL archivo,NO OLVIDES USAR LOS BOTONES PARA AGREGAR")
            
           
        elif 'escribe' in rec:
            v=1
            try:
                with open ("nota.txt",'a') as f:
                    write(f)
                    
            except FileNotFountError as e:
                file = open("nota.txt", 'w')
                write(file)
            
        elif 'encender luces' in rec:
            v = 1
            switch.turn_on()  # Enciende el dispositivo
            talk("Las luces han sido encendidas")
            
        elif 'apagar luces' in rec:
            v = 1
            switch.turn_off()  # Enciende el dispositivo
            talk("Las luces han sido apagadas")
            
        elif 'termina' in rec:
            v=1
            talk('HASTA LUEGO')
            

def write(f):
    talk("que quieres que escriba?")
    rec_write = listen()
    f.write(rec_write + os.linesep)
    f.close()
    talk("listo, puedes revisarlo")
    sub.Popen("nota.txt", shell=True)


def open_file_window():
    global namef_entry, rutef_entry
    file_win = Toplevel()
    file_win.title("Agregar archivos")
    file_win.geometry('300x200')
    file_win.configure(bg="#434343")
    file_win.resizable(0, 0)
    main_window.eval(f'tk::PlaceWindow {str(file_win)} center')
    title_label = Label(file_win, text="Agrega un archivo", fg="white",
                        bg="#434343", font=('Arial', 15, 'bold')).pack(pady=3)
    text_name = Label(file_win, text="Nombre del archivo", fg="white",
                      bg="#434343", font=('Arial', 10, 'bold')).pack(pady=2)
    namef_entry = Entry(file_win)
    namef_entry.pack(pady=1)
    text_rute = Label(file_win, text="Ruta del archivo", fg="white",
                      bg="#434343", font=('Arial', 10, 'bold')).pack(pady=2)
    rutef_entry = Entry(file_win, width=30)
    rutef_entry.pack(pady=1)
    button_add = Button(file_win, text="Agregar", bg='#16222A',
                        fg="white", width=8, height=1, command=add_files).pack(pady=5)


def open_page_window():
    global namep_entry, rutep_entry
    file_win = Toplevel()
    file_win.title("Agregar páginas")
    file_win.geometry('300x200')
    file_win.configure(bg="#434343")
    file_win.resizable(0, 0)
    main_window.eval(f'tk::PlaceWindow {str(file_win)} center')
    title_label = Label(file_win, text="Agrega una página web", fg="white",
                        bg="#434343", font=('Arial', 15, 'bold')).pack(pady=3)
    text_name = Label(file_win, text="Nombre de la página", fg="white",
                      bg="#434343", font=('Arial', 10, 'bold')).pack(pady=2)
    namep_entry = Entry(file_win)
    namep_entry.pack(pady=1)
    text_rute = Label(file_win, text="URL de la página", fg="white",
                      bg="#434343", font=('Arial', 10, 'bold')).pack(pady=2)
    rutep_entry = Entry(file_win, width=30)
    rutep_entry.pack(pady=1)
    button_add = Button(file_win, text="Agregar", bg='#16222A',
                        fg="white", width=8, height=1, command=add_sites).pack(pady=5)


def open_app_window():
    global namea_entry, rutea_entry
    file_win = Toplevel()
    file_win.title("Agregar apps")
    file_win.geometry('300x200')
    file_win.configure(bg="#434343")
    file_win.resizable(0, 0)
    main_window.eval(f'tk::PlaceWindow {str(file_win)} center')
    title_label = Label(file_win, text="Agrega una app", fg="white",
                        bg="#434343", font=('Arial', 15, 'bold')).pack(pady=3)
    text_name = Label(file_win, text="Nombre de la app", fg="white",
                      bg="#434343", font=('Arial', 10, 'bold')).pack(pady=2)
    namea_entry = Entry(file_win)
    namea_entry.pack(pady=1)
    text_rute = Label(file_win, text="Ruta de la app", fg="white",
                      bg="#434343", font=('Arial', 10, 'bold')).pack(pady=2)
    rutea_entry = Entry(file_win, width=30)
    rutea_entry.pack(pady=1)
    button_add = Button(file_win, text="Agregar", bg='#16222A',
                        fg="white", width=8, height=1, command=add_apps).pack(pady=5)

def open_contact_window():
    global namec_entry, phone_entry
    contact_win = Toplevel()
    contact_win .title("Agregar contacto")
    contact_win .geometry('300x200')
    contact_win .configure(bg="#434343")
    contact_win .resizable(0, 0)
    main_window.eval(f'tk::PlaceWindow {str(contact_win )} center')
    title_label = Label(contact_win, text="Agrega un contacto", fg="white",
                        bg="#434343", font=('Arial', 15, 'bold')).pack(pady=3)
    text_name = Label(contact_win, text="Nombre del contacto", fg="white",
                      bg="#434343", font=('Arial', 10, 'bold')).pack(pady=2)
    namec_entry = Entry(contact_win)
    namec_entry.pack(pady=1)
    phone_number = Label(contact_win, text="Número de teléfono (con código de país)", fg="white",
                      bg="#434343", font=('Arial', 10, 'bold')).pack(pady=2)
    phone_entry = Entry(contact_win, width=30)
    phone_entry.pack(pady=1)
    button_add = Button(contact_win, text="Agregar", bg='#16222A',
                        fg="white", width=8, height=1, command=add_contacts).pack(pady=5)
# Funciones para agregar cosas a los diccionarios


def add_files():
    namef = namef_entry.get()
    rutef = rutef_entry.get()
    files[namef] = rutef
    save_files("archivos.txt", namef, rutef)
    namef_entry.delete(0, "end")
    rutef_entry.delete(0, "end")
def add_sites():
    namep = namep_entry.get()
    rutep = rutep_entry.get()
    sites[namep] = rutep
    save_files("sitios.txt", namep, rutep)
    namep_entry.delete(0, "end")
    rutep_entry.delete(0, "end")
def add_apps():
    namea = namea_entry.get()
    rutea = rutea_entry.get()
    programs[namea] = rutea
    save_files("apps.txt", namea, rutea)
    namea_entry.delete(0, "end")
    rutea_entry.delete(0, "end")
def add_contacts():
    namec = namec_entry.get()
    phone = phone_entry.get()
    contacts[namec] = phone
    save_files("contacts.txt", namec, phone)
    namec_entry.delete(0, "end")
    phone_entry.delete(0, "end")
def save_files(file, name, route):
    try:
        with open(file, 'a') as f:
            f.write(name + "," + route + "\n")
    except FileNotFoundError as e:
        file = open(file, 'a')
        file.write(name + "," + route + "\n")

  
def talk(text):
    engine.say(text)
    engine.runAndWait()
    
def read_and_talk():
    text = text_info.get("1.0","end")
    talk(text)
def write_text(text_wiki):
    text_info.insert(INSERT, text_wiki)
def listen():
    listener = sr.Recognizer()  
    rec = ""  
    try:
        with sr.Microphone() as source:
            talk("Te Escucho...")
            pc = listener.listen(source)
            rec = listener.recognize_google(pc, language="es")
            rec = rec.lower()
            if name in rec:
                rec = rec.replace(name, '')

    except Exception as e:
        print(f"Error: {e}")  

    return rec

def clock(rec):
    num = rec.replace('alarma', '')
    num = num.strip()
    talk("Alarma activada a las " +  num + " horas")
    if num[0] != '0' and len(num) <5:
        num = '0' + num
    print (num)
    while True:
        if datetime.datetime.now().strftime('%H:%M') == num:
            print("Despierta")
            mixer.init()
            mixer.music.load("adelee.mp3")
            mixer.music.play()
        else:
            continue
        if keyboard.read_key() == "s":
            mixer.music.stop()
        break





name = "alex"
listener = sr.Recognizer()
engine = pyttsx3.init()

voices = engine.getProperty('voices')
engine.setProperty('voice' , voices[0].id)
engine.setProperty('rate' , 145)
for voice in voices:
    print(voice)
    
 # Función para que Juanita diga que cosas ha guardado el usuario


def talk_files():
    if bool(files) == True:
        talk("Has agregado los siguientes archivos")
        for file in files:
            talk(file)
    else:
        talk("Aún no has agregado archivos!")


def talk_sites():
    if bool(sites) == True:
        talk("Has agregado los siguientes sitios web!")
        for site in sites:
            talk(site)
    else:
        talk("Aún no has agregado sitios web!")


def talk_apps():
    if bool(programs) == True:
        talk("Has agregado las siguientes aplicaciones")
        for app in programs:
            talk(app)
    else:
        talk("Aún no has agregado aplicaciones!")

def talk_contacts():
    if bool(contacts) == True:
        talk("Has agregado a los siguientes contactos")
        for cont in contacts:
            talk(cont)
    else:
        talk("Aún no has agregado contactos!")
           







#botones de idioma
Button_voice_py = Button(main_window, text="Voz Py", fg="white", bg="#45a247",
                              font=("Arial", 12, "bold"), command=mexican_voice)
Button_voice_py.place(x=30, y=400, width=120, height=40)
Button_voice_es = Button(main_window, text="Voz España", fg="white", bg="#f12711",
                              font=("Arial", 12, "bold"), command=spanish_voice) 
Button_voice_es.place(x=30, y=450, width=120, height=40)
Button_voice_us = Button(main_window, text="Voz USA", fg="white", bg="#4286f4",
                              font=("Arial", 12, "bold"), command=english_voice) 
Button_voice_us.place(x=30, y=500, width=120, height=40)

#boton de hablar
Button_speak = Button(main_window, text="Hablar", fg="white", bg="#45a247",
                              font=("Arial", 12, "bold"), command=read_and_talk)
Button_speak.place(x=30, y=550, width=120, height=40)


#boton de escuchar
Button_listen = Button(main_window, text="Escuchar", fg="white", bg="#1565c0", 
                       font=("Arial", 15, "bold"), command=run_alex)
Button_listen.pack(pady=20)



#botones de agregar archivos
Button_add_files = Button(main_window, text="Agregar Archivo", fg="white", bg="#45a247",
                              font=("Arial", 12, "bold"), command=open_file_window)
Button_add_files.place(x=565, y=400, width=160, height=40)
Button_apps = Button(main_window, text="Agregar Apps", fg="white", bg="#f12711",
                              font=("Arial", 12, "bold"), command=open_app_window) 
Button_apps.place(x=565, y=450, width=160, height=40)
Button_add_pages = Button(main_window, text="Agregar Paginas", fg="white", bg="#4286f4",
                              font=("Arial", 12, "bold"), command=open_page_window) 
Button_add_pages.place(x=565, y=500, width=160, height=40)
button_add_contacts = Button(main_window, text="Agregar contactos", fg="white", bg="#4286f4",
                          font=("Arial", 12, "bold"), command=open_contact_window)
button_add_contacts.place(x=565, y=550, width=160, height=40)






button_tell_pages = Button(main_window, text="Páginas agregadas", fg="white", bg="#2c3e50",
                           font=("Arial", 10, "bold"), command=talk_sites)
button_tell_pages.place(x=30, y=600, width=160, height=40)


button_tell_apps = Button(main_window, text="Apps agregadas", fg="white", bg="#2c3e50",
                          font=("Arial", 10, "bold"), command=talk_apps)
button_tell_apps.place(x=30, y=600, width=150, height=40)


button_tell_files = Button(main_window, text="Archivos agregados", fg="white", bg="#2c3e50",
                           font=("Arial", 10, "bold"), command=talk_files)
button_tell_files.place(x=375, y=600, width=175, height=40)
#button_tell_files.pack(side=BOTTOM, pady=3)


button_tell_contacts = Button(main_window, text="Contactos agregados", fg="white", bg="#2c3e50",
                           font=("Arial", 10, "bold"), command=talk_contacts)
button_tell_contacts.place(x=550, y=600, width=175, height=40)






main_window.mainloop()