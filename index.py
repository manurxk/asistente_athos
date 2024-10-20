import speech_recognition as sr
import subprocess as sub
from athos_guitt import FileNotFountError
import pyttsx3, pywhatkit, wikipedia, datetime,keyboard, cam, os
from pygame import mixer


name = "alex"
listener = sr.Recognizer()
engine = pyttsx3.init()

voices = engine.getProperty('voices')
engine.setProperty('voice' , voices[0].id)
engine.setProperty('rate' , 145)
sites={
                'google':'google.com',
                'youtube':'youtube.com',
                'facebook':'facebook.com',
                'whatsapp':'web.whatsapp.com',
                'cursos':'freecodecamp.org/learn'
}
files = {
    
}
programs = {
    'dbeaver': r"C:\Users\DELL\AppData\Local\DBeaver\dbeaver.exe -nl es",
    'apache':r"C:\Program Files\NetBeans-21\netbeans\bin\netbeans64.exe",
    'telegram':r"C:\Users\DELL\AppData\Roaming\Telegram Desktop\Telegram.exe",
    'zoon':r"C:\Users\DELL\AppData\Roaming\Zoom\uninstall\Installer.exe /uninstall",
    'xammpp':r"C:\xampp\xampp-control.exe",
    'word':r"",
    'excel':r"",
    'power point':r"",
}
def talk(text):
    engine.say(text)
    engine.runAndWait()
    
    
    
    
    
def listen():
    listener = sr.Recognizer()     
    with sr.Microphone() as source:
        print("Escuchando...")
        listener.adjust_for_ambient_noise(source)
        pc = listener.listen(source)
    try:
        rec = listener.recognize_google(pc, language="es")
        rec = rec.lower()
        
    except sr.UnknownValueError:
        print("No te entendí, intenta de nuevo")
    if name in rec:
        rec = rec.replace(name, '').strip()
    return rec

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
            print(search + ": " + wiki)
            talk(wiki)
        elif 'alarma' in rec: 
            num = rec.replace('alarma', '')
            num = num.strip()
            talk("Alarma activada a las " +  num + " horas")
            while True:
                if datetime.datetime.now().strftime('%H:%M') == num:
                    print("Despierta")
                    mixer.init()
                    mixer.music.load("adelee.mp3")
                    mixer.music.play()

                    if keyboard.read_key() == "s":
                        mixer.music.stop()
                        break
        elif 'colores' in rec:
            talk("Enseguida")
            cam.capture()
        elif 'abre' in rec:
            for site in sites:
                if site in rec:
                    sub.call(f'start chrome.exe {sites[site]}', shell=True)
                    talk(f'Abriendo{site}')
            for app in programs:
                if app in rec:
                    talk(f'Abriendo {app}')
                    sub.Popen(programs[app])

        elif 'archivo' in rec:
            for file in files:
                if file in rec:
                    sub.Popen([files[file]], shell=True)
                    talk(f'abriendo{file}')
        elif 'escribe' in rec:
            try:
                with open ("nota.txt",'a') as f:
                    write(f)
                    
            except FileNotFountError as e:
                file = open("nota.txt", 'w')
                write(file)
        
        elif 'termina' in rec:
            talk('YO LO AMO MAS A USTED ')
            break

def write(f):
    talk("que quieres que escriba?")
    rec_write = listen()
    f.write(rec_write + os.linesep)
    f.close()
    talk("listo, puedes revisarlo")
    sub.Popen("nota.txt", shell=True)

if __name__ == '__main__':
    run_alex()
