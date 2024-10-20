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

main_window = Tk()
main_window.title("ASISTENTE DE TRABAJO, HERRAMIENTAS Y OPERACIONES DEL SISTEMA")

main_window.geometry("700x800")
main_window.resizable(0,0)
main_window.configure(bg='#4b6cb7')
#uigradients.com colores
#interfaz


comandos ="""
COMANDOS QUE PUEDES USAR:
-Reproduce. (Youtube)
-Busca. (Algo)
-Abre. (paginas web o app)
-Alarma. (hora en 24hs.)
-Archivo. (nombre)
-Termina

"""
label_title = Label (main_window, text= "ATHOS AI", bg="#6DD5FA", fg="#2c3e50",
                     font=('Arial', 30, 'bold'))
label_title.pack(pady=10)

canvas_comandos= Canvas(bg="#2193b0", height=150, width=200)
canvas_comandos.place(x=0, y=650)
canvas_comandos.create_text(120,80, text=comandos,fill="white", font='Arial 8')

text_info = Text(main_window, bg="#6dd5ed", fg="#434343")
text_info.place(x=0, y=50, height=150, width=200)


asistente_photo = ImageTk.PhotoImage(Image.open("alex.jpg"))
window_photo = Label(main_window, image=asistente_photo)
window_photo.pack(pady=5)

def window_files():
    pass #noborrar

def py_voice():
    change_voice(0)
def spanish_voice():
    change_voice(1)
def english_voice():
    change_voice(2)
def change_voice(id):
    engine.setProperty('voice', voices[id].id)
    engine.setProperty('rate', 145)
    talk("Hola soy ATHOS")



def run_alex():
    while True:
        rec = listen() 
        if 'reproduce' in rec:
            music = rec.replace('reproduce', '')
            print("Reproduciendo " + music)
            talk("Reproduciendo " + music)
            pywhatkit.playonyt(music)
            
        elif 'busca' in rec:
            search = rec.replace ('busca','')
            wikipedia.set_lang("es")
            wiki = wikipedia.summary(search, 1)
            talk(wiki)
            write_text(search + ": " + wiki)
            break
            
        elif 'alarma' in rec:
            t = tr.Thread(target=clock, args=(rec,)) 
            t.start()
            
        elif 'colores' in rec:
            talk("Enseguida")
            cam.capture()
            
        elif 'abre' in rec:
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
                talk("LO SIENO, PERO PARECE QUE AUN NO SE AÑADIDO ESA PAGINA WEB O APP,NO OLVIDES USAR LOS BOTONES PARA AGREGAR")

        elif 'archivo' in rec:
            file = rec.replace('archivo','').strip()
            if file in files:
                for file in files:
                    if file in rec:
                        sub.Popen([files[file]], shell=True)
                        talk(f'abriendo{file}')
            else:
                talk("LO SIENO, PERO PARECE QUE AUN NO SE AÑADIDO EL archivo,NO OLVIDES USAR LOS BOTONES PARA AGREGAR")
           
        elif 'escribe' in rec:
            try:
                with open ("nota.txt",'a') as f:
                    write(f)
                    
            except FileNotFountError as e:
                file = open("nota.txt", 'w')
                write(file)
        
        elif 'termina' in rec:
            talk('HASTA LUEGO')
            break

def write(f):
    talk("que quieres que escriba?")
    rec_write = listen()
    f.write(rec_write + os.linesep)
    f.close()
    talk("listo, puedes revisarlo")
    sub.Popen("nota.txt", shell=True)


def open_w_files():
    global namefile_entry, pathf_entry
    window_files = Toplevel()
    window_files.title("Agregar Archivos")
    window_files.configure(bg="#434343")
    window_files.geometry("500x400")
    window_files.resizable(0,0)
    main_window.eval(f'tk::PlaceWindow {str(window_files)} center')
    
    title_label = Label(window_files, text="Agrega un Archivo", fg="white", bg="#434343", font=('Arial', 15, 'bold'))
    title_label.pack(pady=3)
    name_label = Label(window_files, text="Nombre del Archivo", fg="white", bg="#434343", font=('Arial', 10, 'bold'))
    name_label.pack(pady=2)
    
    namefile_entry = Entry(window_files)
    namefile_entry.pack(pady=1)
    
    path_label = Label(window_files, text="Ruta del Archivo", fg="white", bg="#434343", font=('Arial', 10, 'bold'))
    path_label.pack(pady=2)
    
    pathf_entry = Entry(window_files, width=35)
    pathf_entry.pack(pady=1)
    
    save_button = Button(window_files, text="Guardar", fg="white", bg="#16222A", width=8, height=1, command=add_files)
    save_button.pack(pady=4)
    
def open_w_apps():
    global nameapps_entry, patha_entry
    window_apps = Toplevel()
    window_apps.title("Agregar Archivos")
    window_apps.configure(bg="#434343")
    window_apps.geometry("500x400")
    window_apps.resizable(0,0)
    main_window.eval(f'tk::PlaceWindow {str(window_apps)} center')
    
    title_label = Label(window_apps, text="Agrega una Aplicación", fg="white", bg="#434343", font=('Arial', 15, 'bold'))
    title_label.pack(pady=3)
    name_label = Label(window_apps, text="Nombre de la Aplicación", fg="white", bg="#434343", font=('Arial', 10, 'bold'))
    name_label.pack(pady=2)
    
    namefile_entry = Entry(window_apps)
    namefile_entry.pack(pady=1)
    
    path_label = Label(window_apps, text="Ruta de la Aplicación", fg="white", bg="#434343", font=('Arial', 10, 'bold'))
    path_label.pack(pady=2)
    
    patha_entry = Entry(window_apps, width=35)
    patha_entry.pack(pady=1)
    
    save_button = Button(window_apps, text="Guardar", fg="white", bg="#16222A", width=8, height=1, command=add_apps)
    save_button.pack(pady=4)
    

def open_w_pages():
    global namepages_entry, pathp_entry
    window_pages = Toplevel()
    window_pages.title("Agregar Archivos")
    window_pages.configure(bg="#434343")
    window_pages.geometry("500x400")
    window_pages.resizable(0,0)
    main_window.eval(f'tk::PlaceWindow {str(window_pages)} center')
    title_label = Label(window_pages, text="Agrega una Página", fg="white", bg="#434343", font=('Arial', 15, 'bold'))
    title_label.pack(pady=3)
    name_label = Label(window_pages, text="Nombre de la Página", fg="white", bg="#434343", font=('Arial', 10, 'bold'))
    name_label.pack(pady=2)
    
    namefile_entry = Entry(window_pages)
    namefile_entry.pack(pady=1)
    
    path_label = Label(window_pages, text="Ruta de la Página", fg="white", bg="#434343", font=('Arial', 10, 'bold'))
    path_label.pack(pady=2)
    
    pathp_entry = Entry(window_pages, width=35)
    pathp_entry.pack(pady=1)
    
    save_button = Button(window_pages, text="Guardar", fg="white", bg="#16222A", width=8, height=1, command=add_pages)
    save_button.pack(pady=4)



def add_files():
    name_file = namefile_entry.get().strip()
    path_file = pathf_entry.get().strip()
    
    files[name_file] = path_file
    namefile_entry.delete(0, "end")
    pathf_entry.delete(0, "end")

def add_apps():
    name_file = nameapps_entry.get().strip()
    path_file = patha_entry.get().strip()
    
    programs[name_file] = path_file
    nameapps_entry.delete(0, "end")
    patha_entry.delete(0, "end")

def add_pages():
    name_file = namepages_entry.get().strip()
    path_file = pathp_entry.get().strip()
    
    sites[name_file] = path_file
    namepages_entry.delete(0, "end")
    pathp_entry.delete(0, "end")


  
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
    try:   
        with sr.Microphone() as source:
            talk("Te Escucho...")
            pc = listener.listen(source)
            rec = listener.recognize_google(pc, language="es")
            rec = rec.lower()
            if name in rec:
                rec = rec.replace(name, '')
            
    except:
        pass
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
    
    
sites = dict()
files = dict()
programs = dict()







Button_voice_py = Button(main_window, text="Voz Py", fg="white", bg="#45a247",
                              font=("Arial", 12, "bold"), command=py_voice)
Button_voice_py.place(x=605, y=100, width=120, height=40)
Button_voice_es = Button(main_window, text="Voz España", fg="white", bg="#f12711",
                              font=("Arial", 12, "bold"), command=spanish_voice) 
Button_voice_es.place(x=605, y=150, width=120, height=40)
Button_voice_us = Button(main_window, text="Voz USA", fg="white", bg="#4286f4",
                              font=("Arial", 12, "bold"), command=english_voice) 
Button_voice_us.place(x=605, y=200, width=120, height=40)
Button_listen = Button(main_window, text="Escuchar", fg="white", bg="#1565c0", 
                       font=("Arial", 15, "bold"), command=run_alex)
Button_listen.pack(pady=10)


Button_add_files = Button(main_window, text="Agregar Archivo", fg="white", bg="#45a247",
                              font=("Arial", 12, "bold"), command=open_w_files)
Button_add_files.place(x=605, y=350, width=140, height=40)
Button_apps = Button(main_window, text="Agregar Apps", fg="white", bg="#f12711",
                              font=("Arial", 12, "bold"), command=open_w_apps) 
Button_apps.place(x=605, y=400, width=140, height=40)
Button_add_pages = Button(main_window, text="Agregar Paginas", fg="white", bg="#4286f4",
                              font=("Arial", 12, "bold"), command=open_w_pages) 
Button_add_pages.place(x=605, y=450, width=140, height=40)


Button_speak = Button(main_window, text="Hablar", fg="white", bg="#45a247",
                              font=("Arial", 12, "bold"), command=read_and_talk)
Button_speak.place(x=605, y=250, width=120, height=40)


main_window.mainloop()